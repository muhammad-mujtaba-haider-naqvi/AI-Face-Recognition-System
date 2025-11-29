import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  
from student import student
from face_recognition import face_recognition
from attendance import attendance_management
from train import train
from developer import developer
from helpdesk import helpdesk

class Face_Recognition_System:
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
        gradient_canvas = Canvas(lblBG, width=screen_width, height=int(screen_height * 0.06), highlightthickness=0)
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
            text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE",
            fill="white",
            font=("Arial Rounded MT Bold", int(screen_width * 0.017), "bold")
        )

        #Buttons:
        btn_width, btn_height = 180, 180

        # Student Button 
        studentBtn = Image.open(r"APP Pictures\studentBtn.jpeg")
        studentBtn = studentBtn.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        self.photostudentBtn = ImageTk.PhotoImage(studentBtn)
        btn1 = Button(lblBG, image=self.photostudentBtn, command=self.student_details, cursor="hand2", bd=0, highlightthickness=0)
        btn1.place(x=int(screen_width * 0.140), y=int(screen_height * 0.12), width=btn_width, height=btn_height)
        btn1_1 = Button(lblBG, text="Student Details", command=self.student_details, cursor="hand2", # Text Button At Bottom of Student Button
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff")
        btn1_1.place(x=int(screen_width * 0.140), y=int(screen_height * 0.12) + btn_height - 1, width=btn_width, height=40)

        # Face Detect Button 
        facedetectBtn = Image.open(r"APP Pictures\facedetectBtn.jpg")
        facedetectBtn = facedetectBtn.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        self.facedetectBtn = ImageTk.PhotoImage(facedetectBtn)
        btn2 = Button(lblBG, image=self.facedetectBtn, cursor="hand2", command=self.face_recognition, bd=0, highlightthickness=0)
        btn2.place(x=int(screen_width * 0.340), y=int(screen_height * 0.12), width=btn_width, height=btn_height)
        btn2_2 = Button(lblBG, text="Face Detector", cursor="hand2", command=self.face_recognition, # Text Button At Bottom of Student Button
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff")
        btn2_2.place(x=int(screen_width * 0.340), y=int(screen_height * 0.12) + btn_height - 1, width=btn_width, height=40)

        # Attendance Button 
        attendanceBtn = Image.open(r"APP Pictures\attendanceBtn.jpg")
        attendanceBtn = attendanceBtn.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        self.attendanceBtn = ImageTk.PhotoImage(attendanceBtn)
        btn3 = Button(lblBG, image=self.attendanceBtn, cursor="hand2", command=self.attendance_management, bd=0, highlightthickness=0)
        btn3.place(x=int(screen_width * 0.540), y=int(screen_height * 0.12), width=btn_width, height=btn_height)
        btn3_3 = Button(lblBG, text="ATTENDANCE", cursor="hand2", command=self.attendance_management, # Text Button At Bottom of Student Button
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff")
        btn3_3.place(x=int(screen_width * 0.540), y=int(screen_height * 0.12) + btn_height - 1, width=btn_width, height=40)

        # TRAINDATA Button 
        trainDataBtn = Image.open(r"APP Pictures\trainDataBtn.jpg")
        trainDataBtn = trainDataBtn.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        self.trainDataBtn = ImageTk.PhotoImage(trainDataBtn)
        btn4 = Button(lblBG, image=self.trainDataBtn, cursor="hand2", command=self.train_data, bd=0, highlightthickness=0)
        btn4.place(x=int(screen_width * 0.740), y=int(screen_height * 0.12), width=btn_width, height=btn_height)
        btn4_4 = Button(lblBG, text="TRAIN DATA", cursor="hand2", command=self.train_data, # Text Button At Bottom of Student Button
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff")
        btn4_4.place(x=int(screen_width * 0.740), y=int(screen_height * 0.12) + btn_height - 1, width=btn_width, height=40)

        # PhotoGallery Button 
        photoGalleryBtn = Image.open(r"APP Pictures\photoGalleryBtn.jpg")
        photoGalleryBtn = photoGalleryBtn.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        self.photoGalleryBtn = ImageTk.PhotoImage(photoGalleryBtn)
        btn5 = Button(lblBG, image=self.photoGalleryBtn, cursor="hand2", command=self.open_face_data_imgs, bd=0, highlightthickness=0)
        btn5.place(x=int(screen_width * 0.140), y=int(screen_height * 0.5), width=btn_width, height=btn_height)
        btn5_5 = Button(lblBG, text="PHOTOS", cursor="hand2", command=self.open_face_data_imgs, # Text Button At Bottom of Student Button
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff")
        btn5_5.place(x=int(screen_width * 0.140), y=int(screen_height * 0.5) + btn_height - 1, width=btn_width, height=40)

        # Developer Details Button 
        developerDetailBtn = Image.open(r"APP Pictures\developerDetailBtn.jpg")
        developerDetailBtn = developerDetailBtn.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        self.developerDetailBtn = ImageTk.PhotoImage(developerDetailBtn)
        btn6 = Button(lblBG, image=self.developerDetailBtn, cursor="hand2", command=self.developer_information, bd=0, highlightthickness=0)
        btn6.place(x=int(screen_width * 0.340), y=int(screen_height * 0.5), width=btn_width, height=btn_height)
        btn6_6 = Button(lblBG, text="DEVELOPER", cursor="hand2", command=self.developer_information, # Text Button At Bottom of Student Button
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff")
        btn6_6.place(x=int(screen_width * 0.340), y=int(screen_height * 0.5) + btn_height - 1, width=btn_width, height=40)

        # Help Desk Button 
        helpDeskBtn = Image.open(r"APP Pictures\helpDeskBtn.jpg")
        helpDeskBtn = helpDeskBtn.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        self.helpDeskBtn = ImageTk.PhotoImage(helpDeskBtn)
        btn7 = Button(lblBG, image=self.helpDeskBtn, cursor="hand2", command=self.helpdesk, bd=0, highlightthickness=0)
        btn7.place(x=int(screen_width * 0.540), y=int(screen_height * 0.5), width=btn_width, height=btn_height)
        btn7_7 = Button(lblBG, text="HELP DESK", cursor="hand2", command=self.helpdesk, # Text Button At Bottom of Student Button
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff")
        btn7_7.place(x=int(screen_width * 0.540), y=int(screen_height * 0.5) + btn_height - 1, width=btn_width, height=40)

        # Exit Button 
        exitBtn = Image.open(r"APP Pictures\exitBtn.jpg")
        exitBtn = exitBtn.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        self.exitBtn = ImageTk.PhotoImage(exitBtn)
        btn8 = Button(lblBG, image=self.exitBtn, cursor="hand2", command=self.exit_app, bd=0, highlightthickness=0)
        btn8.place(x=int(screen_width * 0.740), y=int(screen_height * 0.5), width=btn_width, height=btn_height)
        btn8_8 = Button(lblBG, text="EXIT", cursor="hand2", command=self.exit_app,
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff",)
        btn8_8.place(x=int(screen_width * 0.740), y=int(screen_height * 0.5) + btn_height - 1, width=btn_width, height=40)
    
    
    # ========================Button Functions========================
    #Student Button:
    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = student(self.new_window)

    #Face Recognisor Button:
    def face_recognition(self):
        self.new_window = Toplevel(self.root)
        self.app = face_recognition(self.new_window)
    
    #Train Data Button:
    def attendance_management(self):
        self.new_window = Toplevel(self.root)
        self.app = attendance_management(self.new_window)

    #Train Data Button:
    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = train(self.new_window)

    #open Face Data Gallery:
    def open_face_data_imgs(self):
        os.startfile("face_data")

    #open Developer Information :
    def developer_information(self):
        self.new_window = Toplevel(self.root)
        self.app = developer(self.new_window)
     
    #open HelpDesk :
    def helpdesk(self):
        self.new_window = Toplevel(self.root)
        self.app = helpdesk(self.new_window)

    #Exit Button:
    def exit_app(self):
        # Attempt to close any Toplevel windows first for a clean shutdown
        try:
            for w in self.root.winfo_children():
                if isinstance(w, Toplevel):
                    w.destroy()
        except Exception:
            pass
        self.root.destroy()  # close the main window and exit the application




    



if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop() 