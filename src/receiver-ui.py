import ipaddress, subprocess
from tkinter import *
from tkinter import filedialog, messagebox
from receiver import Receiver


def register():
    receiver.display_name = display_name_entry.get()
    receiver.serial_number = serial_number_entry.get()
    return_message = receiver.register()
    if return_message == "Decoder already registered!":
        messagebox.showerror("Error", return_message)
    else:
        messagebox.showinfo("Info", return_message)


def receive():
    ip = ip_entry.get()
    port = port_entry.get()
    if not is_valid_ip(ip):
        messagebox.showerror("Error", "Invalid IP address.")
        return
    if not is_valid_port(port):
        messagebox.showerror("Error", "Invalid port.")
        return
    subprocess.Popen(
        [
            "ffplay",
            "-autoexit",
            "-v",
            "warning",
            "-stats",
            f"srt://{ip}:{port}?mode=listener",
        ]
    )


def is_valid_ip(ip):
    if ip == "localhost":
        return True
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    return True


def is_valid_port(port):
    try:
        port = int(port)
        if port >= 1 and port <= 65535:
            return True
        else:
            return False
    except ValueError:
        return False


root = Tk()
root.title("Switchboard - Sample Receiver")
root.geometry("800x400")
root.iconphoto(True, PhotoImage(file=r"public\bean.png"))
receiver = Receiver()
default_font = ("TkDefaultFont", 12)

# Registration section elements
registration_label_frame = LabelFrame(
    root, text="Registration", font=default_font, borderwidth=4
)
display_name_label = Label(
    registration_label_frame, text="Display Name", font=default_font, width=20
)
display_name_entry = Entry(registration_label_frame, width=30, font=default_font)
display_name_entry.insert(0, receiver.display_name)
serial_number_label = Label(
    registration_label_frame, text="Serial Number", font=default_font, width=20
)
serial_number_entry = Entry(registration_label_frame, width=30, font=default_font)
serial_number_entry.insert(0, receiver.serial_number)
register_button = Button(
    registration_label_frame,
    text="Register",
    font=default_font,
    bg="#57A834",
    width=20,
    command=register,
)

# Listening Instructions section elements
listening_label_frame = LabelFrame(
    root, text="Listening Instructions", font=default_font, borderwidth=4
)
ip_label = Label(listening_label_frame, text="IP", font=default_font, width=10)
ip_entry = Entry(listening_label_frame, width=40, font=default_font)
port_label = Label(listening_label_frame, text="Port", font=default_font, width=10)
port_entry = Entry(listening_label_frame, width=40, font=default_font)
receive_button = Button(
    listening_label_frame,
    text="Receive",
    font=default_font,
    bg="#57A834",
    width=20,
    command=receive,
)

# Placing on grid
registration_label_frame.pack(expand="yes", fill="both")
display_name_label.grid(row=0, column=0)
display_name_entry.grid(row=0, column=1, pady=10)
serial_number_label.grid(row=1, column=0)
serial_number_entry.grid(row=1, column=1)
register_button.grid(row=0, column=2, rowspan=2, padx=20, pady=5)
listening_label_frame.pack(expand="yes", fill="both")
ip_label.grid(row=0, column=0, pady=10)
ip_entry.grid(row=0, column=1)
port_label.grid(row=1, column=0)
port_entry.grid(row=1, column=1)
receive_button.grid(row=0, column=2, rowspan=2, padx=20, pady=5)


root.mainloop()