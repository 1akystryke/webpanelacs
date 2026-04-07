import subprocess
import os
from pathlib import Path
from typing import Optional
import json


from . import config_process as cp


class Core:
    def __init__(self, server_path: str):
        self.server_path = Path(server_path)
        self.server_exe = self.server_path / "acServer"
        self.process: Optional[subprocess.Popen] = None
        self.running = False
        self.cars_path = os.path.join(server_path, "content", "cars")
        self.tracks_path = os.path.join(server_path, "content", "tracks")
        self.cfg_path = os.path.join(server_path, "cfg")
        self.server_cfg_path = self.cfg_path + "/server_cfg.ini"
        self.entry_list_path = self.cfg_path + "/entry_list.ini"
    def print_exe_path(self):
        print(self.server_exe)

    def supervisor_stop(self):
        result = subprocess.run(
            ["supervisorctl", "stop", "acserver"], capture_output=True, text=True
        )
        return result.stdout.strip(), result.stderr.strip()

    def supervisor_start(self):
        result = subprocess.run(
            ["supervisorctl", "start", "acserver"], capture_output=True, text=True
        )
        return result.stdout.strip(), result.stderr.strip()

    def status(self):

        result = subprocess.run(
            ["supervisorctl", "status", "acserver"], capture_output=True, text=True
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
        tracks = []
        tracks_dirs = os.listdir(self.tracks_path)

        for track in tracks_dirs:
            track_obj = {}

            track_path = os.path.join(self.tracks_path, track)
            folders = os.listdir(track_path)
            folders = [
                x
                for x in os.listdir(track_path)
                if os.path.isdir(os.path.join(track_path, x)) and x != "data"
            ]

            track_obj["id"] = track
            track_obj["layouts"] = folders
            tracks.append(track_obj)

        return tracks

    def set_car_list(self, car_list):
        car_data = [{"MODEL": car} for car in car_list]
        cp.generate_entry_list(car_data, self.entry_list_path)
        cars_string = cp.generate_server_cfg_string_cars(car_data)
        server_data = cp.get_server_config(self.server_cfg_path)
        server_data["SERVER"]["CARS"] = cars_string
        cp.write_new_server_cfg(server_data, self.server_cfg_path)

    def set_server_parameter(self,key,value):
        server_data = cp.get_server_config(self.server_cfg_path)
        server_data["SERVER"][key] = value
        cp.write_new_server_cfg(server_data, self.server_cfg_path)

    def set_race_laps_amount(self,value):
        server_data = cp.get_server_config(self.server_cfg_path)
        server_data["RACE"]["LAPS"] = value
        cp.write_new_server_cfg(server_data, self.server_cfg_path)

    def set_practice_duration(self,value):
        server_data = cp.get_server_config(self.server_cfg_path)
        server_data["PRACTICE"]["TIME"] = value
        cp.write_new_server_cfg(server_data, self.server_cfg_path)

    def set_qualify_duration(self,value):
        server_data = cp.get_server_config(self.server_cfg_path)
        server_data["QUALIFY"]["TIME"] = value
        cp.write_new_server_cfg(server_data, self.server_cfg_path)

    def get_session_state(self):
        car_data = cp.get_current_cars(self.entry_list_path)
        server_data = cp.get_server_config(self.server_cfg_path)

        output_object = {}
        output_object["cars"]= [car["MODEL"] for car in car_data]
        output_object["damage"]=server_data["SERVER"]["DAMAGE_MULTIPLIER"]
        output_object["fuelConsumption"]=server_data["SERVER"]["FUEL_RATE"]
        output_object["layout"]=server_data["SERVER"]["CONFIG_TRACK"]
        output_object["practiceDuration"]=server_data["PRACTICE"]["TIME"]
        output_object["qualifyingDuration"]=server_data["QUALIFY"]["TIME"]
        output_object["raceLaps"]=server_data["RACE"]["LAPS"]
        output_object["sessionType"]="RACE"
        output_object["slots"]=len(car_data)
        output_object["track"]=server_data["SERVER"]["TRACK"]
        output_object["trackVariant"]=server_data["SERVER"]["CONFIG_TRACK"]
        output_object["trackVariants"]=[]
        output_object["tyreWear"]=server_data["SERVER"]["TYRE_WEAR_RATE"]
        output_object["weather"]={
                "ambientTemp": 26,
                "roadTemp": 32
            }
        return output_object
        
