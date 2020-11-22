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
        channel_port="20000",
        pending_streams=None,
        completed_streams=None,
    ):
        self.display_name = display_name
        self.serial_number = serial_number
        self.channel_port = channel_port
        self.pending_streams = pending_streams if pending_streams is not None else []
        self.completed_streams = (
            completed_streams if completed_streams is not None else []
        )

    def register(self):
        response = requests.get(f"{DEVICE_ENDPOINT}/{self.serial_number}")
        if response.status_code == 404:
            device_payload = {
                "serialNumber": self.serial_number,
                "ipAddress": "127.0.0.1",
                "displayName": self.display_name,
                "status": "Running",
            }
            r = requests.post(DEVICE_ENDPOINT, json=device_payload)
            encoder_payload = {
                "serialNumber": self.serial_number,
                "outputs": [
                    {
                        "channel": {
                            "name": "Sample Sender Channel 1",
                            "port": self.channel_port,
                        }
                    }
                ],
            }
            r = requests.post(ENCODER_ENDPOINT, json=encoder_payload)
            if r.status_code == 201:
                return f"Encoder with serial number {self.serial_number} has been successfully registered."
        else:
            return "Encoder already registered!"

    def get_streams(self):
        response = requests.get(STREAM_ENDPOINT)
        if response.status_code == 200:
            streams = response.json()
            for id in streams:
                if id not in self.pending_streams and id not in self.completed_streams:
                    self.pending_streams.append(id)

    def consume_stream(self, id):
        response = requests.get(f"{STREAM_ENDPOINT}/{id}")
        if response.status_code == 200:
            stream_info = response.json()
            if (
                stream_info["outputChannel"]["encoder"]["serialNumber"]
                == self.serial_number
            ):
                ip = stream_info["inputChannel"]["decoder"]["device"]["ipAddress"]
                port = stream_info["inputChannel"]["port"]
                return (ip, port)
            else:
                return (None, None)
