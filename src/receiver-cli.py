import subprocess, click, requests
from constants import (
    RECEIVER_DISPLAY_NAME,
    RECEIVER_SERIAL_NUMBER,
    DEVICE_ENDPOINT,
    DECODER_ENDPOINT,
)


@click.command()
@click.option("--ip", required=True)
def receive(ip):
    # Register the receiver with the service
    response = requests.get(f"{DEVICE_ENDPOINT}/{RECEIVER_SERIAL_NUMBER}")
    if response.status_code == 404:
        device_payload = {
            "serialNumber": RECEIVER_SERIAL_NUMBER,
            "displayName": RECEIVER_DISPLAY_NAME,
            "status": "Running",
        }
        r = requests.post(DEVICE_ENDPOINT, json=device_payload)
        decoder_payload = {"serialNumber": RECEIVER_SERIAL_NUMBER}
        r = requests.post(DECODER_ENDPOINT, json=decoder_payload)
        if r.status_code == 200:
            click.echo(
                f"Decoder with serial number {RECEIVER_SERIAL_NUMBER} has been successfully registered."
            )
    # Call ffplay
    subprocess.call(
        [
            "ffplay",
            "-v",
            "warning",
            "-stats",
            "-exitonkeydown",
            f"srt://{ip}:23000?mode=listener",
        ]
    )


if __name__ == "__main__":
    receive()
