import click
import subprocess
import requests

@click.command()
@click.option('--ip', required=True)
def receive(ip):
    # Register the receiver with the service
    serial_number = 'z7VBn9aK'
    response = requests.get(f'http://localhost:8080/device/{serial_number}')
    if response.status_code == 200:
        click.echo(f'Device with serial number {serial_number} is already registered.')
    else:
        payload = {'serialNumber': serial_number, 'displayName': 'sample_receiver', 'status': 'Running'}
        url = 'http://localhost:8080/device'
        r = requests.post(url, json = payload)
        payload2 = {'serialNumber': serial_number}
        url2 = 'http://localhost:8080/decoder'
        r2 = requests.post(url2, json = payload2)
        if r2.status_code == 201:
            click.echo(f'Decoder with serial number {serial_number} has been successfully registered.')
    
    # The following simply runs the following command
    # ffplay -autoexit udp://<ip>:23000
    subprocess.call(['ffplay', '-v', 'warning', '-stats', f'udp://{ip}:23000'])

if __name__ == '__main__':
    receive()
