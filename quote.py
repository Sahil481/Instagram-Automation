import requests
import os
import random
from exceptions import QuoteAPIException

def get_api_data(api_url):
    try:
        # Make a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            api_data = response.json()
            return api_data
        else:
            raise QuoteAPIException(f"Couldn't retrieve quote {response.status_code}")
    except Exception as e:
        raise QuoteAPIException(e)

def get_quote():
    api_url = "https://api.quotable.io/random"
    tries = 1
    while tries < 4:
        try:
            data = get_api_data(api_url=api_url)
            break
        except Exception as e:
            print(e)
            tries += 1
            
    return data

def get_random_font_relative(directory_path):
    try:
        # Get a list of all files in the directory
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        # Check if there are any files in the directory
        if not files:
            print("No files found in the directory.")
            return None

        # Choose a random file from the list
        random_file = random.choice(files)

        # Get the relative path of the chosen file
        relative_file_path = os.path.relpath(os.path.join(directory_path, random_file), directory_path)

        return relative_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_font():
    directory_path = "fonts"
    random_font = "fonts/" + get_random_font_relative(directory_path=directory_path)
    return random_font


'''This code maybe used later
def get_opposite_color(dominant_color):
    # Calculate the opposite color by subtracting each RGB component from 255
    opposite_color = [255 - component for component in dominant_color]

    return tuple(opposite_color)
'''