from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np


class train:
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
        header__height = int(screen_width / 3 / 2.3) # Common height

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
        gradient_canvas = Canvas(lblBG, width=screen_width, height=int(screen_height * 0.1), highlightthickness=0)
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
        draw_gradient(gradient_canvas, screen_width, int(screen_height * 0.1), start_color, end_color)
        # Add Title Text Over Gradient
        gradient_canvas.create_text(
            screen_width // 2,
            int(screen_height * 0.05),
            text="Train Data Set",
            fill="white",
            font=("times new roman", int(screen_width * 0.029), "bold")
        )

        # TRAINDATA Button 
        trainDataBtn = Image.open(r"APP Pictures\trainDataBtn.jpg")
        trainDataBtn = trainDataBtn.resize((180, 180), Image.Resampling.LANCZOS)
        self.trainDataBtn = ImageTk.PhotoImage(trainDataBtn)
        btn4 = Button(lblBG, image=self.trainDataBtn, command=self.train_data_classifier, cursor="hand2", bd=0, highlightthickness=0)
        btn4.place(x=int(screen_width * 0.43), y=int(screen_height * 0.25), width=180, height=180)
        btn4_4 = Button(lblBG, text="TRAIN DATA", command=self.train_data_classifier, cursor="hand2", # Text Button At Bottom of Student Button
                font=("Arial Rounded MT Bold", 15, "bold"),
                bg="#ffffff", fg="#004080", bd=0, highlightbackground="#ffffff")
        btn4_4.place(x=int(screen_width * 0.43), y=int(screen_height * 0.25) + 180 - 1, width=180, height=40)

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
        back_button.place(relx=0.95, rely=0.95, anchor="se")  # Bottom-right corner


    #Train Data Functoin
    def train_data_classifier(self):
        data_directory = ("face_data")
        path = [os.path.join(data_directory,file) for file in os.listdir(data_directory)]
        
        faces = []
        ids = []
        
        for image in path:
            img = Image.open(image).convert('L') # Converted In GrayScale
            imageNP = np.array(img,'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNP)
            ids.append(id)
            cv2.imshow("Training",imageNP)
            cv2.waitKey(1) == 13 

        ids = np.array(ids)

        # =============================================Training Classifier===============================
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Training Data Set Completed Successfully", parent = self.root)



if __name__ == "__main__":
    root = Tk()
    obj = train(root)
    root.mainloop()