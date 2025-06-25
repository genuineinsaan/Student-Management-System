from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

class ResultClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Academic Performance Tracker")
        self.window.state('zoomed')
        self.window.config(bg="#ffffff")
        self.window.focus_force()

        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.CA1 = StringVar()
        self.CA2 = StringVar()
        self.CA3 = StringVar()
        self.CA4 = StringVar()
        self.roll_list = []

        self.fetch_roll()

        # Title
        title = Label(self.window, text="Add Student Result", font=("goudy old style", 24, "bold"),
                      bg="#033054", fg="#ffffff")
        title.pack(side=TOP, fill=X)

        # Main Frame
        main_frame = Frame(self.window, bg="#ffffff")
        main_frame.place(x=20, y=60, relwidth=0.97, relheight=0.9)

        # Left Section
        left_frame = Frame(main_frame, bg="#ffffff")
        left_frame.place(relx=0.02, rely=0.05, relwidth=0.55, relheight=0.9)

        Label(left_frame, text="Select Student", font=("goudy old style", 20, "bold"),
               bg="#ffffff").grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.txt_student = ttk.Combobox(left_frame, textvariable=self.var_roll,
                                      values=self.roll_list, font=("goudy old style", 20),
                                      state='readonly')
        self.txt_student.grid(row=0, column=1, padx=10, pady=10)

        Button(left_frame, text="Search",width=12 , font=("goudy old style", 20, "bold"),
               bg="#03a9f4", fg="#ffffff", cursor="hand2", command=self.search).grid(row=0, column=2, padx=10, pady=10)

        Label(left_frame, text="Name", font=("goudy old style", 20, "bold"),
               bg="#ffffff").grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.txt_name =Entry(left_frame, textvariable=self.var_name,
                             font=("goudy old style", 20), state='readonly',
                             bg="#fff9cc")
        self.txt_name.grid(row=1, column=1, padx=10, pady=10)

        Label(left_frame, text="Course", font=("goudy old style", 20, "bold"),
               bg="#ffffff").grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.txt_course =Entry(left_frame, textvariable=self.var_course,
                             font=("goudy old style", 20), state='readonly',
                             bg="#fff9cc")
        self.txt_course.grid(row=2, column=1, padx=10, pady=10)

        Label(left_frame, text="CA1", font=("goudy old style", 20, "bold"),
               bg="#ffffff").grid(row=3, column=0, sticky="w", padx=10, pady=10)

        self.CA1_entry =Entry(left_frame, textvariable=self.CA1,
                             font=("goudy old style", 20), bg="#fff9cc")
        self.CA1_entry.grid(row=3, column=1, padx=10, pady=10)

        Label(left_frame, text="CA2", font=("goudy old style", 20, "bold"),
               bg="#ffffff").grid(row=4, column=0, sticky="w", padx=10, pady=10)

        self.CA2_entry =Entry(left_frame, textvariable=self.CA2,
                             font=("goudy old style", 20), bg="#fff9cc")
        self.CA2_entry.grid(row=4, column=1, padx=10, pady=10)

        Label(left_frame, text="CA3", font=("goudy old style", 20, "bold"),
               bg="#ffffff").grid(row=5, column=0, sticky="w", padx=10, pady=10)

        self.CA3_entry =Entry(left_frame, textvariable=self.CA3,
                             font=("goudy old style", 20), bg="#fff9cc")
        self.CA3_entry.grid(row=5, column=1, padx=10, pady=10)

        Label(left_frame, text="CA4", font=("goudy old style", 20, "bold"),
               bg="#ffffff").grid(row=6, column=0, sticky="w", padx=10, pady=10)

        self.CA4_entry =Entry(left_frame, textvariable=self.CA4,
                             font=("goudy old style", 20), bg="#fff9cc")
        self.CA4_entry.grid(row=6, column=1, padx=10, pady=10)

        # Button Frame
        button_frame = Frame(left_frame, bg="#ffffff")
        button_frame.grid(row=7, columnspan=3, pady=20)

        Button(button_frame, text="Save", width=12, font=("goudy old style", 20),
               bg="#4caf50", fg="#ffffff", command=self.add).pack(side=LEFT, padx=10)

        Button(button_frame, text="Update", width=12, font=("goudy old style", 20),
               bg="#ff9800", fg="#ffffff", command=self.update_result).pack(side=LEFT, padx=10)

        Button(button_frame, text="Clear", width=12, font=("goudy old style", 20),
               bg="#607d8b", fg="#ffffff", command=self.clear_fields).pack(side=LEFT, padx=10)

        Button(button_frame, text="Home", width=12, font=("goudy old style", 20),
               bg="#ffeb3b", fg="#000000", command=self.go_home).pack(side=LEFT, padx=10)

        # Right Section (Picture or Logo Holder)
        img = Image.open("C:/Users/shash/OneDrive/Desktop/Academic Performance Tracker !!/Images/result.webp")
        img = img.resize((500,500))
        photo = ImageTk.PhotoImage(img)

        lbl_img = Label(main_frame, image=photo, bg="#ffffff")
        lbl_img.image = photo
        lbl_img.place(relx=0.60, rely=0.05)

    def fetch_roll(self):
        """Fetch all roll from student table in MySQL."""
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")
            cur = con.cursor()
            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()
            self.roll_list = [item[0] for item in rows]
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching roll: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def search(self):
        """Search student details by roll."""
        if not self.var_roll.get():
            messagebox.showerror("Error", "Please select a roll.")
            return
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")
            cur = con.cursor()
            cur.execute("SELECT name, course FROM student WHERE roll = %s", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])

                cur.execute("SELECT CA1, CA2, CA3, CA4 FROM result WHERE roll = %s", (self.var_roll.get(),))
                res = cur.fetchone()
                if res:
                    self.CA1.set(res[0])
                    self.CA2.set(res[1])
                    self.CA3.set(res[2])
                    self.CA4.set(res[3])
                else:
                    self.CA1.set("")
                    self.CA2.set("")
                    self.CA3.set("")
                    self.CA4.set("")
            else:
                messagebox.showinfo("Not found", "Student not found.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error searching student: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def add(self):
        """Add a new result for student."""
        if not self.var_name.get():
            messagebox.showerror("Error", "Please search for a student first.")
            return
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE roll = %s", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Error", "Result already exists.")
            else:
                cur.execute(" INSERT INTO result (roll, name, course, CA1, CA2, CA3, CA4) VALUES(%s, %s, %s, %s, %s, %s, %s)", 
                            (self.var_roll.get(), self.var_name.get(), self.var_course.get(), self.CA1.get(), self.CA2.get(), self.CA3.get(), self.CA4.get()) )
                con.commit()
                messagebox.showinfo("Success", "Result added successfully.")
                self.clear_fields()
                self.fetch_roll()
        except Exception as ex:
            messagebox.showerror("Error", f"Error adding result: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def update_result(self):
        """Update existing student result."""
        if not self.var_name.get():
            messagebox.showerror("Error", "Please search for a student first.")
            return
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")
            cur = con.cursor()
            cur.execute("UPDATE result SET CA1 = %s, CA2 = %s, CA3 = %s, CA4 = %s WHERE roll = %s",
                        (self.CA1.get(), self.CA2.get(), self.CA3.get(), self.CA4.get(), self.var_roll.get()) )
            con.commit()
            messagebox.showinfo("Success", "Result updated successfully.")
            self.clear_fields()
        except Exception as ex:
            messagebox.showerror("Error", f"Error updating result: {str(ex)}")
        finally:
            if 'con' in locals():
                con.close()

    def clear_fields(self):
        """Clear all fields."""
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.CA1.set("")
        self.CA2.set("")
        self.CA3.set("")
        self.CA4.set("")

    def go_home(self):
        """Go back to main page."""
        if messagebox.askyesno("Confirm", "Do you really want to go Home?"):
            self.window.destroy()
            os.system("python New_Database_Page.py")

# GUI RUN
if __name__ == "__main__":
    root = Tk()
    app = ResultClass(root)
    root.mainloop()
