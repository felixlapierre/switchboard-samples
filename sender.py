import ffmpeg
import click

@click.command()
@click.option('--file', required=True)
@click.option('--ip', required=True)
def send(file, ip):
    stream = ffmpeg.input(file)
    stream = ffmpeg.output(stream, f'udp://{ip}:23000', format = 'mpegts')
    ffmpeg.run(stream)
    # The above simply runs the following command
    # ffmpeg -i <input> -f mpegts udp://<ip>:23000

if __name__ == '__main__':
    send()
