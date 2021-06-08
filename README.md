# COVID-19 Vaccination Slot Monitoring Script

### Important: 
- This is a proof of concept project. I do NOT endorse or condone, in any shape or form, automating any monitoring tasks. **Use at your own risk.**
- This CANNOT book slots automatically. It is just to monitor the availablity using the public cowin APIs 
- API Details (read the first paragraph at least): https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2
- And finally, I know code quality may not be great. Suggestions are welcome. 

### Usage:

Download this code as zip, and extract it to some folder like ```C:\temp\covid-vaccine-monitor```. The py files should be in ```C:\temp\covid-vaccine-monitor\src```.
Install all the dependencies with the below. This is a one-time activity (for anyone not familiar with Python)
```
pip install -r requirements.txt
```
Finally, run the script file to get help:
```
python src\vaccine.py -h
```

To know the status of available 'Paid' slots (in loop every 5 min):
```
python src\vaccine.py -s <State Name> -d <District Name>
```

To know the status of available 'Paid' slots (not in loop):
```
python src\vaccine.py -s <State Name> -d <District Name> -l
```

### Notes:
The script can be modified to also show 'Free' slots but default is to show only available 'Paid' slots
The script when run in loop will send a mail (open gmail.py and setup email ids)



### Python 3.7.x Installation in Windows
- Check if Python is already installed by opening command prompt and running ```python --version```.
- If the above command returns ```Python <some-version-number>``` you're probably good - provided version number is above 3.6
- If Python's not installed, command would say something like: ```'python' is not recognized as an internal or external command, operable program or batch file.```
- If so, download the installer from: https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe
- Run that. In the first screen of installer, there will be an option at the bottom to "Add Python 3.7 to Path". Make sure to select it.
- Open command prompt and run ```python --version```. If everything went well it should say ```Python 3.7.x```
- You're all set! 
