import ipaddress, subprocess, time, json
from tkinter import *
from tkinter import filedialog, messagebox
from constants import SRT_SCHEME, LOCAL_HOST, UDP_SCHEME
from sender import Sender
from threading import Thread

INTERNAL_PORT = 5000


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


def send(use_webcam):
    global continue_sending
    continue_sending = True
    with open("config.json") as json_config:
        config = json.load(json_config)
    webcam = config["camera"]["name"]
    while continue_sending:
        check_status()
        (
            stream_id,
            ip,
            output_channel_port,
            input_channel_port,
            is_rendezvous,
        ) = sender.consume_stream()
        if ip and input_channel_port:
            time.sleep(3)
            if is_rendezvous:
                sender.processes[stream_id] = [
                    subprocess.Popen(
                        [
                            "srt-live-transmit",
                            f"{UDP_SCHEME}://{LOCAL_HOST}:{INTERNAL_PORT}",
                            f"{SRT_SCHEME}://{ip}:{input_channel_port}?mode=rendezvous",
                        ]
                    )
                ]
                ffmpeg_url = f"{UDP_SCHEME}://{LOCAL_HOST}:{INTERNAL_PORT}?pkt_size=1316"
                sender.processes[stream_id].insert(
                    0, start_ffmpeg(use_webcam, webcam, ffmpeg_url, output_channel_port)
                )
                INTERNAL_PORT += 1
            else:
                ffmpeg_url = f"{SRT_SCHEME}://{ip}:{input_channel_port}?pkt_size=1316"
                sender.processes[stream_id] = [
                    start_ffmpeg(use_webcam, webcam, ffmpeg_url, output_channel_port)
                ]


def start_ffmpeg(use_webcam, webcam, ffmpeg_url, output_channel_port):
    if use_webcam:
        return start_ffmpeg_webcam(webcam, ffmpeg_url)
    else:
        return start_ffmpeg_file(ffmpeg_url, output_channel_port)


def start_ffmpeg_file(url, port):
    if port == int(sender.channel_1_port):
        file = choose_file_1_entry.get()
    else:
        file = choose_file_2_entry.get()
    return subprocess.Popen(
        [
            "ffmpeg",
            "-re",
            "-i",
            file,
            "-f",
            "mpegts",
            "-v",
            "fatal",
            url,
        ]
    )


def start_ffmpeg_webcam(webcam, url):
    return subprocess.Popen(
        [
            "ffmpeg",
            "-f",
            "dshow",
            "-i",
            f"video={webcam}",
            "-f",
            "mpegts",
            "-v",
            "fatal",
            url,
        ]
    )


def check_status():
    stream_ids = list(sender.processes.keys())
    for stream_id in stream_ids:
        stream_deleted = True
        for stream in sender.streams:
            if stream["id"] == int(stream_id):
                stream_deleted = False
        if stream_deleted:
            for process in sender.processes[stream_id]:
                process.terminate()
            del sender.processes[stream_id]


def register():
    sender.display_name = display_name_entry.get()
    sender.serial_number = serial_number_entry.get()
    channel_1_port = channel_1_port_entry.get()
    channel_2_port = channel_2_port_entry.get()
    if not is_valid_port(channel_1_port) or not is_valid_port(channel_2_port):
        messagebox.showerror("Error", "Invalid port.")
        return
    else:
        sender.channel_1_port = channel_1_port
        sender.channel_2_port = channel_2_port
    return_message = sender.register()
    if return_message == "Encoder already registered!":
        messagebox.showerror("Error", return_message)
    else:
        messagebox.showinfo("Info", return_message)


def browse(file):
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select File")
    if root.filename:
        if file == 1:
            choose_file_1_entry.delete(0, "end")
            choose_file_1_entry.insert(0, root.filename)
        else:
            choose_file_2_entry.delete(0, "end")
            choose_file_2_entry.insert(0, root.filename)


def start():
    if camera_selection.get() == 1:
        Thread(target=poll).start()
        Thread(target=send, args=(True,)).start()
    else:
        input_file_1 = choose_file_1_entry.get()
        input_file_2 = choose_file_2_entry.get()
        if not input_file_1 or not input_file_2:
            messagebox.showerror("Error", "Missing one or both files.")
            return
        if not is_valid_file(input_file_1) or not is_valid_file(input_file_2):
            messagebox.showerror("Error", "Invalid file type.")
            return
        Thread(target=poll).start()
        Thread(target=send, args=(False,)).start()


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
root.iconphoto(True, PhotoImage(file=r"public/bean.png"))
sender = Sender()
default_font = ("TkDefaultFont", 12)

# Registration section elements
registration_label_frame = LabelFrame(root, text="Registration", font=default_font, borderwidth=4)
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
channel_1_port_label = Label(
    registration_label_frame, text="Channel 1 Port", width=20, font=default_font
)
channel_1_port_entry = Entry(registration_label_frame, width=30, font=default_font)
channel_1_port_entry.insert(0, sender.channel_1_port)
channel_2_port_label = Label(
    registration_label_frame, text="Channel 2 Port", width=20, font=default_font
)
channel_2_port_entry = Entry(registration_label_frame, width=30, font=default_font)
channel_2_port_entry.insert(0, sender.channel_2_port)
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
choose_file_1_label = Label(streaming_label_frame, text="File 1", font=default_font, width=13)
choose_file_1_entry = Entry(streaming_label_frame, width=40, font=default_font)
browse_button_1 = Button(
    streaming_label_frame,
    text="Browse",
    font=default_font,
    width=20,
    command=lambda: browse(1),
)
choose_file_2_label = Label(streaming_label_frame, text="File 2", font=default_font, width=13)
choose_file_2_entry = Entry(streaming_label_frame, width=40, font=default_font)
browse_button_2 = Button(
    streaming_label_frame,
    text="Browse",
    font=default_font,
    width=20,
    command=lambda: browse(2),
)
camera_label = Label(streaming_label_frame, text="Use Camera", font=default_font, width=13)
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
channel_1_port_label.grid(row=2, column=0)
channel_1_port_entry.grid(row=2, column=1, pady=10)
channel_2_port_label.grid(row=3, column=0)
channel_2_port_entry.grid(row=3, column=1)
register_button.grid(row=0, column=2, rowspan=2, padx=20, pady=5)
streaming_label_frame.pack(expand="yes", fill="both")
choose_file_1_label.grid(row=0, column=0)
choose_file_1_entry.grid(row=0, column=1)
browse_button_1.grid(row=0, column=2, padx=20, pady=5)
choose_file_2_label.grid(row=1, column=0)
choose_file_2_entry.grid(row=1, column=1)
browse_button_2.grid(row=1, column=2, padx=20, pady=5)
camera_label.grid(row=3, column=0)
camera_checkbox.grid(sticky="W", row=3, column=1)
start_button.grid(row=3, column=2, pady=10)

root.protocol("WM_DELETE_WINDOW", on_close_window)
root.mainloop()