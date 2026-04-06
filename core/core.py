import subprocess
import os
import json
from pathlib import Path
from typing import Optional


class Core:
    def __init__(self, server_path: str):
        self.server_path = Path(server_path)
        self.server_exe = self.server_path / "acServer"
        self.process: Optional[subprocess.Popen] = None
        self.running = False

        self.cars_path = os.path.join(server_path, "content", "cars")
        self.tracks_path = os.path.join(server_path, "content", "tracks")
        self.cfg_path = os.path.join(server_path, "cfg")

    def list_cars(self):
        default_cars: list = None
        server_cars = os.listdir(self.cars_path)

        with open("core/resources/cars.json", "r", encoding="utf-8") as f:
            cars = json.load(f)
            default_cars = cars

        mod_cars = set.difference(set(server_cars), (x["id"] for x in default_cars))
        
        result_cars = default_cars
        for mod_car in list(mod_cars):
            ui_path = os.path.join(self.cars_path, mod_car, "ui", "ui_car.json")
            with open(ui_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
                content = content.replace("\t", "").replace("\n", "")
                data = json.loads(content)
                result_cars.append({"id": mod_car, "name": data["name"]})
            
        return result_cars

    def list_tracks(self):
        return os.listdir(self.tracks_path)

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
