import subprocess, click, requests
from constants import (
    SENDER_DISPLAY_NAME,
    SENDER_SERIAL_NUMBER,
    DEVICE_ENDPOINT,
    ENCODER_ENDPOINT,
)


@click.command()
@click.option("--file", required=True)
@click.option("--ip", required=True)
def send(file, ip):
    # Register the sender with the service
    response = requests.get(f"{DEVICE_ENDPOINT}/{SENDER_SERIAL_NUMBER}")
    if response.status_code == 404:
        device_payload = {
            "serialNumber": SENDER_SERIAL_NUMBER,
            "displayName": SENDER_DISPLAY_NAME,
            "status": "Running",
        }
        r = requests.post(DEVICE_ENDPOINT, json=device_payload)
        encoder_payload = {"serialNumber": SENDER_SERIAL_NUMBER}
        r = requests.post(ENCODER_ENDPOINT, json=encoder_payload)
        if r.status_code == 201:
            click.echo(
                f"Encoder with serial number {SENDER_SERIAL_NUMBER} has been successfully registered."
            )
    # Call ffmpeg
    subprocess.call(
        [
            "ffmpeg",
            "-re",
            "-i",
            file,
            "-f",
            "mpegts",
            "-v",
            "warning",
            "-stats",
            f"srt://{ip}:23000?pkt_size=1316",
        ]
    )


if __name__ == "__main__":
    send()
