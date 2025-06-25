from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import os
import matplotlib.pyplot as plt

class ResultClass:
    def __init__(self, window):
        self.window = window
        self.window.title("Academic Performance Tracker")
        self.window.geometry("1200x700+100+50")  # adjusted for more vertical space
        self.window.config(bg="white")
        self.window.focus_force()
        self.window.resizable(False, False)

        # Variables
        self.var_roll = StringVar()
        self.result_scores = None

        # Title
        title = Label(self.window, text="Student Performance", font=("goudy old style", 20, "bold"),
                      bg="orange", fg="#262626")
        title.pack(side=TOP, fill=X)

        # Roll Number Dropdown
        frame_input = Frame(self.window, bg="white")
        frame_input.place(relx=0.5, rely=0.1, anchor="n")

        lbl_roll = Label(frame_input, text="Select Roll Number:", font=("goudy old style", 18, "bold"), bg="white")
        lbl_roll.grid(row=0, column=0, padx=10, pady=10)

        self.roll_dropdown = ttk.Combobox(frame_input, textvariable=self.var_roll, font=("goudy old style", 18),
                                          state="readonly", width=15)
        self.roll_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.load_roll_numbers()

        btn_submit = Button(frame_input, text="Submit", font=("goudy old style", 18, "bold"), bg="#03a9f4", fg="white",
                            cursor="hand2", command=self.on_submit)
        btn_submit.grid(row=0, column=2, padx=10, pady=10)

        # Data Display
        frame_data = Frame(self.window, bg="white")
        frame_data.place(relx=0.5, rely=0.22, anchor="n")

        self.lbl_name = Label(frame_data, text="Student Name:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_name.pack(anchor="center", pady=5)

        self.lbl_course = Label(frame_data, text="Course:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_course.pack(anchor="center", pady=5)

        self.lbl_ca1 = Label(frame_data, text="CA1:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_ca1.pack(anchor="center", pady=5)

        self.lbl_ca2 = Label(frame_data, text="CA2:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_ca2.pack(anchor="center", pady=5)

        self.lbl_ca3 = Label(frame_data, text="CA3:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_ca3.pack(anchor="center", pady=5)

        self.lbl_ca4 = Label(frame_data, text="CA4:", font=("goudy old style", 18, "bold"), bg="white")
        self.lbl_ca4.pack(anchor="center", pady=5)

        # Buttons Frame
        frame_buttons = Frame(self.window, bg="white")
        frame_buttons.place(relx=0.5, rely=0.87, anchor="center")

        btn_home = Button(frame_buttons, text="Home", font=("goudy old style", 17, "bold"), bg="#FDFF5A",
                          cursor="hand2", command=self.go_home)
        btn_home.pack(pady=5, fill=X)

        btn_clear = Button(frame_buttons, text="Clear", font=("goudy old style", 17, "bold"), bg="#FDFF5A",
                           cursor="hand2", command=self.clear)
        btn_clear.pack(pady=5, fill=X)

        btn_graph = Button(frame_buttons, text="Show Graph", font=("goudy old style", 17, "bold"), bg="#00C853", fg="white",
                           cursor="hand2", command=self.show_graph)
        btn_graph.pack(pady=5, fill=X)

    def load_roll_numbers(self):
        try:
            con = mysql.connector.connect(
                host="localhost", user="root", password="sanjana1432", database="student_system"
            )
            cur = con.cursor()
            cur.execute("SELECT roll FROM student")
            rolls = [str(row[0]) for row in cur.fetchall()]
            self.roll_dropdown['values'] = rolls
            if rolls:
                self.roll_dropdown.current(0)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading roll numbers: {str(ex)}", parent=self.window)

    def go_home(self):
        if messagebox.askyesno("Confirm", "Do you really want to go Home?", parent=self.window):
            self.window.destroy()
            os.system("python New_Database_Page.py")

    def clear(self):
        self.lbl_name.config(text="Student Name:")
        self.lbl_course.config(text="Course:")
        self.lbl_ca1.config(text="CA1:")
        self.lbl_ca2.config(text="CA2:")
        self.lbl_ca3.config(text="CA3:")
        self.lbl_ca4.config(text="CA4:")
        self.result_scores = None

    def on_submit(self):
        roll = self.var_roll.get()

        try:
            con = mysql.connector.connect(
                host="localhost", user="root", password="sanjana1432", database="student_system"
            )
            cur = con.cursor()
            query = """
                SELECT s.name, s.course, r.CA1, r.CA2, r.CA3, r.CA4
                FROM student s
                JOIN result r ON s.roll = r.roll
                WHERE s.roll = %s
            """
            cur.execute(query, (roll,))
            row = cur.fetchone()
            if row:
                self.lbl_name.config(text=f"Student Name: {row[0]}")
                self.lbl_course.config(text=f"Course: {row[1]}")
                self.lbl_ca1.config(text=f"CA1: {row[2]}")
                self.lbl_ca2.config(text=f"CA2: {row[3]}")
                self.lbl_ca3.config(text=f"CA3: {row[4]}")
                self.lbl_ca4.config(text=f"CA4: {row[5]}")
                self.result_scores = [row[2], row[3], row[4], row[5]]
            else:
                messagebox.showinfo("Info", "No record found", parent=self.window)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Database error: {str(ex)}", parent=self.window)

    def show_graph(self):
        if not self.result_scores:
            messagebox.showwarning("Warning", "No data to show graph. Please submit first.", parent=self.window)
            return

        roll = self.var_roll.get()
        labels = ["CA1", "CA2", "CA3", "CA4"]
        scores = [int(s) if s is not None else 0 for s in self.result_scores]

        bar_colors = ['skyblue', 'lightgreen', 'gold', 'salmon']

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, scores, color=bar_colors)

        ax.set_title(f"Performance of Roll No. {roll}")
        ax.set_ylabel("Scores")
        ax.set_ylim(0, max(scores) + 5)

        for bar, score in zip(bars, scores):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f"{score}", ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        plt.show()

# Run GUI
if __name__ == "__main__":
    window = Tk()
    obj = ResultClass(window)
    window.mainloop()
