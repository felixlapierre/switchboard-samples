import requests
from constants import (
    DEVICE_ENDPOINT,
    ENCODER_ENDPOINT,
    SENDER_DISPLAY_NAME,
    SENDER_SERIAL_NUMBER,
)


class Sender:
    def __init__(
        self, display_name=SENDER_DISPLAY_NAME, serial_number=SENDER_SERIAL_NUMBER
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
            encoder_payload = {"serialNumber": self.serial_number}
            r = requests.post(ENCODER_ENDPOINT, json=encoder_payload)
            if r.status_code == 201:
                return f"Encoder with serial number {self.serial_number} has been successfully registered."
        else:
            return "Encoder already registered!"