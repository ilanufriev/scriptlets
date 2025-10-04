# Seqtimer

Seqtimer is a simple script that plays time after a given amount of seconds have passed. It can be used to time sequences of periods. For example:

```bash
python3 ./seqtimer '30:15:30'
```

Will play sound after 30 seconds, then after 15 seconds, then after 30 seconds again. After that it stops.

## Sound files

The script needs two audiofiles to be placed in the same folder as the .py file: "begin.wav" and "end.wav". Those sounds should be short, since playback time is capped at 1 second (although that is very easy to change.
