import sys
import time
import subprocess


SOUND_BEGIN_PERIOD = "begin.wav"
SOUND_END_SESSION = "end.wav"


def play_sound(filename, playtime, volume):
    try:
        result = subprocess.run(
                    [
                        "ffplay",
                        "-nodisp",
                        "-autoexit",
                        "-t",
                        str(playtime),
                        "-volume",
                        str(volume),
                        filename,
                    ],
                    capture_output=True,
                    text=True)

        if result.returncode != 0:
            print("Playing sound failed. Here is stdout:")
            print(result.stdout)
            print("Here is stderr:")
            print(result.stderr)

    except FileNotFoundError as e:
        e.errno
        print(f"Executable '{e.filename}' does not exist")


def file_exists(filename):
    try:
        with open(filename, mode="r"):
            return True
    except FileNotFoundError:
        return False


def wait_for(secs: float):
    print("Timer started!")
    time.sleep(secs / 2)
    print(f"{secs / 2} seconds left")
    time.sleep(secs / 2)


def main(args):
    playtime = 1.0
    volume = 100

    if len(args) < 2:
        print(f"Usage ./{args[0]} '30:30:30'")
        print("This will give you three 30-second time periods")
        return 0

    if not file_exists(SOUND_BEGIN_PERIOD):
        print(f"File {SOUND_BEGIN_PERIOD} does not exist")
        return 0

    if not file_exists(SOUND_END_SESSION):
        print(f"File {SOUND_END_SESSION} does not exist")
        return 0

    try:
        periods = [float(p.strip()) for p in args[1].split(":")]
    except ValueError:
        print("You should input time in format 'ss:ss:ss', " +
              "where 's' stands for seconds")
        return 1

    for i in range(0, len(periods)):
        print(f"Period #{i + 1}: {periods[i]} seconds")
        play_sound(SOUND_BEGIN_PERIOD, playtime, volume)
        wait_for(periods[i])

    print("Done!")
    play_sound(SOUND_END_SESSION, 1.0, volume)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
