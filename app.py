import json
import os
import subprocess
from subprocess import PIPE

import ambient


def main():
    ambient_channel_id = os.environ["AMBIENT_CHANNEL_ID"]
    ambient_write_key = os.environ["AMBIENT_WRITE_KEY"]
    speedtest_server = os.environ.get("SPEEDTEST_SERVER", "21569")

    command = f"speedtest -s {speedtest_server} -f json"
    proc = subprocess.run(
        command,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        timeout=30,
    )
    result = json.loads(proc.stdout)

    am = ambient.Ambient(ambient_channel_id, ambient_write_key)
    am.send(
        {
            "d1": result["download"]["bandwidth"] / (1000**2 / 8),
            "d2": result["upload"]["bandwidth"] / (1000**2 / 8),
        }
    )


if __name__ == "__main__":
    main()
