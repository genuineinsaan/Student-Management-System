from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

class CourseClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Academic Performance Tracker")
        self.window.state("zoomed")
        self.window.config(bg="#f0f4f7")

        self.var_cid = StringVar()
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()

        # Title
        title = Label(self.window, text="📘 Manage Course Details", font=("Roboto", 24, "bold"), bg="#003366", fg="white")
        title.pack(side=TOP, fill=X)

        # === Left Section (Form) ===
        form_bg = Frame(self.window, bg="white", bd=2, relief=RIDGE)
        form_bg.place(x=40, y=80, width=850, height=500)

        Label(form_bg, text="Course ID:", font=("Roboto", 14, "bold"), bg="white").place(x=30, y=30)
        Entry(form_bg, textvariable=self.var_cid, font=("Roboto", 13), bg="#e7f0fd").place(x=220, y=30, width=550)

        Label(form_bg, text="Course Name:", font=("Roboto", 14, "bold"), bg="white").place(x=30, y=90)
        Entry(form_bg, textvariable=self.var_course, font=("Roboto", 13), bg="#e7f0fd").place(x=220, y=90, width=550)

        Label(form_bg, text="Course Duration:", font=("Roboto", 14, "bold"), bg="white").place(x=30, y=150)
        Entry(form_bg, textvariable=self.var_duration, font=("Roboto", 13), bg="#e7f0fd").place(x=220, y=150, width=550)

        Label(form_bg, text="Course Charges:", font=("Roboto", 14, "bold"), bg="white").place(x=30, y=210)
        Entry(form_bg, textvariable=self.var_charges, font=("Roboto", 13), bg="#e7f0fd").place(x=220, y=210, width=550)

        Label(form_bg, text="Course Description:", font=("Roboto", 14, "bold"), bg="white").place(x=30, y=270)
        self.txt_Description = Text(form_bg, font=("Roboto", 12), bg="#e7f0fd")
        self.txt_Description.place(x=220, y=270, width=550, height=100)

        # Buttons
        Button(form_bg, text="Save", font=("Roboto", 12, "bold"), bg="#1976D2", fg="white", command=self.add).place(x=220, y=400, width=100)
        Button(form_bg, text="Update", font=("Roboto", 12, "bold"), bg="#388E3C", fg="white", command=self.update).place(x=340, y=400, width=100)
        Button(form_bg, text="Delete", font=("Roboto", 12, "bold"), bg="#D32F2F", fg="white", command=self.delete).place(x=460, y=400, width=100)
        Button(form_bg, text="Clear", font=("Roboto", 12, "bold"), bg="#455A64", fg="white", command=self.clear).place(x=580, y=400, width=100)
        Button(form_bg, text="Home", font=("Roboto", 12, "bold"), bg="#FBC02D", fg="black", command=self.go_home).place(x=700, y=400, width=100)

        # === Image Below Form ===
        self.course_img = Image.open("C:/Users/shash/OneDrive/Desktop/Academic Performance Tracker !!/Images/course_details_resized.png")
        self.course_img_tk = ImageTk.PhotoImage(self.course_img)
        Label(self.window, image=self.course_img_tk, bg="#f0f4f7").place(x=260, y=600)

        # === Right Section (Table + Course Count) ===
        table_frame = Frame(self.window, bg="white", bd=2, relief=RIDGE)
        table_frame.place(x=920, y=80, width=550, height=600)

        # Label for total courses
        self.course_count_lbl = Label(table_frame, text="Total Courses Registered: 0", font=("Roboto", 13, "bold"), bg="white", fg="#333")
        self.course_count_lbl.place(x=10, y=10)

        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        self.Coursetable = ttk.Treeview(
            table_frame,
            columns=("Cid", "name", "duration", "charges", "description"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.Coursetable.xview)
        scrolly.config(command=self.Coursetable.yview)

        self.Coursetable.heading("Cid", text="Course ID")
        self.Coursetable.heading("name", text="Course Name")
        self.Coursetable.heading("duration", text="Duration")
        self.Coursetable.heading("charges", text="Charges")
        self.Coursetable.heading("description", text="Description")
        self.Coursetable["show"] = 'headings'
        self.Coursetable.column("Cid", width=80)
        self.Coursetable.column("name", width=120)
        self.Coursetable.column("duration", width=100)
        self.Coursetable.column("charges", width=100)
        self.Coursetable.column("description", width=250)
        self.Coursetable.place(x=10, y=50, width=520, height=520)
        self.Coursetable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_system"
        )

    def go_home(self):
        if messagebox.askyesno("Confirm", "Do you really want to go Home?", parent=self.window):
            self.window.destroy()
            os.system("python New_Database_Page.py")

    def get_data(self, ev):
        selected = self.Coursetable.focus()
        values = self.Coursetable.item(selected, "values")
        if values:
            self.var_cid.set(values[0])
            self.var_course.set(values[1])
            self.var_duration.set(values[2])
            self.var_charges.set(values[3])
            self.txt_Description.delete("1.0", END)
            self.txt_Description.insert(END, values[4])

    def add(self):
        if self.var_cid.get() == "" or self.var_course.get() == "":
            messagebox.showerror("Error", "Course ID and Course Name are required!", parent=self.window)
            return
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM course WHERE Cid=%s", (self.var_cid.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Course ID already exists!", parent=self.window)
            else:
                cur.execute("INSERT INTO course (Cid, name, duration, charges, description) VALUES (%s, %s, %s, %s, %s)", (
                    self.var_cid.get(), self.var_course.get(), self.var_duration.get(),
                    self.var_charges.get(), self.txt_Description.get("1.0", END).strip()
                ))
                con.commit()
                messagebox.showinfo("Success", "Course added successfully", parent=self.window)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Database Error:\n{str(ex)}", parent=self.window)

    def update(self):
        if self.var_cid.get() == "":
            messagebox.showerror("Error", "Select a course to update", parent=self.window)
            return
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("UPDATE course SET name=%s, duration=%s, charges=%s, description=%s WHERE Cid=%s", (
                self.var_course.get(), self.var_duration.get(), self.var_charges.get(),
                self.txt_Description.get("1.0", END).strip(), self.var_cid.get()
            ))
            con.commit()
            messagebox.showinfo("Success", "Course updated successfully", parent=self.window)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Update Error:\n{str(ex)}", parent=self.window)

    def delete(self):
        if self.var_cid.get() == "":
            messagebox.showerror("Error", "Select a course to delete", parent=self.window)
            return
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM course WHERE Cid=%s", (self.var_cid.get(),))
            con.commit()
            messagebox.showinfo("Success", "Course deleted successfully", parent=self.window)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Delete Error:\n{str(ex)}", parent=self.window)

    def clear(self):
        self.var_cid.set("")
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.txt_Description.delete("1.0", END)

    def show(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.Coursetable.delete(*self.Coursetable.get_children())
            for row in rows:
                self.Coursetable.insert("", END, values=row)
            # Update course count
            self.course_count_lbl.config(text=f"Total Courses Registered: {len(rows)}")
        except Exception as ex:
            messagebox.showerror("Error", f"Fetch Error:\n{str(ex)}", parent=self.window)

# Run
if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
