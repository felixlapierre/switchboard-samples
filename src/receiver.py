import requests
from constants import (
    DEVICE_ENDPOINT,
    DECODER_ENDPOINT,
    RECEIVER_DISPLAY_NAME,
    RECEIVER_SERIAL_NUMBER,
)


class Receiver:
    def __init__(
        self, display_name=RECEIVER_DISPLAY_NAME, serial_number=RECEIVER_SERIAL_NUMBER
    ):
        self.display_name = display_name
        self.serial_number = serial_number

    def register(self):
        response = requests.get(f"{DEVICE_ENDPOINT}/{self.serial_number}")
        if response.status_code == 404:
            device_payload = {
                "serialNumber": self.serial_number,
                "displayName": self.display_name,
                "status": "Running",
            }
            r = requests.post(DEVICE_ENDPOINT, json=device_payload)
            decoder_payload = {"serialNumber": self.serial_number}
            r = requests.post(DECODER_ENDPOINT, json=decoder_payload)
            if r.status_code == 201:
                return f"Decoder with serial number {self.serial_number} has been successfully registered."
        else:
            return "Decoder already registered!"