# switchboard-samples
Sample senders and receivers to be used with the Switchboard project. https://github.com/felixlapierre/switchboard

# Requirements
* [Python](https://www.python.org) 3.7.3+
* [ffmpeg](https://ffmpeg.org) 4.1.6+

# Usage
1. Create your virtual environment and install the required packages  
`python3 -m venv env`  
`source env/bin/activate` (or `env\Scripts\activate.bat` for Windows users)  
`pip install -r requirements.txt`  

2. Run the video receiver  
`python3 receiver.py --ip <ip>`

3. Run the video sender  
`python3 sender.py --file <file> --ip <ip>`
