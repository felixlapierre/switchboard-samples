import ipaddress, subprocess
from tkinter import *
from tkinter import filedialog, messagebox
from sender import Sender


def register():
    sender.display_name = display_name_entry.get()
    sender.serial_number = serial_number_entry.get()
    return_message = sender.register()
    if return_message == "Encoder already registered!":
        messagebox.showerror("Error", return_message)
    else:
        messagebox.showinfo("Info", return_message)


def browse():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select File")
    if root.filename:
        choose_file_entry.delete(0, "end")
        choose_file_entry.insert(0, root.filename)


def send():
    input_file = choose_file_entry.get()
    ip = ip_entry.get()
    port = port_entry.get()
    if not is_valid_file(input_file):
        messagebox.showerror("Error", "Invalid file type.")
        return
    if not is_valid_ip(ip):
        messagebox.showerror("Error", "Invalid IP address.")
        return
    if not is_valid_port(port):
        messagebox.showerror("Error", "Invalid port.")
        return
    subprocess.Popen(
        [
            "ffmpeg",
            "-re",
            "-i",
            input_file,
            "-f",
            "mpegts",
            "-v",
            "warning",
            "-stats",
            f"srt://{ip}:{port}?pkt_size=1316",
        ]
    )


def is_valid_file(input_file):
    valid_file_extensions = ("mp4", "webm")
    if input_file.endswith(valid_file_extensions):
        return True
    return False


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
root.title("Switchboard - Sample Sender")
root.geometry("800x400")
root.iconphoto(True, PhotoImage(file=r"public\bean.png"))
sender = Sender()
default_font = ("TkDefaultFont", 12)

# Registration section elements
registration_label_frame = LabelFrame(
    root, text="Registration", font=default_font, borderwidth=4
)
display_name_label = Label(
    registration_label_frame,
    text="Display Name",
    font=default_font,
    width=20,
)
display_name_entry = Entry(registration_label_frame, width=30, font=default_font)
display_name_entry.insert(0, sender.display_name)
serial_number_label = Label(
    registration_label_frame,
    text="Serial Number",
    font=default_font,
    width=20,
)
serial_number_entry = Entry(registration_label_frame, width=30, font=default_font)
serial_number_entry.insert(0, sender.serial_number)
register_button = Button(
    registration_label_frame,
    text="Register",
    font=default_font,
    bg="#57A834",
    width=20,
    command=register,
)

# Streaming Instructions section elements
streaming_label_frame = LabelFrame(
    root, text="Streaming Instructions", font=default_font, borderwidth=4
)
choose_file_label = Label(
    streaming_label_frame, text="File", font=default_font, width=10
)
choose_file_entry = Entry(streaming_label_frame, width=40, font=default_font)
ip_label = Label(streaming_label_frame, text="IP", font=default_font, width=10)
ip_entry = Entry(streaming_label_frame, width=40, font=default_font)
browse_button = Button(
    streaming_label_frame,
    text="Browse",
    font=default_font,
    width=20,
    command=browse,
)
port_label = Label(streaming_label_frame, text="Port", font=default_font, width=10)
port_entry = Entry(streaming_label_frame, width=40, font=default_font)
send_button = Button(
    streaming_label_frame,
    text="Send",
    font=default_font,
    bg="#57A834",
    width=20,
    command=send,
)

# Placing on grid
registration_label_frame.pack(expand="yes", fill="both")
display_name_label.grid(row=0, column=0)
display_name_entry.grid(row=0, column=1, pady=10)
serial_number_label.grid(row=1, column=0)
serial_number_entry.grid(row=1, column=1)
register_button.grid(row=0, column=2, rowspan=2, padx=20, pady=5)
streaming_label_frame.pack(expand="yes", fill="both")
choose_file_label.grid(row=0, column=0)
choose_file_entry.grid(row=0, column=1)
browse_button.grid(row=0, column=2, padx=20, pady=5)
ip_label.grid(row=1, column=0)
ip_entry.grid(row=1, column=1)
port_label.grid(row=2, column=0)
port_entry.grid(row=2, column=1, pady=10)
send_button.grid(row=3, column=2)

root.mainloop()