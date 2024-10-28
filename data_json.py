import json

def load_gif_data(file_path='gif_data.json'):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_gif_data(data, file_path='gif_data.json'):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
