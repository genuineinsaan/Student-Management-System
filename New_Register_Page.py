from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

class Register:
    def __init__(self, window):
        self.window = window
        self.window.title("USER REGISTRATION")
        self.window.state('zoomed')  # Fullscreen

        

        # === Load and place background image ===
        self.bg_img = Image.open("C:/Users/shash/OneDrive/Desktop/Academic Performance Tracker !!/Images/register_bg.jpg")  # Replace with your actual image filename
        self.bg_img = self.bg_img.resize(
            (self.window.winfo_screenwidth(), self.window.winfo_screenheight()),
            Image.LANCZOS  # Compatible with older Pillow versions
        )
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)

        bg_label = Label(self.window, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # === Variables ===
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.contact_no = StringVar()
        self.email_no = StringVar()
        self.pass_no = StringVar()
        self.conf_passwo = StringVar()
        self.ans = StringVar()
        self.combo = StringVar()
        self.var_chk = IntVar()

        # === Central Frame ===
        form_frame = Frame(self.window, bg="light yellow", bd=2, relief=RIDGE)
        form_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=700, height=500)

        Label(form_frame, text="REGISTER ACCOUNT", font=("Roboto", 22, "bold"), bg="white", fg="black").place(x=200, y=20)

        # First Row
        Label(form_frame, text="First Name:", font=("Roboto", 12), bg="white").place(x=50, y=80)
        Entry(form_frame, textvariable=self.first_name, font=("Roboto", 12), bd=1).place(x=50, y=110, width=250)

        Label(form_frame, text="Last Name:", font=("Roboto", 12), bg="white").place(x=370, y=80)
        Entry(form_frame, textvariable=self.last_name, font=("Roboto", 12), bd=1).place(x=370, y=110, width=250)

        # Second Row
        Label(form_frame, text="Contact Number:", font=("Roboto", 12), bg="white").place(x=50, y=150)
        Entry(form_frame, textvariable=self.contact_no, font=("Roboto", 12), bd=1).place(x=50, y=180, width=250)

        Label(form_frame, text="Email:", font=("Roboto", 12), bg="white").place(x=370, y=150)
        Entry(form_frame, textvariable=self.email_no, font=("Roboto", 12), bd=1).place(x=370, y=180, width=250)

        # Third Row
        Label(form_frame, text="Security Question:", font=("Roboto", 12), bg="white").place(x=50, y=220)
        self.combo_box_t = ttk.Combobox(form_frame, textvariable=self.combo, font=("Roboto", 12), state='readonly')
        self.combo_box_t['values'] = ("select", "your pet name", "your birth hour", "your favourite food", "your favourite teacher")
        self.combo_box_t.current(0)
        self.combo_box_t.place(x=50, y=250, width=250)

        Label(form_frame, text="Answer:", font=("Roboto", 12), bg="white").place(x=370, y=220)
        Entry(form_frame, textvariable=self.ans, font=("Roboto", 12), bd=1).place(x=370, y=250, width=250)

        # Password Row
        Label(form_frame, text="Password:", font=("Roboto", 12), bg="white").place(x=50, y=290)
        Entry(form_frame, show="*", textvariable=self.pass_no, font=("Roboto", 12), bd=1).place(x=50, y=320, width=250)

        Label(form_frame, text="Confirm Password:", font=("Roboto", 12), bg="white").place(x=370, y=290)
        Entry(form_frame, show="*", textvariable=self.conf_passwo, font=("Roboto", 12), bd=1).place(x=370, y=320, width=250)

        Checkbutton(form_frame, text="I Agree to the Terms & Conditions", variable=self.var_chk,
                    font=("Roboto", 10), bg="white").place(x=50, y=360)

        Button(form_frame, text="Register", font=("Roboto", 12, "bold"), bg="#4CAF50", fg="white",
               command=self.register_data).place(x=210, y=410, width=250)

        Button(form_frame, text="Back", font=("Roboto", 12, "bold"), bg="red", fg="white",
               command=self.back ).place(x=210, y=450, width=250)

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_system"
        )
    def back(self):
        self.window.destroy(); os.system("python New_Login_Page.py")

    def register_data(self):
        if (self.first_name.get() == "" or self.email_no.get() == "" or self.contact_no.get() == "" or
                self.combo.get() == "select" or self.ans.get() == "" or self.pass_no.get() == "" or
                self.conf_passwo.get() == ""):
            messagebox.showerror("Error", "All Fields are required!", parent=self.window)
        elif self.pass_no.get() != self.conf_passwo.get():
            messagebox.showerror("Error", "Confirm password should be same", parent=self.window)
        elif self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please Agree to the terms & condition", parent=self.window)
        elif not self.email_no.get().endswith("@gmail.com"):
            messagebox.showerror("Error", "Please enter a valid Gmail address", parent=self.window)
        else:
            try:
                con = self.get_connection()
                cur = con.cursor()
                cur.execute("SELECT * FROM employee WHERE email=%s", (self.email_no.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", "User already exists. Please enter properly", parent=self.window)
                else:
                    cur.execute("""
                        INSERT INTO employee 
                        (f_name, l_name, contact, email, question, answer, password) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        self.first_name.get(), self.last_name.get(), self.contact_no.get(),
                        self.email_no.get(), self.combo.get(), self.ans.get(), self.pass_no.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Detail added successfully", parent=self.window)
                    self.window.destroy()
                    os.system("python New_Login_Page.py")
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.window)
            finally:
                if 'con' in locals():
                    con.close()

        

# Run the app
if __name__ == "__main__":
    window = Tk()
    app = Register(window)
    window.mainloop()
