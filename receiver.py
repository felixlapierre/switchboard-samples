import click
import subprocess

@click.command()
@click.option('--ip', required=True)
def receive(ip):
    subprocess.call(['ffplay', '-autoexit', f'udp://{ip}:23000'])
    # The above simply runs the following command
    # ffplay -autoexit udp://<ip>:23000

if __name__ == '__main__':
    receive()
