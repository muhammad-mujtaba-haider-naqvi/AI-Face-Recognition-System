"""
Attendance Manager module for automatic attendance logging.

- Stores attendance in MySQL with one record per student per day
- Provides duplicate prevention, filtering, sorting, searching
- Uses parameterized queries and logging instead of prints
- Designed to be called from the face recognition loop without slowing it down

Configuration
-------------
Set via environment variables or pass a config dict to AttendanceManager:
- DB_HOST (default: 127.0.0.1)
- DB_USER (default: root)
- DB_PASSWORD (default: 12345)
- DB_NAME (default: FaceRecognitionSystem)

Schema
------
See attendance_schema.sql for full DDL. Key points:
- Table `attendance` with UNIQUE (student_id, attendance_date)
- Foreign key to `student(Student_id)`

"""
from __future__ import annotations
import os
import logging
from datetime import datetime, date
from typing import Optional, Dict, Any, List, Tuple

import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import Error as MySQLError


logger = logging.getLogger(__name__)
if not logger.handlers:
    # Minimal logger setup; projects can override
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def _env_config() -> Dict[str, Any]:
    return {
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', '12345'),
        'database': os.getenv('DB_NAME', 'FaceRecognitionSystem'),
        'auth_plugin': os.getenv('DB_AUTH_PLUGIN', None) or None,
    }


class AttendanceManager:
    """Encapsulates attendance operations and in-memory duplicate prevention.

    Duplicate Prevention Strategy
    -----------------------------
    - Maintains in-memory set for students marked today.
    - Also checks DB uniqueness via UNIQUE(student_id, attendance_date) to guard races.
    - If insert races occur, catches IntegrityError and treats as already-marked.
    """

    def __init__(self, db_config: Optional[Dict[str, Any]] = None,
                 pool_name: str = 'attendance_pool', pool_size: int = 5) -> None:
        self.db_config = db_config or _env_config()
        # Create a connection pool for performance in camera loop
        try:
            self.pool = MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                **{k: v for k, v in self.db_config.items() if v is not None}
            )
        except MySQLError as e:
            logger.error("Failed to create MySQL pool: %s", e)
            raise
        # In-memory cache of student_ids marked on current date
        self._cache_date: date = date.today()
        self._marked_today: set[int] = set()

    def _get_conn(self) -> mysql.connector.MySQLConnection:
        return self.pool.get_connection()

    def _reset_cache_if_new_day(self) -> None:
        today = date.today()
        if today != self._cache_date:
            self._cache_date = today
            self._marked_today.clear()
            logger.debug("Attendance cache reset for new day: %s", today.isoformat())

    def check_attendance_exists(self, student_id: int, attendance_date: Optional[date] = None) -> bool:
        """Check if attendance for student_id exists on attendance_date (default: today)."""
        self._reset_cache_if_new_day()
        d = attendance_date or self._cache_date
        # In-memory short-circuit
        if d == self._cache_date and student_id in self._marked_today:
            return True
        q = (
            "SELECT 1 FROM attendance WHERE student_id = %s AND attendance_date = %s LIMIT 1"
        )
        try:
            conn = self._get_conn()
            cur = conn.cursor()
            cur.execute(q, (student_id, d))
            exists = cur.fetchone() is not None
            cur.close(); conn.close()
            if exists and d == self._cache_date:
                self._marked_today.add(student_id)
            return exists
        except MySQLError as e:
            logger.error("check_attendance_exists error: %s", e)
            return False

    def mark_attendance(self, student_id: int, student_name: str, roll_no: str,
                        detection_confidence: float,
                        status: str = 'Present', marked_by: str = 'System') -> bool:
        """Mark attendance for the given student if not already marked today.

        Returns True if a record was created, False if it already existed or on error.
        Note: LBPH returns a distance (lower is better). We store it as detection_confidence.
        """
        self._reset_cache_if_new_day()
        today = self._cache_date
        if student_id in self._marked_today:
            return False
        # Avoid DB hit when possible
        if self.check_attendance_exists(student_id, today):
            return False
        insert_sql = (
            """
            INSERT INTO attendance (
                student_id, roll_no, student_name, attendance_date, attendance_time,
                status, detection_confidence, marked_by, recognized_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
        )
        now = datetime.now()
        params = (
            student_id,
            roll_no,
            student_name,
            today,
            now.time(),
            status,
            float(detection_confidence),
            marked_by,
            now,
        )
        try:
            conn = self._get_conn()
            cur = conn.cursor()
            cur.execute(insert_sql, params)
            conn.commit()
            cur.close(); conn.close()
            self._marked_today.add(student_id)
            logger.info("Attendance marked: id=%s name=%s date=%s", student_id, student_name, today.isoformat())
            return True
        except mysql.connector.IntegrityError:
            # Unique (student_id, date) violation implies already marked
            logger.debug("Duplicate attendance ignored for id=%s date=%s", student_id, today.isoformat())
            self._marked_today.add(student_id)
            return False
        except MySQLError as e:
            logger.error("mark_attendance error: %s", e)
            return False

    def get_attendance_records(self,
                               student_id: Optional[int] = None,
                               student_name: Optional[str] = None,
                               roll_no: Optional[str] = None,
                               start_date: Optional[date] = None,
                               end_date: Optional[date] = None,
                               sort_by: str = 'attendance_date',
                               sort_dir: str = 'DESC',
                               limit: Optional[int] = 200,
                               offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieve attendance records with filtering, sorting, and pagination.

        - sort_by: one of ['attendance_date','student_name','roll_no','student_id','recognized_at']
        - sort_dir: 'ASC' or 'DESC'
        - Name search uses prefix/contains via LIKE if provided
        """
        valid_sort = {
            'attendance_date': 'attendance_date',
            'student_name': 'student_name',
            'roll_no': 'roll_no',
            'student_id': 'student_id',
            'recognized_at': 'recognized_at',
        }
        sort_col = valid_sort.get(sort_by, 'attendance_date')
        sort_dir = 'ASC' if str(sort_dir).upper() == 'ASC' else 'DESC'

        where: List[str] = []
        params: List[Any] = []
        if student_id is not None:
            where.append('student_id = %s'); params.append(student_id)
        if roll_no:
            where.append('roll_no = %s'); params.append(roll_no)
        if student_name:
            where.append('student_name LIKE %s'); params.append(f"%{student_name}%")
        if start_date:
            where.append('attendance_date >= %s'); params.append(start_date)
        if end_date:
            where.append('attendance_date <= %s'); params.append(end_date)
        where_sql = (' WHERE ' + ' AND '.join(where)) if where else ''

        limit_sql = ''
        if limit is not None:
            limit_sql = ' LIMIT %s OFFSET %s'
            params.extend([int(limit), int(offset)])

        sql = (
            f"SELECT id, student_id, roll_no, student_name, attendance_date, attendance_time, "
            f"status, detection_confidence, marked_by, recognized_at "
            f"FROM attendance{where_sql} ORDER BY {sort_col} {sort_dir}{limit_sql}"
        )
        try:
            conn = self._get_conn()
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            cur.close(); conn.close()
            return rows or []
        except MySQLError as e:
            logger.error("get_attendance_records error: %s", e)
            return []

    def delete_attendance(self, record_id: int) -> bool:
        """Delete a single attendance record by its primary key id.

        Returns True if a row was deleted, False otherwise.
        """
        sql = "DELETE FROM attendance WHERE id = %s"
        try:
            conn = self._get_conn()
            cur = conn.cursor()
            cur.execute(sql, (int(record_id),))
            affected = cur.rowcount
            conn.commit()
            cur.close(); conn.close()
            logger.info("Attendance deleted: id=%s", record_id)
            return affected > 0
        except MySQLError as e:
            logger.error("delete_attendance error: %s", e)
            return False

    def delete_all_attendance(self) -> int:
        """Delete all attendance records.

        Returns the number of rows deleted (0 if none or on error).
        """
        sql = "DELETE FROM attendance"
        try:
            conn = self._get_conn()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            affected = int(cur.rowcount or 0)
            cur.close(); conn.close()
            logger.info("All attendance records deleted: %s", affected)
            return affected
        except MySQLError as e:
            logger.error("delete_all_attendance error: %s", e)
            return 0


# Example integration: importing here for documentation purposes
EXAMPLE_INTEGRATION_SNIPPET = """
from attendance_manager import AttendanceManager

# Inside your face recognition initialization
att_mgr = AttendanceManager()

# Inside your detection loop, when you have (id, name, roll_no, distance)
if distance <= THRESHOLD_DISTANCE:
    att_mgr.mark_attendance(student_id=id, student_name=name, roll_no=roll_no, detection_confidence=distance)
"""
