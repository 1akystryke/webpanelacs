import subprocess
import os
import json
from pathlib import Path
import json


from . import config_process as cp


class Core:
    """Core class for managing AC server"""

    def __init__(self, server_path: str):
        self.server_path = Path(server_path)
        self.cars_path = self.server_path / "content" / "cars"
        self.tracks_path = self.server_path / "content" / "tracks"
        self.cfg_path = self.server_path / "cfg"
        self.server_cfg_path = self.cfg_path / "server_cfg.ini"
        self.entry_list_path = self.cfg_path / "entry_list.ini"
        self.log_path = "/var/log/"
        self.map_parameters_name = {
            "name": ["SERVER", "NAME"],
            "password": ["SERVER", "PASSWORD"],
            "adminPassword": ["SERVER", "ADMIN_PASSWORD"],
            "udpPort": ["SERVER", "UDP_PORT"],
            "tcpPort": ["SERVER", "TCP_PORT"],
            "httpPort": ["SERVER", "HTTP_PORT"],
            "damage": ["SERVER", "DAMAGE_MULTIPLIER"],
            "fuelConsumption": ["SERVER", "FUEL_RATE"],
            "layout": ["SERVER", "CONFIG_TRACK"],
            "practiceDuration": ["PRACTICE", "TIME"],
            "qualifyingDuration": ["QUALIFY", "TIME"],
            "raceLaps": ["RACE", "LAPS"],
            "track": ["SERVER", "TRACK"],
            "trackVariant": ["SERVER", "CONFIG_TRACK"],
            "tyreWear": ["SERVER", "TYRE_WEAR_RATE"],
            "sunAngle": ["SERVER", "SUN_ANGLE"],
            "pickupMode": ["SERVER", "PICKUP_MODE_ENABLED"],
            "loopMode": ["SERVER", "LOOP_MODE"],
            "allowedTyresOut": ["SERVER", "ALLOWED_TYRES_OUT"],
            "legalTyres": ["SERVER", "LEGAL_TYRES"],
            "absAllowed": ["SERVER", "ABS_ALLOWED"],
            "tcAllowed": ["SERVER", "TC_ALLOWED"],
            "stabilityAllowed": ["SERVER", "STABILITY_ALLOWED"],
            "autoclutchAllowed": ["SERVER", "AUTOCLUTCH_ALLOWED"],
            "tyreBlanketsAllowed": ["SERVER", "TYRE_BLANKETS_ALLOWED"],
            "forceVirtualMirror": ["SERVER", "FORCE_VIRTUAL_MIRROR"],
            "registerToLobby": ["SERVER", "REGISTER_TO_LOBBY"],
            "maxClients": ["SERVER", "MAX_CLIENTS"],
        }
        self.map_weather_param_names = {
            "graphics": "GRAPHICS",
            "baseTemperatureAmbient": "BASE_TEMPERATURE_AMBIENT",
            "baseTemperatureRoad": "BASE_TEMPERATURE_ROAD",
            "variationAmbient": "VARIATION_AMBIENT",
            "variationRoad": "VARIATION_ROAD",
        }

    def supervisor_stop(self):
        try:
            result = subprocess.run(
                ["supervisorctl", "stop", "acserver"],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            return ("error", e.stderr)
        return result.stdout.strip(), result.stderr.strip()

    def supervisor_start(self):
        try:
            result = subprocess.run(
                ["supervisorctl", "start", "acserver"],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            return ("error", e.stderr)
        return result.stdout.strip(), result.stderr.strip()

    def supervisor_restart(self):
        try:
            result = subprocess.run(
                ["supervisorctl", "restart", "acserver"],
                capture_output=True,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            return ("error", e.stderr)
        return result.stdout.strip(), result.stderr.strip()

    def supervisor_status(self):

        result = subprocess.run(
            ["supervisorctl", "status", "acserver"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip(), result.stderr.strip()

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

    def list_weathers(self):
        with open("core/resources/weather.json", "r", encoding="utf-8") as f:
            weather = json.load(f)
        return weather

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
                if os.path.isdir(os.path.join(track_path, x))
                and x not in ["data", "extension", "skins", "ui"]
            ]

            track_obj["id"] = track
            track_obj["layouts"] = folders
            tracks.append(track_obj)

        return tracks

    def set_car_list(self, car_list):
        car_data = [
            {
                "MODEL": car["id"],
                "RESTRICTOR": car["restrictor"],
                "BALLAST": car["ballast"],
                "SKIN": car["skin"],
            }
            for car in car_list
        ]
        cp.generate_entry_list(car_data, self.entry_list_path)
        cars_string = cp.generate_server_cfg_string_cars(car_data)
        server_data = cp.get_server_config(self.server_cfg_path)
        server_data["SERVER"]["CARS"] = cars_string
        cp.write_new_server_cfg(server_data, self.server_cfg_path)

    def apply_session(self, data):
        server_data = cp.get_server_config(self.server_cfg_path)

        server_data = {k: v for k, v in server_data.items() if not "WEATHER_" in k}

        for param in data.keys():
            if param not in self.map_parameters_name.keys():
                continue
            key1, key2 = self.map_parameters_name[param]
            if param == "maxClients":
                server_data[key1][key2] = len(data["cars"])
            else:
                server_data[key1][key2] = data[param]

        for index, weather in enumerate(data["weather"]):
            server_data[f"WEATHER_{index}"] = {}
            for key in weather.keys():
                server_data[f"WEATHER_{index}"][self.map_weather_param_names[key]] = (
                    weather[key]
                )

        cp.write_new_server_cfg(server_data, self.server_cfg_path)

    def get_session_state(self):
        car_data = cp.get_current_cars(self.entry_list_path)
        server_data = cp.get_server_config(self.server_cfg_path)

        output_object = {}
        output_object["cars"] = [
            {
                "model": car["MODEL"],
                "restrictor": car.get("RESTRICTOR", ""),
                "ballast": car.get("BALLAST", ""),
                "skin": car.get("SKIN", ""),
            }
            for car in car_data
        ]
        for parameter in self.map_parameters_name.keys():
            key1, key2 = self.map_parameters_name[parameter]
            output_object[parameter] = server_data[key1][key2]

        output_object["weather"] = []
        for key in server_data.keys():
            if "WEATHER_" in key:
                tmp_obj = {}
                for sub_key in self.map_weather_param_names.keys():
                    tmp_obj[sub_key] = server_data[key][
                        self.map_weather_param_names[sub_key]
                    ]
                output_object["weather"].append(tmp_obj)

        return output_object

    def get_ac_server_logs(self):
        ac_log_path = self.log_path + "acserver.log"
        ac_err_path = self.log_path + "acserver.err"
        flask_log_path = self.log_path + "servicepy.log"
        flask_err_path = self.log_path + "servicepy.err"
        with open(ac_log_path) as f:
            log_file_content = f.read()
        return log_file_content.split("\n")
