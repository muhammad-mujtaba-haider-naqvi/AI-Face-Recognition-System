from tkinter import *
from PIL import Image, ImageTk

class developer:
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
            text="Developer Information",
            fill="white",
            font=("times new roman", int(screen_width * 0.017), "bold")
        )

        # Center Developer Info Frame (Responsive & Bigger)
        self.dev_frame = Frame(lblBG, bg="white", bd=3, relief=RIDGE)
        self.dev_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.6)

        # Project Name on top of dev_frame
        proj_name_label = Label(self.dev_frame, text="Face Recognition Attendance System",
                                font=("times new roman", 22, "bold"),
                                bg="white", fg="darkgreen")
        proj_name_label.pack(side=TOP, pady=(10, 10))

        # Create left frame for team info, right frame for group photo
        team_frame = Frame(self.dev_frame, bg="white")
        team_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(20, 10), pady=20)

        photo_frame = Frame(self.dev_frame, bg="white")
        photo_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 20), pady=20)

        # Team Information Table in team_frame
        Label(team_frame, text="Project Developers", font=("times new roman", 18, "bold"),
            bg="white", fg="darkblue").grid(row=0, column=0, columnspan=3, pady=10)

        Label(team_frame, text="Name", font=("times new roman", 14, "bold"), bg="white").grid(row=1, column=0, padx=20, sticky=W)
        Label(team_frame, text="Roll No", font=("times new roman", 14, "bold"), bg="white").grid(row=1, column=1, padx=20, sticky=W)
        Label(team_frame, text="Role", font=("times new roman", 14, "bold"), bg="white").grid(row=1, column=2, padx=20, sticky=W)

        devs = [
            ("Ahmad Sheraz", "FA23-BCS-176", "Team Lead"),
            ("Shaafea Dawood", "FA23-BCS-155", "Testing"),
            ("Mujtaba Haider", "FA23-BCS-125", "Designing")
        ]

        for i, (name, roll, role) in enumerate(devs, start=2):
            Label(team_frame, text=name, font=("times new roman", 13), bg="white").grid(row=i, column=0, padx=20, pady=5, sticky=W)
            Label(team_frame, text=roll, font=("times new roman", 13), bg="white").grid(row=i, column=1, padx=20, pady=5, sticky=W)
            Label(team_frame, text=role, font=("times new roman", 13), bg="white").grid(row=i, column=2, padx=20, pady=5, sticky=W)

        # Group Photo in photo_frame (right side)
        try:
            group_img = Image.open(r"APP Pictures\developerteam.jpg")
            group_img = group_img.resize((220, 220), Image.Resampling.LANCZOS)
            self.group_photo = ImageTk.PhotoImage(group_img)
            # Border frame with black background
            border_frame = Frame(photo_frame, bg="black", padx=2, pady=2)
            border_frame.pack(pady=10, padx=10)
            # Actual image label inside border frame
            group_img_label = Label(border_frame, image=self.group_photo, bg="white")
            group_img_label.pack()

        except Exception as e:
            Label(photo_frame, text="Image not found", bg="white", fg="red").pack(pady=10)

        # Submission Date at bottom center inside dev_frame
        date_label = Label(team_frame, text="Submitted On: 4th June 2025",
                   font=("times new roman", 14, "italic"),
                   bg="white", fg="red")
        date_label.grid(row=len(devs) + 2, column=0, columnspan=3, pady=(20, 0), sticky="w")


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







if __name__ == "__main__":
    root = Tk()
    obj = developer(root)
    root.mainloop()