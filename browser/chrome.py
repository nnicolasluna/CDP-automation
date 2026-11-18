
import subprocess
import os


class Chrome:

    def __init__(self, chrome_path=None, port=9222):

        self.chrome_path = chrome_path or (
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )

        self.port = port

        self.profile = os.path.join(
            os.environ["TEMP"],
            "chrome-cdp"
        )

        self.process = None

    def start(self, url="https://www.google.com"):

        command = [
            self.chrome_path,
            f"--remote-debugging-port={self.port}",
            f"--user-data-dir={self.profile}",
            "--no-first-run",
            "--no-default-browser-check",
            url
        ]

        self.process = subprocess.Popen(command)

        print("Chrome iniciado")

    def close(self):

        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

            print("Chrome cerrado")
