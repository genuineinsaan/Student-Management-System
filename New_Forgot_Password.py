from tkinter import *
from tkinter import messagebox
import mysql.connector
import os

class PasswordResetApp:
    def __init__(self, master):
        self.window = master
        self.window.title("Reset Password - Student System")
        self.window.state("zoomed")
        self.window.config(bg="#E3F2FD")

        Label(self.window, text="RESET PASSWORD", font=("Roboto", 24, "bold"), bg="#E3F2FD", fg="#222").pack(pady=30)

        Button(self.window, text="Forgot Password", font=("Roboto", 14), bg="#FFC107", command=self.forget_password).pack(pady=20)
        Button(self.window, text="Back to Login", font=("Roboto", 14), bg="#2196F3", fg="white", command=self.go_login).pack(pady=10)

    def go_login(self):
        self.window.destroy()
        os.system("python New_Login_Page.py")  

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="student_system"
        )

    def center_window(self, win, width, height):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def forget_password(self):
        phone_window = Toplevel(self.window)
        phone_window.title("Verify Contact Number")
        self.center_window(phone_window, 400, 200)
        phone_window.config(bg="light blue")

        Label(phone_window, text="Enter your registered contact number:", font=("Roboto", 12), bg="white").pack(pady=20)
        phone_entry = Entry(phone_window, font=("Roboto", 12))
        phone_entry.pack(pady=5)

        Button(phone_window, text="Submit", font=("Roboto", 12), bg="#4CAF50", fg="white",
               command=lambda: self.show_security_question(phone_window, phone_entry.get())).pack(pady=15)

    def show_security_question(self, parent_window, contact_no):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email, question, answer FROM employee WHERE contact = %s", (contact_no,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Contact number not found!", parent=parent_window)
                return

            parent_window.destroy()
            email, question, current_answer = row

            reset_win = Toplevel(self.window)
            reset_win.title("Reset Password")
            self.center_window(reset_win, 500, 550)
            reset_win.config(bg="light blue")

            Label(reset_win, text=f"Email: {email}", font=("Roboto", 10), bg="light blue", fg="gray").pack(pady=(10, 5))

            Label(reset_win, text="Security Question", font=("Roboto", 12, "bold"), bg="white").pack(pady=(10, 5))
            question_var = StringVar(value=question)
            OptionMenu(reset_win, question_var, question).pack(pady=5)

            Label(reset_win, text="Answer", font=("Roboto", 12), bg="white").pack(pady=5)
            answer_entry = Entry(reset_win, font=("Roboto", 12))
            answer_entry.pack(pady=5)

            Label(reset_win, text="New Password", font=("Roboto", 12), bg="white").pack(pady=10)
            new_pass_entry = Entry(reset_win, show="*", font=("Roboto", 12))
            new_pass_entry.pack(pady=5)

            change_question_var = IntVar()
            Checkbutton(reset_win, text="Change Security Question?", variable=change_question_var,
                        bg="white", font=("Roboto", 10)).pack(pady=10)

            Label(reset_win, text="New Security Question", font=("Roboto", 12), bg="white").pack()
            new_q_var = StringVar()
            new_q_menu = OptionMenu(reset_win, new_q_var, "your pet name", "your birth hour",
                                    "your favourite food", "your favourite teacher")
            new_q_menu.pack()

            Label(reset_win, text="New Answer", font=("Roboto", 12), bg="white").pack()
            new_a_entry = Entry(reset_win, font=("Roboto", 12))
            new_a_entry.pack(pady=5)

            Button(reset_win, text="Reset", font=("Roboto", 12, "bold"), bg="#4CAF50", fg="white",
                   command=lambda: self.update_password(email, answer_entry.get(), new_pass_entry.get(),
                                                        change_question_var.get(), new_q_var.get(),
                                                        new_a_entry.get(), reset_win)).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if 'conn' in locals():
                conn.close()

    def update_password(self, email, answer, new_pass, change_sec, new_q, new_a, window):
        if not answer or not new_pass:
            messagebox.showerror("Error", "Answer and New Password are required.", parent=window)
            return

        try:
            conn = self.get_connection()
            cur = conn.cursor()

            if change_sec:
                if not new_q or not new_a:
                    messagebox.showerror("Error", "New security question and answer required.", parent=window)
                    return
                cur.execute("UPDATE employee SET password=%s, question=%s, answer=%s WHERE email=%s",
                            (new_pass, new_q, new_a, email))
            else:
                cur.execute("UPDATE employee SET password=%s, answer=%s WHERE email=%s",
                            (new_pass, answer, email))

            conn.commit()
            messagebox.showinfo("Success", "Password reset successful.", parent=window)
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}", parent=window)
        finally:
            if 'conn' in locals():
                conn.close()

# Run the GUI
if __name__ == "__main__":
    root = Tk()
    app = PasswordResetApp(root)
    root.mainloop()
