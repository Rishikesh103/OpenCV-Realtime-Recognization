import tkinter as tk
from tkinter import messagebox

import PIL
import cv2
import os
import face_recognition
from PIL import Image, ImageTk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.attributes("-fullscreen", True)


        # set the background image
        self.configure(background='light blue')
        self.bg_label = tk.Label(self)
        img = Image.open(r"E:\STUDY MATERIAL\CPP(megaproject)\GUI_FACE\GUI_FACE\bg.jpg")
        img=img.resize((screen_width,screen_height), PIL.Image.LANCZOS )
        self.bg_label.img = ImageTk.PhotoImage(img)
        self.bg_label['image'] = self.bg_label.img
        self.bg_label.place(x=0, y=0)

        # set the logo image
        self.logo_label = tk.Label(self,bg='light blue')
        img = Image.open(r"E:\STUDY MATERIAL\CPP(megaproject)\GUI_FACE\GUI_FACE\logo.png")
        img = img.resize((200,200), PIL.Image.LANCZOS )
        self.logo_label.img = ImageTk.PhotoImage(img)
        self.logo_label['image'] = self.logo_label.img
        self.logo_label.pack(side=tk.TOP, pady=10)
        
        
        # self.heading=tk.Label(self, text="SPYFIX APP", font=("Arial", 80),bg='light blue')
        # self.heading.pack(pady=30)
        # Create two buttons
        self.btn_register = tk.Button(self, text="Register User", command=self.register_user,font=("Arial", 40),bg='light blue')
        self.btn_register.pack(pady=200)

        self.btn_face_classification = tk.Button(self, text="Identify  User", command=self.face_classification,font=("Arial", 40),bg='light blue')
        self.btn_face_classification.pack(pady=20)

    def register_user(self):
        # Destroy the existing buttons
        self.btn_register.destroy()
        self.btn_face_classification.destroy()
        
        self.btn_back=tk.Button(self,text="Home",command=self.__init__,font=("Arial", 40),bg='light blue').place(x=0, y=1000)
        
        # Create two buttons for criminal and hostage
        self.btn_criminal = tk.Button(self, text="Register Criminal",bg='light blue', command=lambda: self.user_details("criminal"),font=("Arial", 40))
        self.btn_criminal.pack(pady=150)

        self.btn_hostage = tk.Button(self, text="Register Hostage",bg='light blue', command=lambda: self.user_details("hostage"),font=("Arial", 40))
        self.btn_hostage.pack(pady=160)

    def user_details(self, user_type):
        self.btn_criminal.destroy()
        self.btn_hostage.destroy()
        # 1980x1080
        # Create labels and entries to get user information
        self.lbl_name = tk.Label(self, text="     Name     ",font=("Arial", 30),bg='light blue')
        self.lbl_name.pack(pady=20)

        self.ent_name = tk.Entry(self,font=("Arial", 30),bg='light blue')
        self.ent_name.pack(pady=20)

        self.lbl_age = tk.Label(self, text="      Age      ",font=("Arial", 30),bg='light blue')
        self.lbl_age.pack(pady=20)

        self.ent_age = tk.Entry(self,font=("Arial", 30),bg='light blue')
        self.ent_age.pack(pady=20)

        if user_type == "criminal":
            self.lbl_crime = tk.Label(self, text="     Crime     ",font=("Arial", 30),bg='light blue')
            self.lbl_crime.pack(pady=20)

            self.ent_crime = tk.Entry(self,font=("Arial", 30),bg='light blue')
            self.ent_crime.pack(pady=20)

        elif user_type == "hostage":
            self.lbl_contact = tk.Label(self, text="Contact Details",font=("Arial", 30),bg='light blue')
            self.lbl_contact.pack(pady=20)

            self.ent_contact = tk.Entry(self,font=("Arial", 30),bg='light blue')
            self.ent_contact.pack(pady=20)

            self.lbl_area = tk.Label(self, text="      Area     ",font=("Arial", 30),bg='light blue')
            self.lbl_area.pack(pady=20)

            self.ent_area = tk.Entry(self,font=("Arial", 30),bg='light blue')
            self.ent_area.pack(pady=20)
        # Create a button to submit the user details
        self.btn_submit = tk.Button(self, text="  Submit  ", command=lambda: self.capture_face(user_type),font=("Arial", 40),bg='light blue')
        self.btn_submit.pack(pady=30)
        
    def capture_face(self,user_type):
        if self.ent_name.get() == "" or self.ent_age.get() == "":
            self.lbl_name.destroy()
            self.ent_name.destroy()
            self.lbl_age.destroy()
            self.ent_age.destroy()
            if user_type == "criminal":
                self.lbl_crime.destroy()
                self.ent_crime.destroy()
            else:
                self.lbl_contact.destroy()
                self.ent_contact.destroy()
                self.lbl_area.destroy()
                self.ent_area.destroy()
            self.btn_submit.destroy()
            
            messagebox.showerror("Error", "Please enter all the details",command=self.user_details(user_type))
        else:
            # Get user information from the entries
            name = self.ent_name.get()
            age = self.ent_age.get()
            # Create a folder with the user's name and save the user information in a text file
            if not os.path.exists('./users'):
                os.makedirs('./users')
                os.makedirs('./users/criminal')
                os.makedirs('./users/hostage')
            folder_path = f"./users/{user_type}/{name}"
            os.makedirs(folder_path, exist_ok=True)
            # start video capture
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                #Name the cv2 window
                frame = cv2.resize(frame, (int(1980), int(1080)))
                cv2.namedWindow("Capture Image",cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Capture Image", cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
                # display frame
                cv2.putText(frame, "Press 'c' to capture!", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2)
                cv2.imshow("Capture Image", frame)
                
                #Set the properties of GUI app
                # wait for "Capture" button to be clicked
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    # capture image and save to file
                    face_locations = face_recognition.face_locations(frame)
                    if len(face_locations) == 1:
                        print("Face registered successfully!")
                        img_path = "./users/"+str(user_type)+"/"+str(name)+"/face.jpg"
                        cv2.imwrite(img_path, frame)
                        break
                    else:
                        cv2.putText(frame, "Please make sure there is only one face in the frame", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            # ask for additional information
            messagebox.showinfo("Info", "Face registered successfully!")
            

            with open(f"{folder_path}/{name}.txt", "w") as f:
                f.write(f"Name: {name}\n")
                f.write(f"Age: {age}\n")
                if user_type == "criminal":
                    crime = self.ent_crime.get()
                    f.write(f"Crime: {crime}\n")

                elif user_type == "hostage":
                    contact = self.ent_contact.get()
                    area = self.ent_area.get()
                    f.write(f"Contact Details: {contact}\n")
                    f.write(f"Area: {area}\n")
            self.btn_criminal.destroy()
            self.btn_hostage.destroy()
            self.lbl_name.destroy()
            self.ent_name.destroy()
            self.lbl_age.destroy()
            self.ent_age.destroy()
            if user_type == "criminal":
                self.lbl_crime.destroy()
                self.ent_crime.destroy()
            else:
                self.lbl_contact.destroy()
                self.ent_contact.destroy()
                self.lbl_area.destroy()
                self.ent_area.destroy()
            self.btn_submit.destroy()

            # Recreate the original buttons
            # Create two buttons
            self.btn_register = tk.Button(self, text="Register User", command=self.register_user,font=("Arial", 40),bg='light blue')
            self.btn_register.pack(pady=150)

            self.btn_face_classification = tk.Button(self, text="Face Classification", command=self.face_classification,font=("Arial", 40),bg='light blue')
            self.btn_face_classification.pack(pady=160)

    def face_classification(self):
        # load known faces
        known_encodings = []
        known_names = []
        known_type=[]
        for user_name in os.listdir(f"./users/criminal"):
            try:
                user_dir = f"./users/criminal/{user_name}/"
                if not os.path.isdir(user_dir):
                    continue
                img_path = os.path.join(user_dir, "face.jpg")
                if not os.path.exists(img_path):
                    continue
                img = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(img)[0]
                known_encodings.append(encodings)
                known_names.append(user_name)
                known_type.append("criminal")
            except:
                pass
        for user_name in os.listdir(f"./users/hostage"):
            try:
                user_dir = f"./users/hostage/{user_name}/"
                if not os.path.isdir(user_dir):
                    continue
                img_path = os.path.join(user_dir, "face.jpg")
                if not os.path.exists(img_path):
                    continue
                img = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(img)[0]
                known_encodings.append(encodings)
                known_names.append(user_name)
                known_type.append("hostage")
            except:
                pass
        print(known_names)
        print(known_type)
        self.btn_register.destroy()
        self.btn_face_classification.destroy()
        # start video capture
        cap = cv2.VideoCapture(0)
        text=""
        text1=" "
        name=""
        name1=" "
        user_type="None"
        age="None"
        crime="None"
        contact="None"
        area="None"
        while True:
            text=""
            ret, frame = cap.read()
            frame=cv2.resize(frame,(1920,1080))
            # detect faces in frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            # compare detected faces with known faces
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                name = "Unknown"
                # find best match
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    user_type=known_type[best_match_index]
                # draw bounding box and label on frame
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 1)

                # Display the user information if a match is found
                if name is not None and name != "Unknown":
                    # Load the user's image
                    with open(f"./users/{user_type}/{name}/{name}.txt", "r") as f:
                        lines = f.readlines()
                        age = lines[1].split(":")[1].strip()
                        if user_type == "criminal":
                            crime = lines[2].split(":")[1].strip()
                        elif user_type == "hostage":
                            contact = lines[2].split(":")[1].strip()
                            area = lines[3].split(":")[1].strip()
                    # Draw the face box and user information
                    # cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    startX = left
                    startY = top
                    y = startY - 15
                    text+=f"Name: {name} ({user_type})\n"
                    text+=f"Age: {age}\n"
                    
                    cv2.putText(frame, f"{name} ({user_type})", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    y = startY + 15
                    cv2.putText(frame, f"Age: {age}", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    if user_type == "criminal":
                        text+=f"Crime: {crime}\n"
                        y = startY + 45
                        cv2.putText(frame, f"Crime: {crime}", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    elif user_type == "hostage":
                        text+=f"Contact: {contact}\n"
                        text+=f"Area: {area}\n"
                        y = startY + 45
                        cv2.putText(frame, f"Contact: {contact}", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        y = startY + 75
                        cv2.putText(frame, f"Area: {area}", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                text1=text
                
                try:
                    self.lbl_name.destroy()
                    self.lbl_age.destroy()
                except:
                    pass
                try:
                    self.lbl_crime.destroy()
                except:
                    pass
                try:
                    self.lbl_contact.destroy()
                    self.lbl_area.destroy()
                except:
                    pass
                # Create the Text widget and add some text to it
                # self.text_widget = tk.Text(self, height=15, width=30,bg='light blue',font=("Helvetica", 25))
                # self.text_widget.insert(tk.END, text1)
                # self.text_widget.place(x=1300,y=250)
                
                self.lbl_name = tk.Label(self, text=f"Name: {name} ({user_type})",font=("Arial", 30),bg='light blue')
                self.lbl_name.place(x=1000,y=250)

                self.lbl_age = tk.Label(self, text=f"Age: {age}",font=("Arial", 30),bg='light blue',)
                self.lbl_age.place(x=1000,y=310)

                if user_type == "criminal":
                    self.lbl_crime = tk.Label(self, text=f"Crime: {crime}",font=("Arial", 30),bg='light blue')
                    self.lbl_crime.place(x=1000,y=370)

                elif user_type == "hostage":
                    self.lbl_contact = tk.Label(self, text=f"Contact Details: {contact}",font=("Arial", 30),bg='light blue')
                    self.lbl_contact.place(x=1000,y=370)

                    self.lbl_area = tk.Label(self, text=f"Area: {area}",font=("Arial", 30),bg='light blue')
                    self.lbl_area.place(x=1000,y=430)

                # Pack the Text widget to the right side of the window
                # self.text_widget.pack(side=tk.RIGHT)
                self.update()

            # Show the frame
            cv2.namedWindow("Face Classification", cv2.WINDOW_NORMAL)  # set window to normal size
            cv2.resizeWindow("Face Classification", 800, 600)  # set custom size
            cv2.moveWindow("Face Classification", 100, 250)   # set fixed position
            cv2.putText(frame, "Press 'q' to quit", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.setWindowProperty("Face Classification", cv2.WND_PROP_TOPMOST, 1)  # set always on top
            cv2.imshow("Face Classification", frame)#Name the GUI app
            
            
            #Set the properties of GUI app

            # Exit if the 'q' key is pressed
            if cv2.waitKey(1) == ord("q"):
                self.update()
                break

        # Release the webcam and destroy all windows
        cap.release()
        cv2.destroyAllWindows()
        try:
            self.lbl_name.destroy()
            self.lbl_age.destroy()
        except:
            pass
        try:
            self.lbl_crime.destroy()
        except:
            pass
        try:
            self.lbl_contact.destroy()
            self.lbl_area.destroy()
        except:
            pass
        
        self.update()
        self.btn_register = tk.Button(self, text="Register User", command=self.register_user,font=("Arial", 40),bg='light blue')
        self.btn_register.pack(pady=150)

        self.btn_face_classification = tk.Button(self, text="Face Classification", command=self.face_classification,font=("Arial", 40),bg='light blue')
        self.btn_face_classification.pack(pady=160)

def start(front):
    front.destroy()
    app = GUI()
    app.mainloop()

front=tk.Tk()

screen_width = front.winfo_screenwidth()
screen_height = front.winfo_screenheight()
front.attributes("-fullscreen", True)


# set the background image
front.configure(background='light blue')
bg_label = tk.Label(front)
img = Image.open(r"E:\STUDY MATERIAL\CPP(megaproject)\GUI_FACE\GUI_FACE\front.jpg")
img=img.resize((screen_width,screen_height),  PIL.Image.LANCZOS)
bg_label.img = ImageTk.PhotoImage(img)
bg_label['image'] = bg_label.img
bg_label.place(x=0, y=0)

btn_start = tk.Button(front, text="Start", command=lambda: start(front),font=("Arial", 40))
btn_start.pack(side=tk.BOTTOM)

front.mainloop()