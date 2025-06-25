from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os

class ReportClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Academic Performance Tracker")
        self.window.geometry("1350x480+80+170")
        self.window.config(bg="white")
        self.window.focus_force()

        # TITLE
        title = Label(self.window, text="Student Result", font=("goudy old style", 30, "bold"), bg="light blue", fg="#262626")
        title.place(x=10, y=15, relwidth=1, height=50)

        # SEARCH
        self.var_search = StringVar()
        Label(self.window, text="Search By Roll NO", font=("goudy old style", 15, "bold"), bg="white").place(x=370, y=100)

        self.txt_search = ttk.Combobox(self.window, textvariable=self.var_search, font=("goudy old style", 20), state='readonly')
        self.txt_search.place(x=530, y=100, width=200)

        Button(self.window, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white",
               cursor="hand2", command=self.search).place(x=750, y=100, width=120, height=35)
        Button(self.window, text="Clear", font=("goudy old style", 20, "bold"), bg="lightgray",
               activebackground="lightgray", cursor="hand2", command=self.clear_fields).place(x=410, y=420, width=120, height=35)
        Button(self.window, text="Delete", font=("goudy old style", 20, "bold"), bg="red",
               activebackground="red", cursor="hand2", command=self.delete_record).place(x=560, y=420, width=120, height=35)
        Button(self.window, text="Home", font=("goudy old style", 20, "bold"), bg="#FDFF5A",
               cursor="hand2", command=self.os).place(x=710, y=420, width=120, height=35)

        # HEADERS
        Label(self.window, text="Roll No", font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2).place(x=100, y=200, width=150, height=50)
        Label(self.window, text="Name", font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2).place(x=250, y=200, width=250, height=50)
        Label(self.window, text="Course", font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2).place(x=500, y=200, width=150, height=50)
        Label(self.window, text="CA1", font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2).place(x=650, y=200, width=150, height=50)
        Label(self.window, text="CA2", font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2).place(x=800, y=200, width=150, height=50)
        Label(self.window, text="CA3", font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2).place(x=950, y=200, width=150, height=50)
        Label(self.window, text="CA4", font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2).place(x=1100, y=200, width=150, height=50)

        # DATA LABELS
        self.roll = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2)
        self.roll.place(x=100, y=250, width=150, height=50)
        self.name = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2)
        self.name.place(x=250, y=250, width=250, height=50)
        self.course = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2)
        self.course.place(x=500, y=250, width=150, height=50)
        self.CA1 = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2)
        self.CA1.place(x=650, y=250, width=150, height=50)
        self.CA2 = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2)
        self.CA2.place(x=800, y=250, width=150, height=50)
        self.CA3 = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2)
        self.CA3.place(x=950, y=250, width=150, height=50)
        self.CA4 = Label(self.window, font=("goudy old style", 15, "bold"), bg="white", relief="groov", bd=2)
        self.CA4.place(x=1100, y=250, width=150, height=50)

        # Populate combobox at startup
        self.fetch_rolls()

    def fetch_rolls(self):
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")
            cur = con.cursor()
            cur.execute("SELECT roll FROM result")
            rolls = [str(row[0]) for row in cur.fetchall()]
            self.txt_search['values'] = rolls
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching roll numbers: {str(ex)}", parent=self.window)

    def os(self):
        if messagebox.askyesno("Confirm", "Do you really want to go Home?", parent=self.window):
            self.window.destroy()
            os.system("python New_Database_Page.py")

    def search(self):
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Roll No should be required", parent=self.window)
                return

            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")
            cur = con.cursor()
            cur.execute("SELECT * FROM result WHERE roll=%s", (self.var_search.get(),))
            row = cur.fetchone()
            if row:
                self.roll.config(text=row[1])
                self.name.config(text=row[2])
                self.course.config(text=row[3])
                self.CA1.config(text=row[4])
                self.CA2.config(text=row[5])
                self.CA3.config(text=row[6])
                self.CA4.config(text=row[7])
            else:
                messagebox.showinfo("Info", "No record found", parent=self.window)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.window)

    def clear_fields(self):
        self.var_search.set("")
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.CA1.config(text="")
        self.CA2.config(text="")
        self.CA3.config(text="")
        self.CA4.config(text="")

    def delete_record(self):
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Roll No should be required", parent=self.window)
                return

            con = mysql.connector.connect(host="localhost", user="root", password="sanjana1432", database="student_system")
            cur = con.cursor()
            cur.execute("DELETE FROM result WHERE roll=%s", (self.var_search.get(),))
            con.commit()
            messagebox.showinfo("Success", "Record deleted successfully", parent=self.window)
            self.clear_fields()
            self.fetch_rolls()  # Refresh combobox after deletion
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.window)

# GUI RUN
if __name__ == "__main__":
    window = Tk()
    obj = ReportClass(window)
    window.mainloop()
