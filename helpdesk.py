from tkinter import *
from PIL import Image, ImageTk
import webbrowser  # Needed to open Gmail or default email client


class helpdesk:
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
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width1 = screen_width // 3
        width2 = screen_width // 3
        width3 = screen_width - (width1 + width2)
        header__height = int(screen_width / 3 / 3.85)

        # Header Images
        img1 = Image.open(r"APP Pictures\headerLeft.JPG").resize((width1, header__height), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1, bd=0).place(x=0, y=0)

        img2 = Image.open(r"APP Pictures\headerCentre.png").resize((width2, header__height), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2, bd=0).place(x=width1, y=0)

        img3 = Image.open(r"APP Pictures\headerRight.jpeg").resize((width3, header__height), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        Label(self.root, image=self.photoimg3, bd=0).place(x=width1 + width2, y=0)

        # Background
        imgBG = Image.open(r"APP Pictures\backGround.jpg").resize((screen_width, screen_height - header__height), Image.Resampling.LANCZOS)
        self.photoimgBG = ImageTk.PhotoImage(imgBG)
        lblBG = Label(self.root, image=self.photoimgBG, bd=0)
        lblBG.place(x=0, y=header__height)

        # Gradient Title Header
        gradient_canvas = Canvas(lblBG, width=screen_width, height=int(screen_height * 0.055), highlightthickness=0)
        gradient_canvas.place(x=0, y=0)

        def draw_gradient(canvas, width, height, start_rgb, end_rgb):
            r_diff = (end_rgb[0] - start_rgb[0]) / width
            g_diff = (end_rgb[1] - start_rgb[1]) / width
            b_diff = (end_rgb[2] - start_rgb[2]) / width
            for i in range(width):
                r = int(start_rgb[0] + (r_diff * i))
                g = int(start_rgb[1] + (g_diff * i))
                b = int(start_rgb[2] + (b_diff * i))
                canvas.create_line(i, 0, i, height, fill=f"#{r:02x}{g:02x}{b:02x}")

        draw_gradient(gradient_canvas, screen_width, int(screen_height * 0.06), (128, 0, 128), (255, 0, 0))

        gradient_canvas.create_text(
            screen_width // 2,
            int(screen_height * 0.03),
            text="Help Desk",
            fill="white",
            font=("times new roman", int(screen_width * 0.017), "bold")
        )

        # === Support Contact Frame ===
        frame_width = int(screen_width * 0.5)
        frame_height = int(screen_height * 0.35)

        support_frame = Frame(lblBG, bg="white", bd=3, relief=RIDGE)
        support_frame.place(relx=0.5, rely=0.55, anchor="center", width=frame_width, height=frame_height)

        padding_x = 20
        padding_y = 8
        label_font = ("times new roman", 17)
        title_font = ("times new roman", 20, "bold")

        Label(
            support_frame, text="Support & Contact Information",
            font=title_font, bg="white", fg="#800080", pady=15
        ).pack()

        # --- Hover & Clickable Email Label ---
        def open_email(event):
            gmail_url = "https://mail.google.com/mail/?view=cm&fs=1&to=fa23-bcs-176@cuilahore.edu.pk"
            webbrowser.open(gmail_url)

        def on_enter(event):
            email_label.config(fg="blue", cursor="hand2", font=("times new roman", 17, "underline"))

        def on_leave(event):
            email_label.config(fg="black", font=("times new roman", 17))

        email_label = Label(
            support_frame,
            text="📧 Email: fa23-bcs-176@cuilahore.edu.pk",
            font=label_font, bg="white", fg="black",
            anchor="w", padx=padding_x
        )
        email_label.pack(fill="x", pady=padding_y)
        email_label.bind("<Enter>", on_enter)
        email_label.bind("<Leave>", on_leave)
        email_label.bind("<Button-1>", open_email)

        # Phone Label
        Label(
            support_frame,
            text="📞 Phone: +92 328 7537973",
            font=label_font, bg="white", fg="black",
            anchor="w", padx=padding_x
        ).pack(fill="x", pady=padding_y)

        # Development Team
        team_frame = Frame(support_frame, bg="white")
        team_frame.pack(fill="x", pady=padding_y, padx=padding_x)

        Label(team_frame, text="🧑‍💻 Development Team: ", font=label_font, bg="white", fg="black").pack(side=LEFT)

        Label(
            team_frame,
            text="BCS-TRIVEX | COMSATS LHR",
            font=("times new roman", 17, "bold"),
            bg="white", fg="#b22222"
        ).pack(side=LEFT)

        Label(
            support_frame,
            text="📌 For any technical issues or suggestions, feel free to reach out.",
            font=("times new roman", 15, "italic"), bg="white", fg="green",
            padx=padding_x, pady=padding_y
        ).pack(fill="x")

        # === Back Button (Bottom-Right Corner) ===
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
    obj = helpdesk(root)
    root.mainloop()
