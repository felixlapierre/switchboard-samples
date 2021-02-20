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
        channel_1_port="20002",
        channel_2_port="20003",
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
            decoder_payload = {
                "serialNumber": self.serial_number,
                "input": [
                    {
                        "channel": {
                            "name": "Sample Receiver Channel 1",
                            "port": self.channel_1_port,
                        }
                    },
                    {
                        "channel": {
                            "name": "Sample Receiver Channel 2",
                            "port": self.channel_2_port,
                        }
                    },
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
            self.streams = response.json()

    def consume_stream(self):
        for stream in self.streams:
            stream_id = str(stream["id"])
            if stream_id not in self.processes:
                if (
                    stream["outputChannel"]["encoder"]["device"]["publicIpAddress"]
                    == "0:0:0:0:0:0:0:1"
                ):
                    ip = stream["outputChannel"]["encoder"]["device"]["privateIpAddress"]
                else:
                    ip = stream["outputChannel"]["encoder"]["device"]["publicIpAddress"]
                port = stream["inputChannel"]["channel"]["port"]
                is_rendezvous = bool(stream["isRendezvous"])
                return (stream_id, ip, port, is_rendezvous)
        return (None, None, None, None)

    def delete_stream(self, stream_id):
        r = requests.delete(f"{STREAM_ENDPOINT}/{stream_id}")
        if r.status_code == 200:
            return True
        else:
            return False
