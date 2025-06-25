from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk       
import mysql.connector
import os

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - ACADEMIC PERFORMANCE TRACKER")
        self.root.state("zoomed")                
        self.root.config(bg="#f0f0f0")

        
        self.bg_path = r"C:/Users/shash/OneDrive/Desktop/Academic Performance Tracker !!/Images/login_bg.jpg"
        self.bg_label = Label(self.root)         
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.update_background()                 
        self.root.bind("<Configure>", lambda e: self.update_background())   
        

        
        # Variables
        self.email_var = StringVar()
        self.pass_var = StringVar()
        self.show_password = IntVar()

        outer_frame = Frame(self.root, bg="sky blue")
        outer_frame.place(relx=0.5, rely=0.5, anchor="center")

        Label(outer_frame, text="ACADEMIC PERFORMANCE PORTAL",
              font=("Magic Marker", 28, "bold"), bg="sky blue", fg="#222").pack(pady=(20,10))
        Label(outer_frame, text="LOGIN PAGE",
              font=("Roboto", 20, "bold"), bg="sky blue", fg="#333").pack(pady=(0,20))

        frame = Frame(outer_frame, bg="deep sky blue", bd=2, relief=RIDGE)
        frame.pack(padx=10, pady=10)

        Label(frame, text="E-MAIL:", font=("Roboto", 12, "bold"), bg="deep sky blue")\
            .grid(row=0, column=0, sticky="w", padx=20, pady=10)
        self.txt_email = Entry(frame, textvariable=self.email_var,
                               font=("Roboto", 12), bd=2, width=30)
        self.txt_email.grid(row=0, column=1, padx=20, pady=10)

        Label(frame, text="PASSWORD:", font=("Roboto", 12, "bold"), bg="deep sky blue")\
            .grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.txt_pass = Entry(frame, textvariable=self.pass_var,
                              show="*", font=("Roboto", 12), bd=2, width=30)
        self.txt_pass.grid(row=1, column=1, padx=20, pady=10)

        Checkbutton(frame, text="SHOW PASSWORD", variable=self.show_password,
                    font=("Roboto", 10), bg="deep sky blue", command=self.toggle_password)\
            .grid(row=2, column=1, sticky="w", padx=20, pady=(0,10))

        btn_row = Frame(frame, bg="deep sky blue")
        btn_row.grid(row=3, column=1, pady=(5,5), sticky="w")

        Button(btn_row, text="LOGIN", font=("Roboto", 12, "bold"), bg="#4CAF50",
               fg="white", width=12, command=self.login_user).pack(side=LEFT, padx=(0,10))
        Button(btn_row, text="REGISTER", font=("Roboto", 12, "bold"), bg="#2196F3",
               fg="white", width=12, command=self.register_window).pack(side=LEFT)

        Button(frame, text="FORGET PASSWORD?", font=("Roboto", 10), fg="black",
               bg="deep sky blue", bd=0, command=self.forgot_password)\
            .grid(row=4, column=1, sticky="e", padx=20, pady=(5,10))

    
    def update_background(self):
        try:
            # get current window size
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            # avoid 1×1 early-startup bug
            if w < 2 or h < 2: return
            # open, resize, convert
            img = Image.open(self.bg_path).resize((w, h), Image.LANCZOS)
            self.bg_tk = ImageTk.PhotoImage(img)
            self.bg_label.configure(image=self.bg_tk)
        except Exception as e:
            # show once, then unbind to avoid spam
            self.root.unbind("<Configure>")
            messagebox.showwarning("Image Error",
                                   f"Could not resize background:\n{e}",
                                   parent=self.root)
    # -------------------------------------------------------

    # ---------- rest of your methods (toggle, login …) ----------
    def toggle_password(self):
        self.txt_pass.config(show="" if self.show_password.get() else "*")

    def get_connection(self):
        return mysql.connector.connect(host="localhost", user="root",
                                       password="sanjana1432", database="student_system")

    def login_user(self):
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM employee WHERE email=%s", (self.email_var.get(),))
            row = cur.fetchone()
            if row and self.pass_var.get() == row[7]:
                messagebox.showinfo("Success", "Login successful!", parent=self.root)
                self.root.destroy(); os.system("python New_Database_Page.py")
            else:
                messagebox.showerror("Error", "Invalid email or password", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Database Error", str(ex), parent=self.root)
        finally:
            if 'conn' in locals(): conn.close()

    def register_window(self):
        self.root.destroy(); os.system("python New_Register_Page.py")

    def forgot_password(self):
        self.root.destroy(); os.system("python New_Forgot_Password.py")

# Run GUI
if __name__ == "__main__":
    root = Tk()
    app = LoginApp(root)
    root.mainloop()
