from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

class StudentClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Academic Performance Tracker")
        self.window.state('zoomed')
        self.window.config(bg="white")

        # Variables
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_a_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()

        # Title
        title = Label(self.window, text="📘 Manage Student Details", font=("goudy old style", 22, "bold"),
                      bg="#033054", fg="white")
        title.pack(side=TOP, fill=X)

        # Content Frame
        content_frame = Frame(self.window, bg="white")
        content_frame.place(x=10, y=60, relwidth=0.98, relheight=0.80)

        # Form Frame
        form_frame = Frame(content_frame, bg="white")
        form_frame.place(relx=0.01, rely=0.02, relwidth=0.58, relheight=0.95)

        # Form Widgets
        fields = [
            ("Roll No", self.var_roll), ("Name", self.var_name), ("Email", self.var_email),
            ("Gender", self.var_gender), ("State", self.var_state), ("PIN", self.var_pin),
            ("D.O.B (y.m.d)", self.var_dob), ("Contact", self.var_contact), ("Admission (y.m.d)", self.var_a_date),
            ("Course", self.var_course), ("City", self.var_city)
        ]
        for idx, (label, var) in enumerate(fields[:6]):
            Label(form_frame, text=label, font=("goudy old style", 14, "bold"), bg="white")\
                .grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            if label == "Gender":
                gender_cb = ttk.Combobox(form_frame, textvariable=var, font=("goudy old style", 14),
                                         values=["Select", "Male", "Female", "Other"], state="readonly", justify="center")
                gender_cb.grid(row=idx, column=1, padx=10, pady=5)
                gender_cb.current(0)
            else:
                Entry(form_frame, textvariable=var, font=("goudy old style", 14), bg="lightyellow")\
                    .grid(row=idx, column=1, padx=10, pady=5)

        for idx, (label, var) in enumerate(fields[6:], start=0):
            Label(form_frame, text=label, font=("goudy old style", 14, "bold"), bg="white")\
                .grid(row=idx, column=2, sticky="w", padx=10, pady=5)
            if label == "Course":
                self.course_list = []
                self.fetch_course()
                course_cb = ttk.Combobox(form_frame, textvariable=var, font=("goudy old style", 14),
                                         values=self.course_list, state="readonly", justify="center")
                course_cb.grid(row=idx, column=3, padx=10, pady=5)
                course_cb.set("Select")
            else:
                Entry(form_frame, textvariable=var, font=("goudy old style", 14), bg="lightyellow")\
                    .grid(row=idx, column=3, padx=10, pady=5)

        Label(form_frame, text="Address", font=("goudy old style", 14, "bold"), bg="white")\
            .grid(row=6, column=0, sticky="nw", padx=10, pady=5)
        self.txt_address = Text(form_frame, font=("goudy old style", 14), bg="lightyellow", height=3, width=30)
        self.txt_address.grid(row=6, column=1, columnspan=3, padx=10, pady=5)

        # Button Frame
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=7, column=0, columnspan=4, pady=20)
        Button(btn_frame, text="Save", width=12, font=("goudy old style", 14), bg="#2196f3", fg="white", command=self.add).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Update", width=12, font=("goudy old style", 14), bg="#4caf50", fg="white", command=self.update).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Delete", width=12, font=("goudy old style", 14), bg="#f44336", fg="white", command=self.delete).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Clear", width=12, font=("goudy old style", 14), bg="#607d8b", fg="white", command=self.clear).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Home", width=12, font=("goudy old style", 14), bg="#FDFF5A", fg="black", command=self.go_home).pack(side=LEFT, padx=10)

        # Image Frame
        self.img = Image.open("C:/Users/shash/OneDrive/Desktop/Academic Performance Tracker !!/Images/banner.webp")  # Replace with your own image path
        self.img = self.img.resize((690, 210), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.img)
        Label(form_frame, image=self.photo, bg="white").grid(row=8, column=0, columnspan=4, pady=10)

        # Table Frame
        table_frame = Frame(content_frame, bg="white", bd=2, relief=RIDGE)
        table_frame.place(relx=0.61, rely=0.02, relwidth=0.37, relheight=0.95)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        self.student_table = ttk.Treeview(table_frame, columns=("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "pin", "address"),
                                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=self.student_table.yview)
        scroll_x.config(command=self.student_table.xview)

        for col in self.student_table["columns"]:
            self.student_table.heading(col, text=col.capitalize())
            self.student_table.column(col, width=100)
        self.student_table["show"] = "headings"
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    def get_connection(self):
        return mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")

    def add(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO student (roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (self.var_roll.get(), self.var_name.get(), self.var_email.get(), self.var_gender.get(),
                         self.var_dob.get(), self.var_contact.get(), self.var_a_date.get(), self.var_course.get(),
                         self.var_state.get(), self.var_city.get(), self.var_pin.get(),
                         self.txt_address.get("1.0", END).strip()))
            con.commit()
            messagebox.showinfo("Success", "Student added successfully")
            self.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'con' in locals(): con.close()

    def update(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("UPDATE student SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, admission=%s, course=%s, state=%s, city=%s, pin=%s, address=%s WHERE roll=%s",
                        (self.var_name.get(), self.var_email.get(), self.var_gender.get(), self.var_dob.get(),
                         self.var_contact.get(), self.var_a_date.get(), self.var_course.get(),
                         self.var_state.get(), self.var_city.get(), self.var_pin.get(),
                         self.txt_address.get("1.0", END).strip(), self.var_roll.get()))
            con.commit()
            messagebox.showinfo("Success", "Student updated successfully")
            self.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'con' in locals(): con.close()

    def delete(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM student WHERE roll=%s", (self.var_roll.get(),))
            con.commit()
            messagebox.showinfo("Deleted", "Record deleted successfully")
            self.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if 'con' in locals(): con.close()

    def clear(self):
        for var in [self.var_roll, self.var_name, self.var_email, self.var_gender, self.var_dob, self.var_contact,
                    self.var_course, self.var_a_date, self.var_state, self.var_city, self.var_pin]:
            var.set("")
        self.txt_address.delete("1.0", END)

    def get_data(self, ev):
        selected = self.student_table.focus()
        data = self.student_table.item(selected)["values"]
        if data:
            self.var_roll.set(data[0])
            self.var_name.set(data[1])
            self.var_email.set(data[2])
            self.var_gender.set(data[3])
            self.var_dob.set(data[4])
            self.var_contact.set(data[5])
            self.var_a_date.set(data[6])
            self.var_course.set(data[7])
            self.var_state.set(data[8])
            self.var_city.set(data[9])
            self.var_pin.set(data[10])
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, data[11])

    def show(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert("", END, values=row)
        except:
            pass
        finally:
            if 'con' in locals(): con.close()

    def fetch_course(self):
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")
            cur = con.cursor()
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            self.course_list = [row[0] for row in rows]
        except:
            self.course_list = []
        finally:
            if 'con' in locals(): con.close()

    def go_home(self):
        if messagebox.askyesno("Confirm", "Do you really want to go Home?", parent=self.window):
            self.window.destroy()
            os.system("python New_Database_Page.py")


# Run
if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()
