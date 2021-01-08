import ipaddress, subprocess, time
from tkinter import *
from tkinter import filedialog, messagebox
from receiver import Receiver
from threading import Thread


def on_close_window():
    global continue_polling
    continue_polling = False
    global continue_receiving
    continue_receiving = False
    root.destroy()


def poll():
    global continue_polling
    continue_polling = True
    while continue_polling:
        time.sleep(5)
        receiver.get_streams()


def receive():
    global continue_receiving
    continue_receiving = True
    while continue_receiving:
        if receiver.pending_streams:
            print(
                f"Pending Streams: {receiver.pending_streams}, Completed Streams: {receiver.completed_streams}"
            )
            stream_id = receiver.pending_streams.pop(0)
            ip, port = receiver.consume_stream(stream_id)
            if ip and port:
                subprocess.Popen(
                    [
                        "ffplay",
                        "-v",
                        "warning",
                        f"srt://{ip}:{port}?mode=listener",
                    ]
                )
            receiver.completed_streams.append(stream_id)


def register():
    receiver.display_name = display_name_entry.get()
    receiver.serial_number = serial_number_entry.get()
    channel_port = channel_port_entry.get()
    if not is_valid_port(channel_port):
        messagebox.showerror("Error", "Invalid port.")
        return
    else:
        receiver.channel_port = channel_port
    return_message = receiver.register()
    if return_message == "Decoder already registered!":
        messagebox.showerror("Error", return_message)
    else:
        messagebox.showinfo("Info", return_message)


def start():
    Thread(target=poll).start()
    Thread(target=receive).start()


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
channel_port_label = Label(
    registration_label_frame, text="Channel Port", width=20, font=default_font
)
channel_port_entry = Entry(registration_label_frame, width=30, font=default_font)
channel_port_entry.insert(0, receiver.channel_port)
register_button = Button(
    registration_label_frame,
    text="Register",
    font=default_font,
    bg="#57A834",
    width=20,
    command=register,
)

# Listening Instructions section elements
listening_label_frame = LabelFrame(root, font=default_font, borderwidth=4)
start_button = Button(
    listening_label_frame,
    text="Start",
    font=default_font,
    bg="#57A834",
    width=20,
    command=start,
)

# Placing on grid
registration_label_frame.pack(expand="yes", fill="both")
display_name_label.grid(row=0, column=0)
display_name_entry.grid(row=0, column=1, pady=10)
serial_number_label.grid(row=1, column=0)
serial_number_entry.grid(row=1, column=1)
channel_port_label.grid(row=2, column=0)
channel_port_entry.grid(row=2, column=1, pady=10)
register_button.grid(row=0, column=2, rowspan=2, padx=20, pady=5)
listening_label_frame.pack(expand="yes", fill="both")
start_button.place(relx=0.5, rely=0.5, anchor=CENTER)

root.protocol("WM_DELETE_WINDOW", on_close_window)
root.mainloop()