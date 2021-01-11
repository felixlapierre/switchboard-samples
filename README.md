# switchboard-samples
Sample senders and receivers to be used with the Switchboard project.  
https://github.com/felixlapierre/switchboard

# Requirements
* [Python](https://www.python.org) 3.7.3+
* [ffmpeg](https://ffmpeg.org) 4.1.6+

# Usage
1. Create your virtual environment and install the required packages  
`python -m venv env`  
`source env/bin/activate` (or `env\Scripts\activate.bat` for Windows users)  
`pip install -r requirements.txt`  

2. Change directory to src  
`cd src`

3. Edit the configuration file to choose which camera to use  
`vi config.json`
    * To list all available video devices, run the following command:  
    `ffmpeg -list_devices true -f dshow -i dummy`

4. Run the video receiver  
`python receiver-ui.py`

5. Run the video sender  
`python sender-ui.py`
