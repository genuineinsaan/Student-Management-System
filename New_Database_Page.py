from tkinter import *
from tkinter import messagebox, ttk, Toplevel
from tkinter import filedialog
import mysql.connector
import os
import csv
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

class RMS:
    def __init__(self, window):
        self.window = window
        self.window.title("RESULT MANAGEMENT")
        self.window.state("zoomed")
        self.window.config(bg="white")

        # Header logo
        from PIL import Image, ImageTk
        self.logo_dash = ImageTk.PhotoImage(file="Images/logo_p_.png")
        title = Label(self.window, text="ACADEMIC PERFORMANCE TRACKER", padx=10, compound=LEFT,
                      image=self.logo_dash, font=("Roboto", 22, "bold"), bg="#033054", fg="white")
        title.place(x=0, y=0, relwidth=1, height=60)

        # Left Menu
        menu_frame = LabelFrame(self.window, text="MENU", font=("Roboto", 15, "bold"), bg="white")
        menu_frame.place(x=10, y=80, width=260, height=580)

        Button(menu_frame, text="Course Details", font=("Roboto", 13, "bold"), bg="#0b5277", fg="white",
               cursor="hand2", command=self.course).place(x=25, y=30, width=200, height=50)
        Button(menu_frame, text="Student Details", font=("Roboto", 13, "bold"), bg="#0b5277", fg="white",
               cursor="hand2", command=self.student).place(x=25, y=100, width=200, height=50)
        Button(menu_frame, text="Update Result", font=("Roboto", 13, "bold"), bg="#0b5277", fg="white",
               cursor="hand2", command=self.result).place(x=25, y=170, width=200, height=50)
        Button(menu_frame, text="Student Results", font=("Roboto", 13, "bold"), bg="#0b5277", fg="white",
               cursor="hand2", command=self.view_result).place(x=25, y=240, width=200, height=50)
        Button(menu_frame, text="Exit", font=("Roboto", 13, "bold"), bg="#0b5277", fg="white",
               cursor="hand2", command=self.Exit).place(x=25, y=310, width=200, height=50)

        # Tools
        tools_frame = LabelFrame(self.window, text="TOOLS", font=("Roboto", 15, "bold"), bg="white")
        tools_frame.place(relx=1.0, x=-270, y=80, width=260, height=580)

        Button(tools_frame, text="Student's Performance", font=("Roboto", 13, "bold"), bg="#0b5277", fg="white",
               cursor="hand2", command=self.performance).place(x=25, y=30, width=200, height=50)

        Button(tools_frame, text="Send Result", font=("Roboto", 13, "bold"), bg="#0b5277", fg="white",
               cursor="hand2", command=self.send_result).place(x=25, y=100, width=200, height=50)

        # Center image
        screen_width = self.window.winfo_screenwidth()
        image_width = 920
        image_x = (screen_width - image_width) // 2

        self.bg_img = Image.open("Images/bg.jpeg").resize((image_width, 345))
        self.bg_img_tk = ImageTk.PhotoImage(self.bg_img)
        Label(self.window, image=self.bg_img_tk).place(x=image_x, y=200, width=image_width, height=350)

        # Info cards
        self.lbl_student = Label(self.window, text="Total Student\n[0]", font=("Roboto", 18),
                                 bd=10, relief="ridge", bg="#e43b06", fg="white")
        self.lbl_student.place(x=image_x + 70, y=580, width=250, height=100)

        self.lbl_course = Label(self.window, text="Total Course\n[0]", font=("Roboto", 18),
                                bd=10, relief="ridge", bg="#0676ad", fg="white")
        self.lbl_course.place(x=image_x + 600, y=580, width=250, height=100)

        footer = Label(self.window,
                       text="APT - ACADEMIC PERFORMANCE TRACKER\nContact us: 74398xxx64",
                       font=("Roboto", 12), bg="dark blue", fg="white")
        footer.pack(side=BOTTOM, fill=X)

        self.fetch_course()
        self.fetch_student()

    def course(self):
        self.window.destroy()
        os.system("python New_Course_Details_Page.py")

    def student(self):
        self.window.destroy()
        os.system("python New_Student_Details_Page.py")

    def result(self):
        self.window.destroy()
        os.system("python New_Result_Update_Page.py")

    def view_result(self):
        self.window.destroy()
        os.system("python New_Student_Result.py")

    def performance(self):
        self.window.destroy()
        os.system("python New_Student_Performance.py")

    def Exit(self):
        if messagebox.askyesno("Exit", "Do you really want to exit?", parent=self.window):
            self.window.destroy()
            os.system("python New_Login_Page.py")

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="", database="student_system"
        )

    def fetch_course(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.lbl_course.config(text=f"Total Course\n[{len(rows)}]")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching courses:\n{str(ex)}", parent=self.window)
        finally:
            if 'con' in locals():
                con.close()

    def fetch_student(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.lbl_student.config(text=f"Total Student\n[{len(rows)}]")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching students:\n{str(ex)}", parent=self.window)
        finally:
            if 'con' in locals():
                con.close()

    def send_result(self):
        # Create popup
        popup = Toplevel(self.window)
        popup.title("Send Result")
        popup.geometry("400x250")
        popup.grab_set()

        Label(popup, text="Select Roll Number:", font=("Roboto", 14)).pack(pady=10)
        roll_var = StringVar()
        roll_combo = ttk.Combobox(popup, textvariable=roll_var, font=("Roboto", 14), state="readonly", width=20)
        roll_combo.pack()
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT roll FROM student")
            roll_list = [str(r[0]) for r in cur.fetchall()]
            roll_combo['values'] = roll_list
            if roll_list:
                roll_combo.current(0)
        except Exception as ex:
            messagebox.showerror("Error", f"Error loading roll numbers:\n{str(ex)}", parent=popup)

        Label(popup, text="Enter Email Address:", font=("Roboto", 14)).pack(pady=10)
        email_entry = Entry(popup, font=("Roboto", 14), width=30)
        email_entry.pack(pady=5)

        def send():
            roll = roll_var.get()
            to_email = email_entry.get()
            if not roll or not to_email:
                messagebox.showerror("Error", "Both fields are required.", parent=popup)
                return

            try:
                con = self.get_connection()
                cur = con.cursor()
                cur.execute("""
                    SELECT s.name, s.email, s.course, r.CA1, r.CA2, r.CA3, r.CA4 
                    FROM student s 
                    JOIN result r ON s.roll = r.roll 
                    WHERE s.roll = %s
                """, (roll,))
                data = cur.fetchone()
                if not data:
                    messagebox.showerror("Error", "Result not found for this student.", parent=popup)
                    return
                name, student_email, course, ca1, ca2, ca3, ca4 = data

                # CSV
                csv_file = f"Result_{roll}.csv"
                with open(csv_file, "w", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Name", "Course", "CA1", "CA2", "CA3", "CA4"])
                    writer.writerow([name, course, ca1, ca2, ca3, ca4])

                # PDF
                pdf_file = f"Result_{roll}.pdf"
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=14)
                pdf.cell(200, 10, txt=f"Result for {name} (Roll: {roll})", ln=True, align="C")
                pdf.ln(10)
                for i, label in enumerate(["Course", "CA1", "CA2", "CA3", "CA4"]):
                    pdf.cell(200, 10, txt=f"{label}: {data[2 + i]}", ln=True)
                pdf.output(pdf_file)

                # Email
                msg = EmailMessage()
                msg['Subject'] = f"Academic Result for {name}"
                msg['From'] = "youremail@example.com"  # Change
                msg['To'] = to_email
                msg.set_content("Please find attached the result.")

                with open(csv_file, "rb") as f:
                    msg.add_attachment(f.read(), maintype="text", subtype="csv", filename=csv_file)
                with open(pdf_file, "rb") as f:
                    msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_file)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("shashanksrivastava318@gmail.com", "nvfk rcnj vuds ylmn")  # Change
                    smtp.send_message(msg)

                messagebox.showinfo("Success", "Result sent successfully!", parent=popup)
                popup.destroy()

            except Exception as ex:
                messagebox.showerror("Error", f"Failed to send result:\n{str(ex)}", parent=popup)

        Button(popup, text="Send", font=("Roboto", 14, "bold"), bg="green", fg="white", command=send).pack(pady=20)

# Run app
if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()
