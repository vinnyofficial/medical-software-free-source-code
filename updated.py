import tkinter as tk
from tkinter import ttk, messagebox
import os
import random
import time
from datetime import datetime
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Image

# import win32prin
# import win32api


# User name is vinny
#password is vinny

class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login -  Medical Store")
        self.root.geometry("500x500")
        self.root.resizable(False, False)  # Prevent resizing

        self.create_ui()

    def create_ui(self):
        # Dark Cyberpunk Theme
        self.root.configure(bg="#121212")

        # Real-time Clock
        self.clock_label = tk.Label(self.root, font=("Arial", 12, "bold"), bg="#121212", fg="cyan")
        self.clock_label.pack(pady=10)
        self.update_clock()

        # Left & Right Cyberpunk Elements
        self.create_side_bars()
        self.create_floating_particles()
        self.create_medical_icons()

        # Glassmorphism Styled Frame (Main Login Box)
        frame = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=20, highlightbackground="cyan", highlightthickness=2)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Animated Holographic Title
        self.title_label = tk.Label(frame, text="Login", font=("Arial", 20, "bold"), bg="#1e1e1e")
        self.title_label.pack(pady=10)
        self.animate_title()

        # Neon Glow Input Fields
        self.create_entry(frame, "Username")
        self.username = self.create_entry_widget(frame)

        self.create_entry(frame, "Password")
        self.password = self.create_entry_widget(frame, show="*")

        # Neon Glow Button
        self.login_btn = tk.Button(frame, text="Login", bg="#4caf50", fg="white", font=("Arial", 12, "bold"),
                                   command=self.check_login, relief=tk.FLAT, bd=2, activebackground="#45a049",
                                   highlightbackground="#00FF00", highlightthickness=2, padx=10, pady=5)
        self.login_btn.pack(pady=10, ipadx=10, ipady=5)

    def update_clock(self):
        """ Updates the clock every second """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def animate_title(self):
        colors = ["cyan", "lime", "magenta", "yellow", "red"]
        self.current_color = random.choice(colors)
        self.title_label.config(fg=self.current_color)
        self.root.after(1000, self.animate_title)  # Change color every 1s

    def create_entry(self, frame, text):
        """ Creates labels for input fields with neon styling """
        label = tk.Label(frame, text=text, font=("Arial", 12), bg="#1e1e1e", fg="white")
        label.pack()

    def create_entry_widget(self, frame, show=""):
        """ Creates neon glow entry fields with Enter key binding """
        entry = tk.Entry(frame, width=25, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white",
                        relief=tk.FLAT, show=show, highlightbackground="#00FF00", highlightthickness=2)
        entry.pack(pady=5, ipadx=5, ipady=5)

        # Bind Enter key
        entry.bind("<Return>", self.on_enter_pressed)
        return entry


    def create_side_bars(self):
        """ Adds glowing gradient bars on the left and right """
        left_bar = tk.Canvas(self.root, width=15, height=500, bg="#00FF00", highlightthickness=0)
        left_bar.place(x=0, y=0)

        right_bar = tk.Canvas(self.root, width=15, height=500, bg="#FF00FF", highlightthickness=0)
        right_bar.place(x=585, y=0)

        # Circuit-Like Designs
        for i in range(20):
            left_bar.create_line(5, i * 80, 15, i * 90, fill="cyan", width=2)
            right_bar.create_line(0, i * 70, 10, i * 80, fill="magenta", width=2)

    def create_floating_particles(self):
        """ Creates slow-moving floating dots for a sci-fi effect """
        self.particles = []
        for _ in range(50):
            x = random.randint(20, 580)
            y = random.randint(50, 450)
            size = random.randint(3, 7)
            color = random.choice(["#00FFFF", "#FF00FF", "#00FF00"])
            particle = tk.Label(self.root, text="•", font=("Arial", size), fg=color, bg="#121212")
            particle.place(x=x, y=y)
            self.particles.append((particle, x, y, random.choice([-1, 1]), random.choice([-1, 1])))

        self.animate_particles()

    def animate_particles(self):
        """ Moves particles slowly up and down """
        for i, (particle, x, y, dx, dy) in enumerate(self.particles):
            x += dx
            y += dy
            if x < 20 or x > 580:
                dx *= -1
            if y < 50 or y > 450:
                dy *= -1

            particle.place(x=x, y=y)
            self.particles[i] = (particle, x, y, dx, dy)

        self.root.after(100, self.animate_particles)  # Reduced updates to every 100ms

    def create_medical_icons(self):
        """ Adds small floating medical icons to the sides """
        left_icon = tk.Label(self.root, text="⚕", font=("Arial", 25), fg="cyan", bg="#121212")
        left_icon.place(x=20, y=420)

        right_icon = tk.Label(self.root, text="💊", font=("Arial", 25), fg="magenta", bg="#121212")
        right_icon.place(x=40, y=420)

        self.animate_icons(left_icon, 20, 420, 1)
        self.animate_icons(right_icon, 550, 420, -1)

    def animate_icons(self, widget, x, y, direction):
        """ Makes medical icons float slightly up and down """
        y += direction
        if y < 410 or y > 430:
            direction *= -1


        widget.place(x=x, y=y)
        self.root.after(200, self.animate_icons, widget, x, y, direction)
        
    def on_enter_pressed(self, event):
        """ Handles Enter key to move between fields and trigger login """
        if event.widget == self.username:  # Move focus to password field
            self.password.focus_set()
        elif event.widget == self.password:  # If both fields are filled, trigger login
            if self.username.get() and self.password.get():
                self.check_login()



    def check_login(self):
        if self.username.get() == "vinny" and self.password.get() == "vinny":
            messagebox.showinfo("Success", "Login Successful!")
            self.root.withdraw()  # Hide current window
            new_window = tk.Toplevel(self.root)
            BillingSoftware(new_window)
        else:
            messagebox.showerror("Error", "Invalid Username or Password")


class BillingSoftware:
    def __init__(self, root):
        self.root = root
        self.root.title("Najar Medical Store")
        self.root.geometry("1350x750")
        self.root.configure(bg='#1A1A2E')

        # Gradient Background
        self.create_gradient_background()

        # Neumorphic & Cyberpunk Styling
        def neon_style(widget):
            widget.configure(relief=tk.FLAT, bd=2, bg="#0F3460", fg="white", font=("Arial", 10, "bold"),
                             highlightthickness=3, highlightbackground="#E94560", highlightcolor="#08D9D6")

        # Customer Details
        tk.Label(root, text="Customer Details", fg="#F8E71C", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=20)
        tk.Label(root, text="Customer Name", fg="white", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=50)
        self.customer_name = tk.Entry(root, width=30)
        neon_style(self.customer_name)
        self.customer_name.place(x=150, y=50)

        tk.Label(root, text="Phone No.", fg="white", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=400, y=50)
        self.phone_no = tk.Entry(root, width=30)
        neon_style(self.phone_no)
        self.phone_no.place(x=500, y=50)

        # Product Details
        tk.Label(root, text="Product Details", fg="#F8E71C", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=100)
        tk.Label(root, text="S.No", fg="#08D9D6", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=130)
        self.product_sno = tk.Entry(root, width=10, state='readonly')
        self.product_sno.insert(0, '1')
        neon_style(self.product_sno)
        self.product_sno.place(x=150, y=130)

        tk.Label(root, text="Product Name", fg="#08D9D6", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=160)
        self.product_name = tk.Entry(root, width=30)
        neon_style(self.product_name)
        self.product_name.place(x=150, y=160)

        tk.Label(root, text="Rate", fg="#08D9D6", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=190)
        self.product_rate = tk.Entry(root, width=10)
        neon_style(self.product_rate)
        self.product_rate.place(x=150, y=190)

        tk.Label(root, text="Quantity", fg="#08D9D6", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=220)
        self.product_quantity = tk.Entry(root, width=10)
        neon_style(self.product_quantity)
        self.product_quantity.place(x=150, y=220)

        tk.Label(root, text="Exp Date", fg="#08D9D6", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=250)
        self.product_exp_date = tk.Entry(root, width=15)
        neon_style(self.product_exp_date)
        self.product_exp_date.place(x=150, y=250)

        tk.Label(root, text="Batch", fg="#08D9D6", bg="#1A1A2E", font=("Arial", 10, "bold")).place(x=20, y=280)
        self.product_batch = tk.Entry(root, width=15)
        neon_style(self.product_batch)
        self.product_batch.place(x=150, y=280)

        # Cyberpunk Buttons with Hover Effect
        self.create_animated_button("Add item", self.add_item, 20, 330)
        self.create_animated_button("Generate Bill", self.generate_bill, 200, 330)
        self.create_animated_button("Save Bill", self.save_bill, 20, 370)
        self.create_animated_button("Print Bill", self.print_bill, 200, 370)
        self.create_animated_button("Clear", self.clear_all, 20, 410)
        self.create_animated_button("Exit", root.quit, 200, 410)
        self.create_animated_button("Light Mode", lambda: self.toggle_theme(), 400, 330)
        self.create_animated_button("Random Color", lambda: self.randomize_colors(), 400, 370)

        # Futuristic Bill Area
        self.bill_area = tk.Text(root, width=120, height=40, bg="#0F3460", fg="#F8E71C", font=("Consolas", 10, "bold"), relief=tk.FLAT, bd=2)
        self.bill_area.place(x=600, y=100)

        self.items = []
        self.bill_number = self.generate_unique_bill_number()
        self.serial_number = 1
        self.reset_bill_area()


    def create_gradient_background(self):
        """Creates a gradient background for the billing software."""
        canvas = tk.Canvas(self.root, width=1350, height=750, bg="#1A1A2E", highlightthickness=0)
        canvas.place(x=0, y=0)

        # Create gradient
        for i in range(750):
            color = f"#{int(0x1A + (0x2E - 0x1A) * i / 750):02X}{int(0x1A + (0x2E - 0x1A) * i / 750):02X}{int(0x2E + (0x1A - 0x2E) * i / 750):02X}"
            canvas.create_line(0, i, 1350, i, fill=color)

    def create_animated_button(self, text, command, x, y):
        """Creates a button with hover animation."""
        btn = tk.Button(self.root, text=text, bg="#E94560", fg="white", font=("Arial", 10, "bold"),
                        command=command, relief=tk.FLAT, bd=2, activebackground="#08D9D6", padx=10, pady=5)
        btn.place(x=x, y=y)

        def on_enter(e):
            btn.config(bg="#08D9D6", fg="black")

        def on_leave(e):
            btn.config(bg="#E94560", fg="white")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def generate_unique_bill_number(self):
        """Generates a unique bill number."""
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        bill_numbers_file = os.path.join(desktop_path, "medical", "bill_number.txt")

        if not os.path.exists(bill_numbers_file):
            os.makedirs(os.path.dirname(bill_numbers_file), exist_ok=True)
            open(bill_numbers_file, 'w').close()

        with open(bill_numbers_file, 'r') as file:
            existing_numbers = file.read().splitlines()

        while True:
            number = random.randint(999, 9999)
            if str(number) not in existing_numbers:
                with open(bill_numbers_file, 'a') as file:
                    file.write(f"{number}\n")
                return number

    def reset_bill_area(self):
        """Resets the bill area with headers."""
        try:
            self.bill_area.delete(1.0, tk.END)
            self.bill_area.insert(tk.END, "◆" * 31 + "\n")
            self.bill_area.insert(tk.END, "         your company name\n")
            self.bill_area.insert(tk.END, "      🏆Li.No : xxxxxxxxxx  🏆\n")
            self.bill_area.insert(tk.END, "      📍 Address:  xxxxxxxx ✨\n")
            self.bill_area.insert(tk.END, "       📞 Contact: (+91) xxxxxxxx0\n")
            self.bill_area.insert(tk.END, "◆" * 31 + "\n")
            self.bill_area.insert(tk.END, "📜 Bill No: " + str(self.bill_number) + "\n")            
            self.bill_area.insert(tk.END, "🩺 Doctor/OPD: \n")
            self.bill_area.insert(tk.END, "═" * 55 + "\n")
            self.bill_area.insert(tk.END, "S.No|Product Name|QTY|EXP  |Batch |Rate/  |Total🛍️\n")
            self.bill_area.insert(tk.END, "═" * 55 + "\n")


        except Exception as e:
            print(f"An error occurred: {e}")


    def add_item(self):
        if self.serial_number <= 8:  # Check if the serial number is less than or equal to 8
            serial_number = self.serial_number  # Use the current serial number
            product = self.product_name.get()
            rate = self.product_rate.get()
            quantity = self.product_quantity.get()
            exp_date = self.product_exp_date.get()
            batch = self.product_batch.get()

            if product and rate and quantity and exp_date and batch:
                try:
                    rate = float(rate)
                    quantity = int(quantity)
                    total_price = rate * quantity
                    self.items.append((serial_number, product, quantity, exp_date, batch, rate, total_price))
                    self.bill_area.insert(tk.END, f"{serial_number:<4}|{product:<12}|{quantity:<3}|{exp_date:<5}|{batch:<6}|{rate:<7}|{total_price:<6}|\n")
                    self.serial_number += 1  # Increment the serial number
                    self.product_sno.configure(state='normal')
                    self.product_sno.delete(0, tk.END)
                    self.product_sno.insert(0, str(self.serial_number))
                    self.product_sno.configure(state='readonly')
                except ValueError:
                    messagebox.showerror("Error", "Invalid rate or quantity!")
            else:
                messagebox.showerror("Error", "Invalid product details!")
        else:
            messagebox.showerror("Error", "Serial number limit reached!")

    def generate_bill(self):
        if not self.customer_name.get() or not self.phone_no.get():
            messagebox.showerror("Error", "Please enter customer details!")
        else:
            self.bill_area.insert(tk.END, "-" * 55 + "\n")
            
            total_amount = sum(item[6] for item in self.items)
            self.bill_area.insert(tk.END, f"{'Total--->':<30}{total_amount:<8}\n\n\n\n")
            self.bill_area.insert(tk.END, f"{'Thanks You visit again':<30}{'Signature'}")



    def save_bill(self):
        bill_data = self.bill_area.get(1.0, "end").strip()  
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        medical_bills_path = os.path.join(desktop_path, "medical", "bills")
        pdf_file_path = os.path.join(medical_bills_path, f"{self.customer_name.get().replace(' ', '_')}_{self.bill_number}.pdf")
        os.makedirs(medical_bills_path, exist_ok=True)

        doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        header_style = ParagraphStyle("HeaderStyle", parent=styles["Heading1"], fontSize=14, textColor=colors.darkblue, spaceAfter=10)
        normal_style = styles["Normal"]

        current_date = datetime.now().strftime("%d-%m-%Y")

        def left_align(element, width=300):
            return Table([[element, None]], colWidths=[300, width])  # Adjust width to push content left

        store_name = Paragraph("<b><font size='18' color='darkblue'> MEDICAL STORE</font></b>", header_style)
        elements.append(left_align(store_name))
        elements.append(Spacer(1, 5))

        store_info = Table([
            ["License No:", "RLF1JK2023002539/2549"],
            ["Address:", "Main Market, Sombruna"],
            ["Contact:", "(+91) 6005962180"]
        ], colWidths=[110, 250])

        store_info.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))

        elements.append(left_align(store_info))
        elements.append(Spacer(1, 10))

        bill_info = Paragraph(f"<b>Bill No:</b> {self.bill_number}  |  <b>Date:</b> {current_date}", normal_style)
        doctor_info = Paragraph("<b>Doctor/OPD:</b> ___________", normal_style)

        elements.append(left_align(bill_info))
        elements.append(left_align(doctor_info))
        elements.append(Spacer(1, 10))

        table_data = [["S.No", "Product Name", "QTY", "EXP", "Batch", "Rate", "Total"]]
        total_amount = 0

        for item in self.items:
            serial_number, product, quantity, exp_date, batch, rate, total_price = item
            table_data.append([serial_number, product, quantity, exp_date, batch, rate, f"{total_price:.2f}"])
            total_amount += total_price

        bill_table = Table(table_data, colWidths=[35, 100, 35, 50, 50, 45, 55])
        bill_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, -1), "Courier"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))

        elements.append(left_align(bill_table))
        elements.append(Spacer(1, 10))

        total_table = Table([
            ["Grand Total:", f"₹{total_amount:.2f}"]
        ], colWidths=[150, 100])

        total_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
        ]))

        elements.append(left_align(total_table))
        elements.append(Spacer(1, 5))

        thank_you = Paragraph("<b>Thank You !</b>", normal_style)
        visit_again = Paragraph("<b>Visit Again!</b>", normal_style)
        signature = Paragraph("<b><font color='red'>Signature:</font></b> _______________", normal_style)

        elements.append(left_align(thank_you))
        elements.append(left_align(visit_again))
        elements.append(left_align(signature))

        doc.build(elements)
        messagebox.showinfo("Success", "Bill saved in an elegant left-aligned format!")


    def print_bill(self):
        messagebox.showinfo("This is under construction")
        # bill_data = self.bill_area.get(1.0, tk.END)

        # if not bill_data.strip():
        #     messagebox.showerror("Error", "No bill data to print!")
        #     return

        # printer_name = win32print.GetDefaultPrinter()
        # hprinter = win32print.OpenPrinter(printer_name)
        # printer_info = win32print.GetPrinter(hprinter, 2)
        # pdc = win32print.CreateDC(printer_info["pDriverName"], printer_name, printer_info["pPortName"], {})
        
        # # Print the bill text
        # hdc = win32ui.CreateDC()
        # hdc.CreatePrinterDC(printer_name)
        # hdc.StartDoc('Bill Printout')
        # hdc.StartPage()
        # hdc.TextOut(100, 100, bill_data)
        # hdc.EndPage()
        # hdc.EndDoc()
        # hdc.DeleteDC()

    def clear_all(self):
        self.customer_name.delete(0, tk.END)
        self.phone_no.delete(0, tk.END)
        self.product_name.delete(0, tk.END)
        self.product_rate.delete(0, tk.END)
        self.product_rate.insert(0, '')
        self.product_quantity.delete(0, tk.END)
        self.product_quantity.insert(0, '')
        self.bill_area.delete(1.0, tk.END)
        self.reset_bill_area()
        self.items.clear()
        self.serial_number = 1  # Reset serial number
        self.product_sno.configure(state='normal')
        self.product_sno.delete(0, tk.END)
        self.product_sno.insert(0, '1')
        self.product_sno.configure(state='readonly')

if __name__ == "__main__":
    root = tk.Tk()
    LoginUI(root)
    root.mainloop()
