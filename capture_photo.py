import json
import pygame.camera

import requests

import datetime
from settings import CREATE_DIRECTORY_URL, LOG_IMAGE_FILE_DIRECTORY, URL_IMAGES


def create_image_directory():
    response = requests.post(CREATE_DIRECTORY_URL)
    return json.loads(response.content)['directory_name']


def capture_photos(cam, server_image_directory_name):
    img = cam.get_image()
    image_file_name = LOG_IMAGE_FILE_DIRECTORY + 'pic.jpg'
    pygame.image.save(img, image_file_name)
    with open(image_file_name) as f:
        requests.post(URL_IMAGES, files={'file': (image_file_name, f)},
                      data={'directory_name': server_image_directory_name})


def start():
    server_image_directory_name = create_image_directory()
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()
    for i in range(5):
        capture_photos(cam, server_image_directory_name)


start()
