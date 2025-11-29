from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import mysql.connector
import numpy as np


class face_recognition:
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def __init__(self, root):
        self.root = root
        self.fullscreen = True 
        self.video_cap = None  # will hold the active VideoCapture for cleanup
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
            text="Face Detector/Recognition",
            fill="white",
            font=("times new roman", int(screen_width * 0.017), "bold")
        )

        # ===== Center Portrait Image Below Gradient Title (Optimized) =====
        #Size & Position
        img = Image.open(r"APP Pictures\face_recognition_centre_frame.jpg")
        title_h = int(screen_height * 0.1)
        avail_h = screen_height - header__height - title_h
        tgt_h = int(avail_h * 0.85)
        tgt_w = int(tgt_h * (img.width / img.height))
        img = img.resize((tgt_w, tgt_h), Image.Resampling.LANCZOS)
        #Placement
        self.centre_img_photo = ImageTk.PhotoImage(img)
        Label(lblBG, image=self.centre_img_photo, bd=0).place(
            x=(screen_width - tgt_w) // 2,
            y=title_h + (avail_h - tgt_h) // 9
        )

        # ===== Face Recognition/Detector Button =====
        #Size & Position:
        btn_width = int(tgt_w * 0.6)
        btn_height = int(tgt_h * 0.07)
        btn_x = (screen_width - btn_width) // 2
        btn_y = title_h + (avail_h - tgt_h) // 9 + tgt_h + 60 - btn_height - 17  # 20px padding above image bottom
        #Placement:
        face_recognition_BTN = Button(lblBG, text="Start Recognition", command=self.face_recognition_func,
                                      font=("Helvetica", 14, "bold"),bg="darkgreen", fg="white", bd=0, 
                                      activebackground="#45a049")
        face_recognition_BTN.place(x=btn_x, y=btn_y, width=btn_width, height=btn_height)

        # ===== Back Button - Bottom Right Corner =====
        back_button = Button(
            self.root,
            text="Back",
            command=self.on_back,
            font=("times new roman", 13, "bold"),
            bg="red",
            fg="white",
            cursor="hand2",
            width=10
        )
        back_button.place(relx=0.95, rely=0.95, anchor="se")  # Bottom-right corner


    def cleanup(self):
        """Release camera and destroy any OpenCV windows."""
        try:
            if self.video_cap is not None and self.video_cap.isOpened():
                self.video_cap.release()
        except Exception:
            pass
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass

    def on_back(self):
        """Handle Back button: cleanup resources then close window."""
        self.cleanup()
        self.root.destroy()

    #======================Face Recognition Function====================
    def face_recognition_func(self):
        def draw_boundary(img, classifier, scale_factor, min_neighbour, color, text, clf):
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_img, scale_factor, min_neighbour)
            coordinates = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                id, predict = clf.predict(gray_img[y:y + h, x:x + w])
                print(f"Predicted ID: {id}, Confidence Value: {predict}")
                confidence = int(100 * (1 - predict / 300))

                try:
                    conn = mysql.connector.connect(
                        host="127.0.0.1", username="root", password="12345", database="FaceRecognitionSystem"
                    )
                    my_cursor = conn.cursor()
                    my_cursor.execute("SELECT name, roll_no, department FROM student WHERE student_id = %s", (id,))
                    result = my_cursor.fetchone()
                    conn.close()

                    if result:
                        n, r, d = result
                    else:
                        n, r, d = "Unknown", "N/A", "N/A"
                except Exception as e:
                    print("Database Error:", e)
                    # n, r, d = "DB Error", "N/A", "N/A"

                if confidence > 82:
                    cv2.putText(img, f"Roll No: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coordinates = [x, y, w, h]

            return coordinates

        def recognize(img, clf, faceCascade):
            coordinates = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
            return img

        # Check if classifier.xml exists
        if not os.path.exists("classifier.xml"):
            messagebox.showerror("Model Error", "classifier.xml not found. Please train your model first.")
            return

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # LBPHFaceRecognizer lives in the opencv-contrib package. Provide a clear message if missing.
        try:
            clf = cv2.face.LBPHFaceRecognizer_create()
        except AttributeError:
            messagebox.showerror(
                "OpenCV Contrib Missing",
                "cv2.face is unavailable. Install opencv-contrib-python (the contrib build) or use a Python version that has wheels for it."
            )
            return
        try:
            clf.read("classifier.xml")
        except Exception as e:
            messagebox.showerror("Model Load Error", f"Failed to read classifier.xml: {e}")
            return

        self.video_cap = cv2.VideoCapture(0)
        if not self.video_cap.isOpened():
            messagebox.showerror("Camera Error", "Cannot access webcam. Please check your camera.")
            return

        while True:
            ret, img = self.video_cap.read()
            if not ret:
                break
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition", img)
            key = cv2.waitKey(1) & 0xFF
            # Exit on Enter (13) or Esc (27)
            if key in (13, 27):
                break
            # If user manually closes the window (clicks X), stop re-opening
            if cv2.getWindowProperty("Face Recognition", cv2.WND_PROP_VISIBLE) < 1:
                break

        self.cleanup()



                


if __name__ == "__main__":
    root = Tk()
    obj = face_recognition(root)
    root.mainloop()