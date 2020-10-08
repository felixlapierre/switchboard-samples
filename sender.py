import ffmpeg
import click
import requests

@click.command()
@click.option('--file', required=True)
@click.option('--ip', required=True)
def send(file, ip):
    # Register the sender with the service
    serial_number = 'd7TxFn7o'
    response = requests.get(f'http://localhost:8080/device/{serial_number}')
    if response.status_code == 200:
        click.echo(f'Device with serial number {serial_number} is already registered.')
    else:
        payload = {'serialNumber': serial_number, 'displayName': 'sample_sender', 'status': 'Running'}
        url = 'http://localhost:8080/device'
        r = requests.post(url, json = payload)
        payload2 = {'serialNumber': serial_number}
        url2 = 'http://localhost:8080/encoder'
        r2 = requests.post(url2, json = payload2)
        if r2.status_code == 201:
            click.echo(f'Encoder with serial number {serial_number} has been successfully registered.')
    
    # The following simply runs the following command
    # ffmpeg -i <input> -f mpegts udp://<ip>:23000
    stream = ffmpeg.input(file)
    stream = ffmpeg.output(stream, f'udp://{ip}:23000', f = 'mpegts', v = 'warning', stats = None)
    ffmpeg.run(stream)

if __name__ == '__main__':
    send()
