import ipaddress, subprocess, time, json
from tkinter import *
from tkinter import filedialog, messagebox
from sender import Sender
from threading import Thread


def on_close_window():
    global continue_polling
    continue_polling = False
    global continue_sending
    continue_sending = False
    root.destroy()


def poll():
    global continue_polling
    continue_polling = True
    while continue_polling:
        time.sleep(5)
        sender.get_streams()


def send_file():
    global continue_sending
    continue_sending = True
    while continue_sending:
        if sender.pending_streams:
            print(
                f"Pending Streams: {sender.pending_streams}, Completed Streams: {sender.completed_streams}"
            )
            stream_id = sender.pending_streams.pop(0)
            ip, port = sender.consume_stream(stream_id)
            if ip and port:
                # To give time for receiver to start
                # Need to find a more elegant solution in the future
                time.sleep(3)
                subprocess.Popen(
                    [
                        "ffmpeg",
                        "-re",
                        "-i",
                        choose_file_entry.get(),
                        "-f",
                        "mpegts",
                        "-v",
                        "warning",
                        f"srt://{ip}:{port}?pkt_size=1316",
                    ]
                )
            sender.completed_streams.append(stream_id)


def send_cam():
    global continue_sending
    continue_sending = True
    with open("config.json") as json_config:
        config = json.load(json_config)
    webcam = config["camera"]["name"]
    while continue_sending:
        if sender.pending_streams:
            print(
                f"Pending Streams: {sender.pending_streams}, Completed Streams: {sender.completed_streams}"
            )
            stream_id = sender.pending_streams.pop(0)
            ip, port = sender.consume_stream(stream_id)
            if ip and port:
                # To give time for receiver to start
                # Need to find a more elegant solution in the future
                time.sleep(3)
                subprocess.Popen(
                    [
                        "ffmpeg",
                        "-f",
                        "dshow",
                        "-i",
                        f"video={webcam}",
                        "-f",
                        "mpegts",
                        "-v",
                        "warning",
                        f"srt://{ip}:{port}?pkt_size=1316",
                    ]
                )
            sender.completed_streams.append(stream_id)


def register():
    sender.display_name = display_name_entry.get()
    sender.serial_number = serial_number_entry.get()
    channel_port = channel_port_entry.get()
    if not is_valid_port(channel_port):
        messagebox.showerror("Error", "Invalid port.")
        return
    else:
        sender.channel_port = channel_port
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


def start():
    if camera_selection.get() == 1:
        Thread(target=poll).start()
        Thread(target=send_cam).start()
    else:
        input_file = choose_file_entry.get()
        if not is_valid_file(input_file):
            messagebox.showerror("Error", "Invalid file type.")
            return
        Thread(target=poll).start()
        Thread(target=send_file).start()


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
channel_port_label = Label(
    registration_label_frame, text="Channel Port", width=20, font=default_font
)
channel_port_entry = Entry(registration_label_frame, width=30, font=default_font)
channel_port_entry.insert(0, sender.channel_port)
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
    streaming_label_frame, text="File", font=default_font, width=13
)
choose_file_entry = Entry(streaming_label_frame, width=40, font=default_font)
browse_button = Button(
    streaming_label_frame,
    text="Browse",
    font=default_font,
    width=20,
    command=browse,
)
camera_label = Label(
    streaming_label_frame, text="Use Camera", font=default_font, width=13
)
camera_selection = IntVar()
camera_checkbox = Checkbutton(
    streaming_label_frame,
    variable=camera_selection,
)
start_button = Button(
    streaming_label_frame,
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
streaming_label_frame.pack(expand="yes", fill="both")
choose_file_label.grid(row=0, column=0)
choose_file_entry.grid(row=0, column=1)
browse_button.grid(row=0, column=2, padx=20, pady=5)
camera_label.grid(row=3, column=0)
camera_checkbox.grid(sticky="W", row=3, column=1)
start_button.grid(row=3, column=2, pady=10)

root.protocol("WM_DELETE_WINDOW", on_close_window)
root.mainloop()