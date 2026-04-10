import configparser
import io


def get_current_cars(path):

    config = configparser.ConfigParser()
    config.optionxform = str

    config.read(path)

    list_cars = []
    for section in config.sections():
        car = {}
        for key in config[section].keys():
            car[key] = config[section][key]
        list_cars.append(car)
    return list_cars


def generate_entry_list(data, out_path):

    config = configparser.ConfigParser()
    config.optionxform = str

    for i, car in enumerate(data):
        section_name = f"CAR_{i}"
        config[section_name] = car
    buffer = io.StringIO()
    config.write(buffer, space_around_delimiters=False)

    result = buffer.getvalue()

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)


def generate_server_cfg_string_cars(data):
    models = str(set([car["MODEL"] for car in data])).replace("', '", ";")[2:-2]
    return models


def get_server_config(path):

    config = configparser.ConfigParser()
    config.optionxform = str

    config.read(path)
    result = {section: dict(config[section]) for section in config.sections()}
    return result


def write_new_server_cfg(data, path):

    config = configparser.ConfigParser()
    config.optionxform = str

    for section, params in data.items():
        config[section] = {k: str(v) for k, v in params.items()}

    buffer = io.StringIO()
    config.write(buffer, space_around_delimiters=False)

    result = buffer.getvalue()
    with open(path, "w", encoding="utf-8") as f:
        f.write(result)
