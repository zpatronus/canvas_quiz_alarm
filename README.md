# UMich Canvas Quiz Alarm

The scripts that helped me get an A+ in EECS496.

Originally named "UMich EECS496 Quiz Alarm" (for WN24)

## How to run it

### 1. Use the web service

~~[UM Canvas Quiz Alarm](https://wt.zpatronus.top/quiz_alarm/)~~ stopped service

If you want to deploy the website on your machine, you need to install `requests` and `flask` via `pip`.

To have a production deployment, you may also want to install `gunicorn`.

```bash
# start with flask (dev)
flask --app quiz_alarm_server.py run --debug -h 0.0.0.0
# start with gunicorn (production)
gunicorn -w 1 -b 0.0.0.0:10102 quiz_alarm_server:app
```

### 2. Run it locally with Python script

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then edit `priv_sets_sample.py` to fill necessary info like access token and course id. Remember to rename it to `priv_sets.py`

```shell
python3 quiz_alarm.py
```

The alarm will notify you when the quiz status for this course has changed.
