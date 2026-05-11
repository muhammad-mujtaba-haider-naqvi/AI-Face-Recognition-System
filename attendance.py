from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import csv
from datetime import datetime, date
from attendance_manager import AttendanceManager

class attendance_management:
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def __init__(self, root):
        self.root = root
        self.fullscreen = True 
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.title("Face Recognition System")
        self.root.attributes("-fullscreen", self.fullscreen)
        self.root.bind("<Escape>", self.toggle_fullscreen)

        # Header Setup
        screen_width = self.root.winfo_screenwidth()  # Get Screen Width
        screen_height = self.root.winfo_screenheight()  # Get Screen Height

        # Defining width & Height, so the total = screen_width
        width1 = screen_width // 3
        width2 = screen_width // 3
        width3 = screen_width - (width1 + width2)  # Remaining pixels
        header__height = int(screen_width / 3 / 3.85)  # Common height

        # Image 1
        img1 = Image.open(r"APP Pictures\headerLeft.JPG")
        img1 = img1.resize((width1, header__height), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        lbl1 = Label(self.root, image=self.photoimg1, bd=0)
        lbl1.place(x=0, y=0)

        # Image 2
        img2 = Image.open(r"APP Pictures\headerCentre.png")
        img2 = img2.resize((width2, header__height), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lbl2 = Label(self.root, image=self.photoimg2, bd=0)
        lbl2.place(x=width1, y=0)

        # Image 3 
        img3 = Image.open(r"APP Pictures\headerRight.jpeg")
        img3 = img3.resize((width3, header__height), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        lbl3 = Label(self.root, image=self.photoimg3, bd=0)
        lbl3.place(x=width1 + width2, y=0)

        # DashBoard backGround 
        imgBG = Image.open(r"APP Pictures\backGround.jpg")
        imgBG = imgBG.resize((screen_width, screen_height - header__height), Image.Resampling.LANCZOS)
        self.photoimgBG = ImageTk.PhotoImage(imgBG)
        lblBG = Label(self.root, image=self.photoimgBG, bd=0)
        lblBG.place(x=0, y=header__height)

        # Dashboard Title
        # --- Title Gradient Header Using Canvas ---
        gradient_canvas = Canvas(lblBG, width=screen_width, height=int(screen_height * 0.055), highlightthickness=0)
        gradient_canvas.place(x=0, y=0)
        # Gradient Colors
        start_color = (128, 0, 128)   # 800080 (purple)
        end_color = (255, 0, 0)       # ff0000 (red)
        # Function to Draw Gradient
        def draw_gradient(canvas, width, height, start_rgb, end_rgb):
            r_diff = (end_rgb[0] - start_rgb[0]) / width
            g_diff = (end_rgb[1] - start_rgb[1]) / width
            b_diff = (end_rgb[2] - start_rgb[2]) / width

            for i in range(width):
                r = int(start_rgb[0] + (r_diff * i))
                g = int(start_rgb[1] + (g_diff * i))
                b = int(start_rgb[2] + (b_diff * i))
                color = f"#{r:02x}{g:02x}{b:02x}"
                canvas.create_line(i, 0, i, height, fill=color)
        # Draw the Gradient Background
        draw_gradient(gradient_canvas, screen_width, int(screen_height * 0.06), start_color, end_color)
        # Add Title Text Over Gradient
        gradient_canvas.create_text(
            screen_width // 2,
            int(screen_height * 0.03),
            text="Attendance Management System",
            fill="white",
            font=("times new roman", int(screen_width * 0.017), "bold")
        )

        # === Attendance UI ===
        self.att_mgr = AttendanceManager()

        # Filters & Controls Frame - Professional styling with better spacing
        controls_frame = Frame(lblBG, bg="white", bd=3, relief=GROOVE)
        controls_frame.place(relx=0.025, rely=0.09, width=int(screen_width*0.95), height=int(screen_height*0.20))

        # Title for controls section
        title_label = Label(controls_frame, text="🔍 Search & Filter Attendance Records", 
                           bg="white", fg="#800080", font=("Arial Rounded MT Bold", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=9, pady=(8, 10), sticky=W+E)

        # Configure grid weights for responsive layout
        for i in range(9):
            controls_frame.grid_columnconfigure(i, weight=1)

        # Row 1: Student ID, Roll No, Name
        Label(controls_frame, text="Student ID:", bg="white", fg="#004080", 
              font=("times new roman", 11, "bold")).grid(row=1, column=0, padx=8, pady=6, sticky=W)
        self.var_student_id = StringVar()
        student_id_entry = ttk.Entry(controls_frame, textvariable=self.var_student_id, width=16, font=("times new roman", 10))
        student_id_entry.grid(row=1, column=1, padx=5, pady=6, sticky=W+E)

        Label(controls_frame, text="Roll No:", bg="white", fg="#004080", 
              font=("times new roman", 11, "bold")).grid(row=1, column=2, padx=8, pady=6, sticky=W)
        self.var_roll_no = StringVar()
        roll_entry = ttk.Entry(controls_frame, textvariable=self.var_roll_no, width=16, font=("times new roman", 10))
        roll_entry.grid(row=1, column=3, padx=5, pady=6, sticky=W+E)

        Label(controls_frame, text="Name:", bg="white", fg="#004080", 
              font=("times new roman", 11, "bold")).grid(row=1, column=4, padx=8, pady=6, sticky=W)
        self.var_name = StringVar()
        name_entry = ttk.Entry(controls_frame, textvariable=self.var_name, width=18, font=("times new roman", 10))
        name_entry.grid(row=1, column=5, columnspan=2, padx=5, pady=6, sticky=W+E)

        # Row 2: Date Range
        Label(controls_frame, text="Start Date:", bg="white", fg="#004080", 
              font=("times new roman", 11, "bold")).grid(row=2, column=0, padx=8, pady=6, sticky=W)
        self.var_start_date = StringVar()
        start_entry = ttk.Entry(controls_frame, textvariable=self.var_start_date, width=16, font=("times new roman", 10))
        start_entry.grid(row=2, column=1, padx=5, pady=6, sticky=W+E)

        Label(controls_frame, text="End Date:", bg="white", fg="#004080", 
              font=("times new roman", 11, "bold")).grid(row=2, column=2, padx=8, pady=6, sticky=W)
        self.var_end_date = StringVar()
        end_entry = ttk.Entry(controls_frame, textvariable=self.var_end_date, width=16, font=("times new roman", 10))
        end_entry.grid(row=2, column=3, padx=5, pady=6, sticky=W+E)

        Label(controls_frame, text="(Format: YYYY-MM-DD)", bg="white", fg="gray", 
              font=("times new roman", 9, "italic")).grid(row=2, column=4, columnspan=2, padx=5, pady=6, sticky=W)

        # Row 3: Sort controls
        Label(controls_frame, text="Sort By:", bg="white", fg="#004080", 
              font=("times new roman", 11, "bold")).grid(row=3, column=0, padx=8, pady=6, sticky=W)
        self.sort_by = ttk.Combobox(controls_frame, state="readonly", 
                                    values=["attendance_date","student_name","roll_no","student_id","recognized_at"], 
                                    width=18, font=("times new roman", 10))
        self.sort_by.current(0)
        self.sort_by.grid(row=3, column=1, columnspan=2, padx=5, pady=6, sticky=W+E)

        Label(controls_frame, text="Order:", bg="white", fg="#004080", 
              font=("times new roman", 11, "bold")).grid(row=3, column=3, padx=8, pady=6, sticky=W)
        self.sort_dir = ttk.Combobox(controls_frame, state="readonly", values=["DESC","ASC"], 
                                     width=10, font=("times new roman", 10))
        self.sort_dir.current(0)
        self.sort_dir.grid(row=3, column=4, padx=5, pady=6, sticky=W)

        # Action Buttons Frame - Styled buttons
        btn_frame = Frame(controls_frame, bg="white")
        btn_frame.grid(row=1, column=7, rowspan=3, columnspan=2, padx=10, pady=5, sticky=N+S+E+W)

        search_btn = Button(btn_frame, text="🔍 Search", command=self.search_filter, 
                           font=("Arial Rounded MT Bold", 11, "bold"), bg="#28a745", fg="white", 
                           bd=0, padx=20, pady=8, cursor="hand2", relief=FLAT)
        search_btn.pack(fill=X, pady=4)
        search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#218838"))
        search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#28a745"))

        reset_btn = Button(btn_frame, text="↻ Reset", command=self.reset_filters, 
                          font=("Arial Rounded MT Bold", 11, "bold"), bg="#17a2b8", fg="white", 
                          bd=0, padx=20, pady=8, cursor="hand2", relief=FLAT)
        reset_btn.pack(fill=X, pady=4)
        reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg="#138496"))
        reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg="#17a2b8"))

        export_btn = Button(btn_frame, text="📥 Export CSV", command=self.export_csv, 
                           font=("Arial Rounded MT Bold", 11, "bold"), bg="#007bff", fg="white", 
                           bd=0, padx=20, pady=8, cursor="hand2", relief=FLAT)
        export_btn.pack(fill=X, pady=4)
        export_btn.bind("<Enter>", lambda e: export_btn.config(bg="#0056b3"))
        export_btn.bind("<Leave>", lambda e: export_btn.config(bg="#007bff"))

        delete_btn = Button(btn_frame, text="🗑 Delete Selected", command=self.delete_selected, 
                           font=("Arial Rounded MT Bold", 11, "bold"), bg="#dc3545", fg="white", 
                           bd=0, padx=20, pady=8, cursor="hand2", relief=FLAT)
        delete_btn.pack(fill=X, pady=4)
        delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#c82333"))
        delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#dc3545"))

        clear_all_btn = Button(btn_frame, text="Clear All", command=self.delete_all,
                   font=("Arial Rounded MT Bold", 11, "bold"), bg="#6c757d", fg="white",
                   bd=0, padx=20, pady=8, cursor="hand2", relief=FLAT)
        clear_all_btn.pack(fill=X, pady=4)
        clear_all_btn.bind("<Enter>", lambda e: clear_all_btn.config(bg="#5a6268"))
        clear_all_btn.bind("<Leave>", lambda e: clear_all_btn.config(bg="#6c757d"))

        # Table Frame - Better positioned to avoid overlap
        table_frame = Frame(lblBG, bg="white", bd=3, relief=GROOVE)
        table_frame.place(relx=0.025, rely=0.31, width=int(screen_width*0.95), height=int(screen_height*0.59))

        # Scrollbars
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        
        # Table title bar
        table_title = Label(table_frame, text="📋 Attendance Records", 
                           bg="#f8f9fa", fg="#004080", font=("Arial Rounded MT Bold", 13, "bold"),
                           bd=2, relief=RIDGE, padx=10, pady=8)
        table_title.pack(side=TOP, fill=X)
        
        self.att_table = ttk.Treeview(table_frame,
            columns=("id","student_id","roll_no","student_name","attendance_date","attendance_time","status","detection_confidence","marked_by","recognized_at"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.att_table.xview)
        scroll_y.config(command=self.att_table.yview)

        # Headings with better styling
        for col, text in [
            ("id","ID"),("student_id","Student ID"),("roll_no","Roll No"),("student_name","Name"),
            ("attendance_date","Date"),("attendance_time","Time"),("status","Status"),
            ("detection_confidence","LBPH Dist"),("marked_by","Marked By"),("recognized_at","Recognized At")
        ]:
            self.att_table.heading(col, text=text)
        self.att_table["show"] = "headings"

        # Column widths - optimized for readability
        widths = {
            "id": 60, "student_id": 100, "roll_no": 100, "student_name": 180,
            "attendance_date": 110, "attendance_time": 90, "status": 80,
            "detection_confidence": 90, "marked_by": 100, "recognized_at": 150
        }
        for col, w in widths.items():
            self.att_table.column(col, width=w, anchor=W)
        
        # Alternate row colors for better readability
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                       background="white",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="white",
                       font=("times new roman", 10))
        style.map('Treeview', background=[('selected', '#0078d7')])
        
        self.att_table.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)

        # Data state
        self.current_rows = []
        self.search_filter()  # initial load

        
        # Back Button - Bottom Right Corner
        back_button = Button(
            self.root,
            text="Back",
            command=self.root.destroy,
            font=("times new roman", 13, "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            width=10
        )
        back_button.place(relx=0.95, rely=0.95, anchor="se")  

    def parse_date(self, s: str):
        s = (s or "").strip()
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            messagebox.showerror("Date Error", "Dates must be in YYYY-MM-DD format.", parent=self.root)
            return None

    def search_filter(self):
        student_id = (self.var_student_id.get() or "").strip() or None
        roll_no = (self.var_roll_no.get() or "").strip() or None
        name = (self.var_name.get() or "").strip() or None
        start_d = self.parse_date(self.var_start_date.get())
        end_d = self.parse_date(self.var_end_date.get())
        sort_by = self.sort_by.get()
        sort_dir = self.sort_dir.get()

        # Convert student_id to correct type (varchar kept as str)
        try:
            rows = self.att_mgr.get_attendance_records(
                student_id=student_id,
                student_name=name,
                roll_no=roll_no,
                start_date=start_d,
                end_date=end_d,
                sort_by=sort_by,
                sort_dir=sort_dir,
                limit=500,
                offset=0
            )
        except Exception as e:
            messagebox.showerror("DB Error", f"Failed to load attendance: {e}", parent=self.root)
            return

        self.current_rows = rows
        self.att_table.delete(*self.att_table.get_children())
        for r in rows:
            self.att_table.insert("", END, values=(
                r.get("id"), r.get("student_id"), r.get("roll_no"), r.get("student_name"),
                r.get("attendance_date"), r.get("attendance_time"), r.get("status"),
                r.get("detection_confidence"), r.get("marked_by"), r.get("recognized_at")
            ))

    def reset_filters(self):
        self.var_student_id.set("")
        self.var_roll_no.set("")
        self.var_name.set("")
        self.var_start_date.set("")
        self.var_end_date.set("")
        self.sort_by.set("attendance_date")
        self.sort_dir.set("DESC")
        self.search_filter()

    def export_csv(self):
        if not self.current_rows:
            messagebox.showinfo("Export", "No rows to export.", parent=self.root)
            return
        fpath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files","*.csv"), ("All files","*.*")],
            initialfile=f"attendance_{date.today().isoformat()}.csv",
            title="Save attendance CSV"
        )
        if not fpath:
            return
        try:
            with open(fpath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id","student_id","roll_no","student_name","attendance_date","attendance_time","status","detection_confidence","marked_by","recognized_at"])
                for r in self.current_rows:
                    writer.writerow([
                        r.get("id"), r.get("student_id"), r.get("roll_no"), r.get("student_name"),
                        r.get("attendance_date"), r.get("attendance_time"), r.get("status"),
                        r.get("detection_confidence"), r.get("marked_by"), r.get("recognized_at")
                    ])
            messagebox.showinfo("Export", f"CSV saved: {fpath}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save CSV: {e}", parent=self.root)

    def delete_selected(self):
        sel = self.att_table.selection()
        if not sel:
            messagebox.showinfo("Delete", "Select a row to delete.", parent=self.root)
            return
        # Support deleting multiple selections
        confirm = messagebox.askyesno("Confirm Delete", "Delete selected attendance record(s)?", parent=self.root)
        if not confirm:
            return
        deleted_any = False
        for item in sel:
            vals = self.att_table.item(item, 'values')
            if not vals:
                continue
            rec_id = vals[0]
            try:
                rec_id_int = int(rec_id)
            except Exception:
                continue
            ok = self.att_mgr.delete_attendance(rec_id_int)
            if ok:
                deleted_any = True
                self.att_table.delete(item)
                # Remove from current_rows cache
                self.current_rows = [r for r in self.current_rows if r.get('id') != rec_id_int]
        if deleted_any:
            messagebox.showinfo("Delete", "Selected record(s) deleted.", parent=self.root)
        else:
            messagebox.showinfo("Delete", "No records deleted.", parent=self.root)

    def delete_all(self):
        if not self.current_rows:
            messagebox.showinfo("Delete", "No records to delete.", parent=self.root)
            return
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete ALL attendance records? This cannot be undone.",
            parent=self.root
        )
        if not confirm:
            return
        deleted = self.att_mgr.delete_all_attendance()
        if deleted > 0:
            self.att_table.delete(*self.att_table.get_children())
            self.current_rows = []
            messagebox.showinfo("Delete", f"Deleted {deleted} record(s).", parent=self.root)
        else:
            messagebox.showinfo("Delete", "No records deleted.", parent=self.root)




if __name__ == "__main__":
    root = Tk()
    obj = attendance_management(root)
    root.mainloop()