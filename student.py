from importlib.resources import contents
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector  
import cv2


class student:
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
        screen_width = self.root.winfo_screenwidth() #Get Screen Width
        screen_height = self.root.winfo_screenheight() #Get Screen Height

        # Defining width & Height, so the total = screen_width
        width1 = screen_width // 3
        width2 = screen_width // 3
        width3 = screen_width - (width1 + width2)  # Remaining pixels
        header__height = int(screen_width / 3 / 3.85) # Common height

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
        start_color = (128, 0, 128)   #800080 (purple)
        end_color = (255, 0, 0)       #ff0000 (red)
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
            text="STUDENT MANAGEMENT SYSTEM",
            fill="white",
            font=("Arial Rounded MT Bold", int(screen_width * 0.017), "bold")
        )

         # =================Entry Variables====================
        self.var_dept = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_stdID = StringVar()
        self.var_stdName = StringVar()
        self.var_div = StringVar()
        self.var_rollNO = StringVar()
        self.var_gender = StringVar()
        self.var_DOB = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_radioBTN1 = StringVar()

        #Student Management Frame
        #Frame Size
        frame_width = int(screen_width * 0.96)                               # 96% of screen width
        frame_height = int(screen_height * 0.76)                             # 71% of screen height
        frame_x = int(screen_width * 0.02)                                   # 2% from the left
        frame_y = int(screen_height * 0.07)                                  # 10% from the top (below title bar)
        #Frame
        main_frame = Frame(lblBG, bd=2, bg="white")
        main_frame.place(x=frame_x, y=frame_y, width=frame_width, height=frame_height)

        # --- Left & Right Label Frames:
        # Sizes and positions relative to main_frame
        label_frame_padding = int(frame_width * 0.012)                       # padding between edge and frame
        label_frame_width = int((frame_width - (3 * label_frame_padding)) / 2)
        label_frame_height = int(frame_height - 2 * label_frame_padding)
        label_frame_y = label_frame_padding + 10

        # Left Label Frame
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details",
                                font=("times new roman", 12, "bold"))
        left_frame.place(x=label_frame_padding, y=label_frame_y, width=label_frame_width, height=label_frame_height)
        # Left Frame Header Image
        left_header_img_width = int(label_frame_width * 0.973)                    # 97.3% of label frame width
        header_img_height = int(label_frame_height * 0.20)                   # 20% of label frame height
        imgLF = Image.open(r"APP Pictures\headerLeft.JPG")
        imgLF = imgLF.resize((left_header_img_width, header_img_height), Image.Resampling.LANCZOS)
        self.photoimgLF = ImageTk.PhotoImage(imgLF)
        lblLF = Label(left_frame, image=self.photoimgLF)
        lblLF.place(x=int(label_frame_width * 0.01), y=0)                    # small padding from left edge

        # Current Course Frame 
        course_frame_x = int(label_frame_width * 0.01)                       # 1% padding from left
        course_frame_y = header_img_height + int(label_frame_height * 0.02)  # below header image with 2% padding
        course_frame_width = int(label_frame_width * 0.975)                  # 97.5% of left frame width
        course_frame_height = int(label_frame_height * 0.19)                 # 19% of left frame height
        current_course_frame = LabelFrame(left_frame,bd=2,bg="white",relief=RIDGE,
            text="Current Course Information", font=("times new roman", 12, "bold"))
        current_course_frame.place(x=course_frame_x, y=course_frame_y, width=course_frame_width, height=course_frame_height)

        # ComBoxes Inside Course Frame
        # Size and Positioning:
        for i in range(4):  # 4 columns
            current_course_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):  # 2 rows
            current_course_frame.grid_rowconfigure(i, weight=0)
        # Department
        department_label = Label(current_course_frame, bd=2, bg="white", text="Department", font=("times new roman", 12, "bold"))
        department_label.grid(row=0, column=0, padx=5,pady=5, sticky=W)
        department_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dept, font=("times new roman", 12, "bold"), state="readonly", width=18)
        department_combo["values"] = (
            "Select Department", "Architecture and Design", "Chemical Engineering", "Computer Sciences", 
            "Electrical Engineering", "Humanities", "Management Sciences", "Mathematics", "Physics")
        department_combo.current(0)
        department_combo.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        # Course
        course_label = Label(current_course_frame, bd=2, bg="white", text="Course", font=("times new roman", 12, "bold"))
        course_label.grid(row=0, column=2, padx=5,pady=5, sticky=W)
        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=("times new roman", 12, "bold"), state="readonly", width=18)
        course_combo["values"] = (
            "Select Course", "Programming Fundamentals", "Data Structures & Algorithms", "Digital Logic Design", 
            "Artificial Intelligence", "Marketing Management", "Human Resource Management", "English Literature",
            "Applied Physics", "Analytical Geometry", "Engineering Mechanics")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=5, pady=5, sticky=W)
        # Semester
        semester_label = Label(current_course_frame, bd=2, bg="white", text="Semester", font=("times new roman", 12, "bold"))
        semester_label.grid(row=1, column=0, padx=5,pady=5, sticky=W)
        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=("times new roman", 12, "bold"), state="readonly", width=18)
        semester_combo["values"] = (
            "Select Semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        # Year
        year_label = Label(current_course_frame, bd=2, bg="white", text="Year", font=("times new roman", 12, "bold"))
        year_label.grid(row=1, column=2, padx=5,pady=5, sticky=W)
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=("times new roman", 12, "bold"), state="readonly", width=18)
        year_combo["values"] = (
            "Select Year", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25")
        year_combo.current(0)
        year_combo.grid(row=1, column=3, padx=5, pady=5, sticky=W)

        # Class Student Informatoin Frame 
        class_student_frame_x = int(label_frame_width * 0.01)                       # 1% padding from left
        class_student_frame_y = header_img_height + int(label_frame_height * 0.23)  # below header image with 23% padding
        class_student_frame_width = int(label_frame_width * 0.975)                  # 97.5% of left frame width
        class_student_frame_height = int(label_frame_height * 0.5266)               # 52.66% of left frame height

        class_student_frame = LabelFrame(left_frame,bd=2,bg="white",relief=RIDGE,
            text="Class Student Information", font=("times new roman", 12, "bold"))
        class_student_frame.place(x=class_student_frame_x, y=class_student_frame_y, width=class_student_frame_width, 
                                  height=class_student_frame_height)
        
        # Size & Position Of Components
        for i in range(4):  # 4 columns
            class_student_frame.columnconfigure(i, weight=1)
        for i in range(5):  # 5 rows
            class_student_frame.rowconfigure(i, weight=0)  # fixed height rows
            
        # Student ID
        studentID_label = Label(class_student_frame, bd=2, bg="white", text="Student ID:", font=("times new roman", 12, "bold"))
        studentID_label.grid(row=0, column=0, padx=4, pady=4, sticky=W)
        studentID_entry = ttk.Entry(class_student_frame, textvariable=self.var_stdID, width=20, font=("times new roman", 12, "bold"))
        studentID_entry.grid(row=0, column=1, padx=4, pady=4, sticky=W)
        # Student Name
        student_name_label = Label(class_student_frame, bd=2, bg="white", text="Name:", font=("times new roman", 12, "bold"))
        student_name_label.grid(row=0, column=2, padx=4, pady=4, sticky=W)
        student_name_entry = ttk.Entry(class_student_frame, textvariable=self.var_stdName, width=20, font=("times new roman", 12, "bold"))
        student_name_entry.grid(row=0, column=3, padx=4, pady=4, sticky=W)
        # Class Division
        class_division_label = Label(class_student_frame, bd=2, bg="white", text="Class Division:", font=("times new roman", 12, "bold"))
        class_division_label.grid(row=1, column=0, padx=4, pady=4, sticky=W)
        class_division_combo = ttk.Combobox(class_student_frame, textvariable=self.var_div, font=("times new roman", 12, "bold"), state="readonly", width=18)
        class_division_combo["values"] = ("Select Division", "A", "B", "C","D")
        class_division_combo.current(0)
        class_division_combo.grid(row=1, column=1, padx=4, pady=4, sticky=W)
        # Roll No
        roll_no_label = Label(class_student_frame, bd=2, bg="white", text="Roll No:", font=("times new roman", 12, "bold"))
        roll_no_label.grid(row=1, column=2, padx=4, pady=4, sticky=W)
        roll_no_entry = ttk.Entry(class_student_frame, textvariable=self.var_rollNO, width=20, font=("times new roman", 12, "bold"))
        roll_no_entry.grid(row=1, column=3, padx=4, pady=4, sticky=W)
        # Gender
        gender_label = Label(class_student_frame, bd=2, bg="white", text="Gender:", font=("times new roman", 12, "bold"))
        gender_label.grid(row=2, column=0, padx=4, pady=4, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender, font=("times new roman", 12, "bold"), state="readonly", width=18)
        gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=4, pady=4, sticky=W)
        # Date of Birth
        dob_label = Label(class_student_frame, bd=2, bg="white", text="DOB:", font=("times new roman", 12, "bold"))
        dob_label.grid(row=2, column=2, padx=4, pady=4, sticky=W)
        dob_entry = ttk.Entry(class_student_frame, textvariable=self.var_DOB, width=20, font=("times new roman", 12, "bold"))
        dob_entry.grid(row=2, column=3, padx=4, pady=4, sticky=W)
        # Email
        email_label = Label(class_student_frame, bd=2, bg="white", text="Email:", font=("times new roman", 12, "bold"))
        email_label.grid(row=3, column=0, padx=4, pady=4, sticky=W)
        email_entry = ttk.Entry(class_student_frame, textvariable=self.var_email, width=20, font=("times new roman", 12, "bold"))
        email_entry.grid(row=3, column=1, padx=4, pady=4, sticky=W)
        # Phone No
        phone_label = Label(class_student_frame, bd=2, bg="white", text="Phone No:", font=("times new roman", 12, "bold"))
        phone_label.grid(row=3, column=2, padx=4, pady=4, sticky=W)
        phone_entry = ttk.Entry(class_student_frame, textvariable=self.var_phone, width=20, font=("times new roman", 12, "bold"))
        phone_entry.grid(row=3, column=3, padx=4, pady=4, sticky=W)
        # Address
        address_label = Label(class_student_frame, bd=2, bg="white", text="Address:", font=("times new roman", 12, "bold"))
        address_label.grid(row=4, column=0, padx=4, pady=4, sticky=W)
        address_entry = ttk.Entry(class_student_frame, textvariable=self.var_address, width=20, font=("times new roman", 12, "bold"))
        address_entry.grid(row=4, column=1, padx=4, pady=4, sticky=W)
        # Teacher Name
        teacher_label = Label(class_student_frame, bd=2, bg="white", text="Teacher Name:", font=("times new roman", 12, "bold"))
        teacher_label.grid(row=4, column=2, padx=4, pady=4, sticky=W)
        teacher_entry = ttk.Entry(class_student_frame, textvariable=self.var_teacher, width=20, font=("times new roman", 12, "bold"))
        teacher_entry.grid(row=4, column=3, padx=4, pady=4, sticky=W)

        # Radio Buttons in Student Information:
        radioBTN1 = StringVar(value="no")  # Store the selected value (yes or no)
        # Take Photo Sample
        radio_button_TPS = ttk.Radiobutton( class_student_frame,
            text="Take Photo Sample",
            variable=self.var_radioBTN1,   # this stores the selected value
            value="yes"
        )
        radio_button_TPS.grid(row=5, column=1, padx=1, pady=1, sticky=W)
        # Without Photo Sample
        radio_button_NPS = ttk.Radiobutton(
            class_student_frame,
            text="Without Photo Sample",
            variable=self.var_radioBTN1,
            value="no"
        )
        radio_button_NPS.grid(row=5, column=3, padx=1, pady=1, sticky=W)

        #upper Footer Button frames:
        # Size  
        upper_footer_button_frame_x = int(label_frame_width * 0.005)                      # 0.5% padding from left
        upper_footer_button_frame_y = header_img_height + int(label_frame_height * 0.16)  # below header image with 16% padding
        upper_footer_button_frame_width = int(label_frame_width * 0.961)                  # 96.1% of left frame width
        upper_footer_button_frame_height = int(label_frame_height * 0.065)                # 6.5% of left frame height
        #Position
        upper_footer_button_frame = LabelFrame(class_student_frame,bd=2,bg="white",relief=RIDGE)
        upper_footer_button_frame.place(x=upper_footer_button_frame_x, y=upper_footer_button_frame_y, 
                                    width=upper_footer_button_frame_width, height=upper_footer_button_frame_height)
        
        #Buttons:
        #Save Button
        save_button = Button(upper_footer_button_frame, text="Save", command=self.add_data, width=int(upper_footer_button_frame_width*0.028), 
                            font=("times new roman", 12, "bold"), bg="green", fg="white")
        save_button.grid(row=0,column=0)
        #Update Button
        update_button = Button(upper_footer_button_frame, text="Update", command=self.update_data, width=int(upper_footer_button_frame_width*0.028), 
                            font=("times new roman", 12, "bold"), bg="green", fg="white")
        update_button.grid(row=0,column=1)
        #delete Button
        delete_button = Button(upper_footer_button_frame, text="Delete", command=self.delete_data_BF, width=int(upper_footer_button_frame_width*0.028), 
                            font=("times new roman", 12, "bold"), bg="green", fg="white")
        delete_button.grid(row=0,column=2)
        #Reset Button
        reset_button = Button(upper_footer_button_frame, text="Reset", command=self.reset_data, width=int(upper_footer_button_frame_width*0.028), 
                            font=("times new roman", 12, "bold"), bg="green", fg="white")
        reset_button.grid(row=0,column=3)

        #Lower Footer Button frames:
        # Size  
        loweer_footer_button_frame_x = int(label_frame_width * 0.005)                      # 0.5% padding from left
        loweer_footer_button_frame_y = header_img_height + int(label_frame_height * 0.22)  # below header image with 16% padding
        loweer_footer_button_frame_width = int(label_frame_width * 0.961)                  # 96.1% of left frame width
        loweer_footer_button_frame_height = int(label_frame_height * 0.06)                 # 6% of left frame height
        #Position
        loweer_footer_button_frame = LabelFrame(class_student_frame,bd=2,bg="white",relief=RIDGE)
        loweer_footer_button_frame.place(x=loweer_footer_button_frame_x, y=loweer_footer_button_frame_y, 
                                    width=loweer_footer_button_frame_width, height=loweer_footer_button_frame_height)
        #Take Photo Sample Button
        reset_button = Button(loweer_footer_button_frame, text="Take Photo Sample",command=self.generate_face_dataset,
                            width=int(upper_footer_button_frame_width*0.056), font=("times new roman", 12, "bold"), 
                            bg="green", fg="white")
        reset_button.grid(row=0,column=0)
        #Update Photo Sample Button
        reset_button = Button(loweer_footer_button_frame, text="Update Photo Sample",command=self.generate_face_dataset, width=int(upper_footer_button_frame_width*0.056), 
                            font=("times new roman", 12, "bold"), bg="green", fg="white")
        reset_button.grid(row=0,column=1)


        # Right Label Frame
        right_frame = LabelFrame(main_frame ,bd=2, bg="white", relief=RIDGE, text="Student Details", 
                                 font=("times new roman", 13, "bold"))
        right_frame.place(x=label_frame_padding * 2 + label_frame_width, y=label_frame_y,
                          width=label_frame_width, height=label_frame_height)
        # Right Frame Header Image
        right_header_img_width = int(label_frame_width * 0.973)                    # 97.3% of label frame width
        header_img_height = int(label_frame_height * 0.20)                         # 20% of label frame height
        imgRF = Image.open(r"APP Pictures\headerLeft.JPG")
        imgRF = imgRF.resize((right_header_img_width, header_img_height), Image.Resampling.LANCZOS)
        self.photoimgRF = ImageTk.PhotoImage(imgRF)
        lblRF = Label(right_frame, image=self.photoimgRF)
        lblRF.place(x=int(label_frame_width * 0.01), y=0)                          # small padding from left edge

        #=========Search System=========
        # Search System Frame:
        search_frame_x = int(label_frame_width * 0.01)                       # 1% padding from left
        search_frame_y = header_img_height + int(label_frame_height * 0.02)  # below header image with 2% padding
        search_frame_width = int(label_frame_width * 0.975)                  # 97.5% of left frame width
        search_frame_height = int(label_frame_height * 0.11)                 # 11% of left frame height
        search_frame = LabelFrame(right_frame,bd=2,bg="white",relief=RIDGE,
            text="Search System", font=("times new roman", 12, "bold"))
        search_frame.place(x=search_frame_x, y=search_frame_y, width=search_frame_width, height=search_frame_height)
        #Search By label
        searchBY_label = Label(search_frame, bd=2, bg="red",fg="white", text="Search By:", font=("times new roman", 13, "bold"))
        searchBY_label.grid(row=0, column=0, padx=5,pady=5, sticky=W)
        #Search By Combo
        searchBY_combo = ttk.Combobox(search_frame, font=("times new roman", 12, "bold"), state="readonly", width=15)
        searchBY_combo["values"] = ( "Select Method", "Roll No", "Phone Number","CNIC")
        searchBY_combo.current(0)
        searchBY_combo.grid(row=0, column=1, padx=4, pady=5, sticky=W)
        #Search By Entry Field
        search_entry = ttk.Entry(search_frame, width=15, font=("times new roman", 12, "bold"))
        search_entry.grid(row=0, column=2, padx=3, pady=4, sticky=W)
        #Search Button
        search_button = Button(search_frame, text="Search", width=int(search_frame_width*0.019), 
                            font=("times new roman", 11), bg="green", fg="white")
        search_button.grid(row=0,column=3,padx=3)
        #Show All Button
        showAll_button = Button(search_frame, text="Show ALL", width=int(search_frame_width*0.019), 
                            font=("times new roman", 11), bg="green", fg="white")
        showAll_button.grid(row=0,column=4,padx=1)

        # Table Frame 
        table_frame_x = int(label_frame_width * 0.01)                       # 1% padding from left
        table_frame_y = header_img_height + int(label_frame_height * 0.14)  # below header image with 14% padding
        table_frame_width = int(label_frame_width * 0.975)                  # 97.5% of left frame width
        table_frame_height = int(label_frame_height * 0.615)               # 52.66% of left frame height

        table_frame = Frame(right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=table_frame_x, y=table_frame_y, width=table_frame_width, 
                                  height=table_frame_height)
        #Scroll Bars 
        scroll_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame,orient=VERTICAL)
        #Table
        self.student_table = ttk.Treeview(table_frame,  # or whatever parent widget you're using
            columns=("dep", "course", "year", "sem", "id", "name", "div","roll" ,"gender", "dob",
                    "email", "phone", "address", "teacher", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.student_table.yview)
        # Show Header Headings 
        self.student_table.heading("dep", text="Department") 
        self.student_table.heading("course", text="Course") 
        self.student_table.heading("year", text="Year") 
        self.student_table.heading("sem", text="Semester") 
        self.student_table.heading("id", text="Student_ID") 
        self.student_table.heading("name", text="Name") 
        self.student_table.heading("div", text="Division") 
        self.student_table.heading("roll", text="Roll No") 
        self.student_table.heading("gender", text="Gender") 
        self.student_table.heading("dob", text="D.O.B") 
        self.student_table.heading("email", text="@Email") 
        self.student_table.heading("phone", text="Phone") 
        self.student_table.heading("address", text="Address") 
        self.student_table.heading("teacher", text="Teacher") 
        self.student_table.heading("photo", text="Photo_Sample_Status") 
        #Header: Show & Width Setting
        self.student_table["show"] = "headings"
        self.student_table.column("dep",width=100)
        self.student_table.column("course",width=100)
        self.student_table.column("year",width=100)
        self.student_table.column("sem",width=100)
        self.student_table.column("id",width=100)
        self.student_table.column("name",width=100)
        self.student_table.column("div",width=100)
        self.student_table.column("roll",width=100)
        self.student_table.column("gender",width=100)
        self.student_table.column("dob",width=100)
        self.student_table.column("email",width=100)
        self.student_table.column("phone",width=100)
        self.student_table.column("address",width=100)
        self.student_table.column("teacher",width=100)
        self.student_table.column("photo",width=100)
        #Settle All
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor_data)
        self.fetch_data()

    # ===== Back Button - Bottom Right Corner =====
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
        back_button.place(relx=0.97, rely=0.225, anchor="ne")  # Top-right corner



    # =======================Data Manipulation/Button Functions==========================
    #Data Addition to DB
    def add_data(self):
        if (
            self.var_dept.get() == "Select Department" or
            self.var_course.get() == "Select Course" or
            self.var_year.get() == "Select Year" or
            self.var_semester.get() == "Select Semester" or
            self.var_stdID.get() == "" or
            self.var_stdName.get() == "" or
            self.var_div.get() == "Select Division" or
            self.var_rollNO.get() == "" or
            self.var_gender.get() == "Select Gender" or
            self.var_DOB.get() == "" or
            self.var_email.get() == "" or
            self.var_phone.get() == "" or
            self.var_address.get() == "" or
            self.var_teacher.get() == ""):
            messagebox.showerror("Error","All Fields are required", parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="127.0.0.1",username="root",password="12345",
                                            database="FaceRecognitionSystem")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                    self.var_dept.get(),
                                    self.var_course.get(),
                                    self.var_year.get(),
                                    self.var_semester.get(),
                                    self.var_stdID.get(),
                                    self.var_stdName.get(),
                                    self.var_div.get(),
                                    self.var_rollNO.get(),
                                    self.var_gender.get(),
                                    self.var_DOB.get(),
                                    self.var_email.get(),
                                    self.var_phone.get(),
                                    self.var_address.get(),
                                    self.var_teacher.get(),
                                    self.var_radioBTN1.get()
                                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Student Details Have been added Successfully",
                                    parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To: {str(es)}",parent = self.root)

    #Fetching Data into Table from DataBase
    def fetch_data(self):
        conn=mysql.connector.connect(host="127.0.0.1",username="root",password="12345",
                                            database="FaceRecognitionSystem")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    #Get Cursor Data(Select Data from Right Table through Cursor) 
    def get_cursor_data(self,event=""):
        cursor_focus = self.student_table.focus()
        content_table = self.student_table.item(cursor_focus)
        data = content_table["values"]

        self.var_dept.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_stdID.set(data[4]),
        self.var_stdName.set(data[5]),
        self.var_div.set(data[6]),
        self.var_rollNO.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_DOB.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_teacher.set(data[13]),
        self.var_radioBTN1.set(data[14])
    
    # Data(OF DB) Update Button Function
    def update_data(self):
        if (
            self.var_dept.get() == "Select Department" or
            self.var_course.get() == "Select Course" or
            self.var_year.get() == "Select Year" or
            self.var_semester.get() == "Select Semester" or
            self.var_stdID.get() == "" or
            self.var_stdName.get() == "" or
            self.var_div.get() == "Select Division" or
            self.var_rollNO.get() == "" or
            self.var_gender.get() == "Select Gender" or
            self.var_DOB.get() == "" or
            self.var_email.get() == "" or
            self.var_phone.get() == "" or
            self.var_address.get() == "" or
            self.var_teacher.get() == ""):
            messagebox.showerror("Error","All Fields are required", parent=self.root)
        else:
            try:
                update = messagebox.askyesno("Update data","Do you want to update selected student details",
                                             parent = self.root)
                if update>0:
                    conn=mysql.connector.connect(host="127.0.0.1",username="root",password="12345",
                                            database="FaceRecognitionSystem")
                    my_cursor = conn.cursor()
                    my_cursor.execute("update student set Department=%s, Course=%s, Year=%s, Semester=%s, Name=%s, Division=%s, Roll_No = %s, Gender=%s, DOB=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s, PhotoSample=%s where Student_id = %s",
                                      (
                                        self.var_dept.get(),
                                        self.var_course.get(),
                                        self.var_year.get(),
                                        self.var_semester.get(),
                                        self.var_stdName.get(),
                                        self.var_div.get(),
                                        self.var_rollNO.get(),
                                        self.var_gender.get(),
                                        self.var_DOB.get(),
                                        self.var_email.get(),
                                        self.var_phone.get(),
                                        self.var_address.get(),
                                        self.var_teacher.get(),
                                        self.var_radioBTN1.get(),
                                        self.var_stdID.get()))
                else:
                    if not update:
                        return
                messagebox.showinfo("Success,","Student Details Successfully Updated", parent = self.root)
                conn.commit()
                self.fetch_data()
                conn.close
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    #Delete Button Function
    def delete_data_BF(self):
        if self.var_stdID.get()=="":
            messagebox.showerror("Error","Student ID Must Be Selected", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Student Delete Page", "Do you want to delete this studdent",
                                             parent=self.root)
                if delete>0:
                    conn=mysql.connector.connect(host="127.0.0.1",username="root",password="12345",
                                            database="FaceRecognitionSystem")
                    my_cursor = conn.cursor()
                    my_cursor.execute("delete from student where Student_id=%s",(self.var_stdID.get(),))
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Deleted", " Student Details Deleted Successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    #Reset Button Function
    def reset_data(self):
        self.var_dept.set("Select Department"),
        self.var_course.set("Select Course"),
        self.var_year.set("Select Year"),
        self.var_semester.set("Select Semester",),
        self.var_stdID.set(""),
        self.var_stdName.set(""),
        self.var_div.set("Select Division"),
        self.var_rollNO.set(""),
        self.var_gender.set("Select Gender"),
        self.var_DOB.set(""),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_address.set(""),
        self.var_teacher.set(""),
        self.var_radioBTN1.set("")
 

    #============================Face Related/Button Functions======================
    def generate_face_dataset(self):
        if (
            self.var_dept.get() == "Select Department" or
            self.var_course.get() == "Select Course" or
            self.var_year.get() == "Select Year" or
            self.var_semester.get() == "Select Semester" or
            self.var_stdID.get() == "" or
            self.var_stdName.get() == "" or
            self.var_div.get() == "Select Division" or
            self.var_rollNO.get() == "" or
            self.var_gender.get() == "Select Gender" or
            self.var_DOB.get() == "" or
            self.var_email.get() == "" or
            self.var_phone.get() == "" or
            self.var_address.get() == "" or
            self.var_teacher.get() == ""):
            messagebox.showerror("Error","All Fields are required", parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="127.0.0.1",username="root",password="12345",
                                            database="FaceRecognitionSystem")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                my_result=my_cursor.fetchall()
                id=0
                for x in my_result:
                    id+=1
                my_cursor.execute("update student set Department=%s, Course=%s, Year=%s, Semester=%s, Name=%s, Division=%s, Roll_No = %s, Gender=%s, DOB=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s, PhotoSample=%s where Student_id = %s",
                                      (
                                        self.var_dept.get(),
                                        self.var_course.get(),
                                        self.var_year.get(),
                                        self.var_semester.get(),
                                        self.var_stdName.get(),
                                        self.var_div.get(),
                                        self.var_rollNO.get(),
                                        self.var_gender.get(),
                                        self.var_DOB.get(),
                                        self.var_email.get(),
                                        self.var_phone.get(),
                                        self.var_address.get(),
                                        self.var_teacher.get(),
                                        self.var_radioBTN1.get(),
                                        self.var_stdID.get()==id+1
                                        ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                # =======Load PreDefined Frontal Face Date from Open-CV2(Built in Algorithm)======
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                #Image Cropping and grescaling Function
                def face_cropped(img):
                    grey_scale_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(grey_scale_img,1.3,5)
                    for (x,y,w,h) in faces:
                        face_cropped = img[y:y+h,x:x+w]
                        return face_cropped
                    
                cap_cam = cv2.VideoCapture(0)
                img_id = 0
                while True:
                    ret,my_frame = cap_cam.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        face = cv2.resize(face_cropped(my_frame),(450,450))
                        face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path = "face_data/user."+str(id)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Cropped Face",face)
                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                    
                cap_cam.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Data Set Generated Completed:")

            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = student(root)
    root.mainloop()