import json
import logging
import os
import subprocess
import sys
from subprocess import PIPE, TimeoutExpired

import ambient

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)


def main():
    ambient_channel_id = os.environ["AMBIENT_CHANNEL_ID"]
    ambient_write_key = os.environ["AMBIENT_WRITE_KEY"]
    speedtest_server = os.environ.get("SPEEDTEST_SERVER", "21569")

    command = f"speedtest -s {speedtest_server} -f json"
    try:
        proc = subprocess.run(
            command,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            timeout=30,
        )
    except TimeoutExpired:
        logging.error("Timeout Expired: 30 (sec)")
        sys.exit(1)

    if proc.returncode == 0:
        result = json.loads(proc.stdout)

        logging.info(
            f"Server: {result['server']['name']} ({result['server']['country']}, {result['server']['location']})"  # noqa: E501
        )

        download = result["download"]["bandwidth"] / (1000**2 / 8)
        upload = result["upload"]["bandwidth"] / (1000**2 / 8)

        logging.info(f"Download: {download} (Mbps)")
        logging.info(f"Upload: {upload} (Mbps)")

        am = ambient.Ambient(ambient_channel_id, ambient_write_key)
        am.send(
            {
                "d1": download,
                "d2": upload,
            }
        )
    else:
        logging.error(f"return code: {proc.returncode}")
        logging.error(f"stderr: {proc.stderr}")
        sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
