import subprocess
import os
from pathlib import Path
from typing import Optional



class Core:
    def __init__(self, server_path: str):
        self.server_path = Path(server_path)
        self.server_exe = self.server_path / "acServer"
        self.process: Optional[subprocess.Popen] = None
        self.running = False

    def print_exe_path(self):
        print(self.server_exe)

    def start(self):
        os.chdir(self.server_path)
        cmd = [str(self.server_exe)]

        with subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True,
        ) as self.process:
            self.running = True

        print(f"Server is running (PID: {self.process.pid})")

    def status(self):
        pass

    def shutdown(self):
        self.running = False

        if self.process:
            self.process.terminate()
            try:
                self.process.wait(5)
                print("Server treminated")
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("Timeout: server killed")

    def restart(self):
        pass

    def wait(self):
        if self.process:
            self.process.wait()
