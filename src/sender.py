import requests
from constants import (
    DEVICE_ENDPOINT,
    ENCODER_ENDPOINT,
    SENDER_DISPLAY_NAME,
    SENDER_SERIAL_NUMBER,
    STREAM_ENDPOINT,
)


class Sender:
    def __init__(
        self,
        display_name=SENDER_DISPLAY_NAME,
        serial_number=SENDER_SERIAL_NUMBER,
        channel_1_port="20000",
        channel_2_port="20001",
        streams=None,
        processes=None,
    ):
        self.display_name = display_name
        self.serial_number = serial_number
        self.channel_1_port = channel_1_port
        self.channel_2_port = channel_2_port
        self.streams = streams if streams is not None else []
        self.processes = processes if processes is not None else {}

    def register(self):
        response = requests.get(f"{DEVICE_ENDPOINT}/{self.serial_number}")
        if response.status_code == 404:
            device_payload = {
                "serialNumber": self.serial_number,
                "privateIpAddress": "127.0.0.1",
                "displayName": self.display_name,
                "status": "Running",
            }
            r = requests.post(DEVICE_ENDPOINT, json=device_payload)
            encoder_payload = {
                "serialNumber": self.serial_number,
                "output": [
                    {
                        "channel": {
                            "name": "Sample Sender Channel 1",
                            "port": self.channel_1_port,
                        }
                    },
                    {
                        "channel": {
                            "name": "Sample Sender Channel 2",
                            "port": self.channel_2_port,
                        }
                    },
                ],
            }
            r = requests.post(ENCODER_ENDPOINT, json=encoder_payload)
            if r.status_code == 200:
                return f"Encoder with serial number {self.serial_number} has been successfully registered."
        else:
            return "Encoder already registered!"

    def get_streams(self):
        response = requests.get(f"{ENCODER_ENDPOINT}/{self.serial_number}/streams")
        if response.status_code == 200:
            self.streams = response.json()

    def consume_stream(self):
        for stream in self.streams:
            stream_id = str(stream["id"])
            if stream_id not in self.processes:
                if (
                    stream["inputChannel"]["decoder"]["device"]["publicIpAddress"]
                    == "0:0:0:0:0:0:0:1"
                ):
                    ip = stream["inputChannel"]["decoder"]["device"]["privateIpAddress"]
                else:
                    ip = stream["inputChannel"]["decoder"]["device"]["publicIpAddress"]
                output_channel_port = stream["outputChannel"]["channel"]["port"]
                input_channel_port = stream["inputChannel"]["channel"]["port"]
                is_rendezvous = bool(stream["isRendezvous"])
                return (
                    stream_id,
                    ip,
                    output_channel_port,
                    input_channel_port,
                    is_rendezvous,
                )
        return (None, None, None, None, None)
