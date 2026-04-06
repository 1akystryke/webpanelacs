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

    def supervisor_stop(self):
        result = subprocess.run(
            ["supervisorctl", "stop", "acserver"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip(), result.stderr.strip()

    def supervisor_start(self):
        result = subprocess.run(
            ["supervisorctl", "start", "acserver"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip(), result.stderr.strip()

    def status(self):
        
        result = subprocess.run(
            ["supervisorctl", "status", "acserver"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip(), result.stderr.strip()

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
