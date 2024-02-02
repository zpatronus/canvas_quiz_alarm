# UMich EECS496 Quiz Alarm (for WN24)

## How to run it

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
