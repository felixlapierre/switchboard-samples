import requests
from constants import (
    DEVICE_ENDPOINT,
    DECODER_ENDPOINT,
    RECEIVER_DISPLAY_NAME,
    RECEIVER_SERIAL_NUMBER,
    STREAM_ENDPOINT,
)


class Receiver:
    def __init__(
        self,
        display_name=RECEIVER_DISPLAY_NAME,
        serial_number=RECEIVER_SERIAL_NUMBER,
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
                "privateIpAddress": "127.0.0.1",
                "displayName": self.display_name,
                "status": "Running",
            }
            r = requests.post(DEVICE_ENDPOINT, json=device_payload)
            decoder_payload = {
                "serialNumber": self.serial_number,
                "input": [
                    {
                        "channel": {
                            "name": "Sample Receiver Channel 1",
                            "port": self.channel_port,
                        }
                    }
                ],
            }
            r = requests.post(DECODER_ENDPOINT, json=decoder_payload)
            if r.status_code == 200:
                return f"Decoder with serial number {self.serial_number} has been successfully registered."
        else:
            return "Decoder already registered!"

    def get_streams(self):
        response = requests.get(f"{DECODER_ENDPOINT}/{self.serial_number}/streams")
        if response.status_code == 200:
            streams = response.json()
            for stream in streams:
                new_stream_found = True
                for s in self.pending_streams:
                    if stream["id"] == s["id"]:
                        new_stream_found = False
                for s in self.completed_streams:
                    if stream["id"] == s["id"]:
                        new_stream_found = False
                if new_stream_found:
                    self.pending_streams.append(stream)

    def consume_stream(self):
        if self.pending_streams:
            stream = self.pending_streams.pop(0)
            ip = stream["outputChannel"]["encoder"]["device"]["privateIpAddress"]
            port = stream["inputChannel"]["channel"]["port"]
            self.completed_streams.append(stream)
            return (ip, port)
        else:
            return (None, None)
