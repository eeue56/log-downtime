# log-downtime
Log the times when your network connection goes down. Your downtime will be stored in a CSV file named after the year, month, day and hour which you started the program. 

It will attempt to ping randomly one of the URLs you provide every minute. When it fails, it will log that failure.


## Install

You need Python 3.6 for this.

```
git clone https://github.com/eeue56/log-downtime
cd log-downtime
pip3 install -r requirements.txt
``` 

## Run

```
python3.6 main.py --url https://www.google.com
```