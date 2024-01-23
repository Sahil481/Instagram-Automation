import cv2
import requests
from PIL import Image
import random
from Quote2Image import ImgObject
import numpy as np
from exceptions import ImageAPIException
from constants import BACKGROUND_FILE_PATH, IMAGE_TAGS, OUTPUT_FILE
from datetime import datetime
import os


def get_random_image_data():
    tags = IMAGE_TAGS
    random_tag = random.choice(tags)
    random_page = random.randrange(1, 6)
    api_url=f"https://api.pexels.com/v1/search?query={random_tag}&per_page=30&orientation=square&page={random_page}"
    api_key = "EyW7mCoREYBoymhZHqEupcVFooriGNaxlI1nE26GMI2Ho36URhtMm7mW"
    
    try:
        # Define headers with the API key
        headers = {'Authorization': api_key}

        # Make a GET request to the API with the specified headers
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            api_data = response.json()
            return api_data["photos"]
        else:
            raise ImageAPIException(f"The following page could not be found. {response.status_code}")
    except Exception as e:
        raise ImageAPIException(e)
        
def save_image_from_url(url):
    try:
        # Make a GET request to the image URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open a local file with write-binary mode and save the image content
            with open(BACKGROUND_FILE_PATH, 'wb') as file:
                file.write(response.content)
            print(f"Image saved to {BACKGROUND_FILE_PATH}")
        else:
            raise ImageAPIException(f"Couldn't retrive image {response.status_code}")
    except Exception as e:
        raise ImageAPIException(e)
        
def compress_and_resize_image(target_resolution=(1080, 1080), quality=100):
    try:
        # Open the image
        original_image = Image.open(BACKGROUND_FILE_PATH)

        # Resize the image while maintaining the aspect ratio
        original_image.thumbnail(target_resolution)

        # Save the compressed and resized image
        original_image.save(BACKGROUND_FILE_PATH, 'JPEG', quality=quality)

        print(f"Image saved to {BACKGROUND_FILE_PATH}")
    except Exception as e:
        raise ImageAPIException(e)
        
def adjust_gamma(gamma=1.7):
    img = cv2.imread(BACKGROUND_FILE_PATH)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    try:
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        
        lut_img = cv2.LUT(image, table)
        cv2.imwrite(BACKGROUND_FILE_PATH, lut_img)
        print(f"gamma corrected and saved to {BACKGROUND_FILE_PATH}")
    except Exception as e:
        raise ImageAPIException(e)
        
def apply_background_blur(blur_strength=25):
    try:
        # Read the input image
        original_image = cv2.imread(BACKGROUND_FILE_PATH)

        # Blur the image
        blurred = cv2.GaussianBlur(original_image, (blur_strength, blur_strength), 0)

        # Save the result
        cv2.imwrite(BACKGROUND_FILE_PATH, blurred)
        print(f"Image with background blur saved to {BACKGROUND_FILE_PATH}")
    except Exception as e:
        raise ImageAPIException(e)
        
def download_and_save_image():
    image_received = False
    while not image_received:
        try:
            random_image_data = get_random_image_data()
            image_received = True
        except ImageAPIException as e:
            image_received = False
            print(e.message)
    
    random_index = random.randrange(0, len(random_image_data))
    random_image = random_image_data[random_index]["src"]["original"]
    
    tries = 1
    while tries < 4:
        try:
            save_image_from_url(random_image)
            break
        except Exception as e:
            print(e)
            tries += 1
        
def generate_background_image():
    download_and_save_image()
    tries = 1
    while tries < 4:
        try:
            compress_and_resize_image()
            break
        except Exception as e:
            print(e)
            tries += 1
            
    tries = 1
    while tries < 4:
        try:
            adjust_gamma()
            break
        except Exception as e:
            print(e)
            tries += 1

    bg=ImgObject(image=BACKGROUND_FILE_PATH)
    return bg


def determine_brightness_image():
    image = Image.open(BACKGROUND_FILE_PATH)
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def determine_text_color():
    brightness = determine_brightness_image()

    # Decide text color based on brightness
    text_color = (255, 255, 255) if brightness < .5 else (0, 0, 0)

    return text_color


def create_picture_folder():
    # Get the current date
    current_date = datetime.now().date()

    # Format the date as a string
    date_string = current_date.strftime("%Y/%m/%d")

    # Create the folder path based on the date
    folder_path = os.path.join(OUTPUT_FILE, date_string)

    # Create the folder and its parent directories if they don't exist
    os.makedirs(folder_path, exist_ok=True)

    return folder_path

def save_picture_path():
    # Create a unique filename for the picture (you may want to use a timestamp or other unique identifier)
    picture_filename = "quote.jpeg"

    # Create the folder for the current date
    folder_path = create_picture_folder()

    # Save the picture in the corresponding folder
    picture_path = os.path.join(folder_path, picture_filename)

    # Save your picture (replace this with your actual code to save the picture)
    # For example: image_data.save(picture_path)
    print(f"Picture saved at: {picture_path}")
    return picture_path
