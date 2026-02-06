-- Attendance table schema for Face Recognition Attendance System
-- Engine: InnoDB; charset: utf8mb4
-- Uniqueness: one record per (student_id, attendance_date)

CREATE TABLE IF NOT EXISTS attendance (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  student_id VARCHAR(50) NOT NULL,
  roll_no VARCHAR(50) NOT NULL,
  student_name VARCHAR(255) NOT NULL,
  attendance_date DATE NOT NULL,
  attendance_time TIME NOT NULL,
  status ENUM('Present','Absent','Late') NOT NULL DEFAULT 'Present',
  detection_confidence DOUBLE NOT NULL,
  marked_by VARCHAR(32) NOT NULL DEFAULT 'System',
  recognized_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uniq_student_date (student_id, attendance_date),
  KEY idx_date (attendance_date),
  KEY idx_student (student_id),
  KEY idx_roll (roll_no),
  CONSTRAINT fk_attendance_student
    FOREIGN KEY (student_id) REFERENCES student (Student_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;