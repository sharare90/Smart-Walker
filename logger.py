from datetime import datetime
import requests
import json
from urllib import urlopen
import os.path
from pathlib import Path
from enum import Enum
import copy
from functools import total_ordering

#import pygame.camera

from settings import (TEST_ENVIRONMENT, SERVER_URL, POST_URL,
CREATE_FILE_URL, LOG_FILE_DIRECTORY, LOG_IMAGE_FILE_DIRECTORY, FILE_HEADER, UPLOAD_FREQUENCY)

class LoggerEnum(Enum):
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        else:
            return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        else:
            return NotImplemented

class DataSources(LoggerEnum):
    WEIGHT = 1
    GYROSCOPE = 2
    PROXIMITY = 3

class DataTypes(LoggerEnum):
    TIME = 1
    FR = 2
    FL = 3
    RR = 4
    RL = 5
    HEAD = 6
    ROLL = 7
    PITCH = 8
    SYS = 9
    GYRO = 10
    ACC = 11
    MAG = 12
    PROXIMITY = 13

class Logger(object):

    def __init__(self):


        file_name = str(datetime.now())
        for char in ('.', ':', ' '):
            file_name = file_name.replace(char, '-')
        #os.mkdir(LOG_IMAGE_FILE_DIRECTORY + file_name)
        #self.image_file_name = LOG_IMAGE_FILE_DIRECTORY + file_name + "/"
        #self.image_counter = 1
        file_name += '.txt'
        self._is_upload = True
        self._current_data = dict()
        self.clear_and_build_current_data()
        self._data_list = []
        self._response = None
        self._server_file_name = None
        self._log_file_directory = Path(os.path.dirname(LOG_FILE_DIRECTORY))
        if not self._log_file_directory.exists():
            self._log_file_directory.mkdir(True, True)
        try:
            self.file = open(LOG_FILE_DIRECTORY + file_name, 'w')
        except IOError:
            print("An error occurred while opening the log file. Do you have appropriate permissions?")
        self.write_header()
        #pygame.camera.init()
        #self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        #self.cam.start()

    # write_header(self)
    # Writes header to file
    def write_header(self):
        self.file.write(FILE_HEADER)
        self.file.write('\n')

    def set_time(self):
        self._current_data[DataTypes.TIME] = str(datetime.now())

    def clear_and_build_current_data(self):
        self._current_data = dict()
        for i in DataTypes:
            self._current_data[i] = ''

    def is_dictionary_full(self):
        no_empty_values = True
        for dataType in DataTypes:
            if self._current_data[dataType] == '' and dataType.value != DataTypes.TIME.value:
                no_empty_values = False
        return no_empty_values

    def add_data(self, data, dataSource):
        startingIndex = 0
        endingIndex = 0
        if(dataSource == DataSources.WEIGHT):
            startingIndex = DataTypes.FR
            endingIndex = DataTypes.RL
        elif(dataSource == DataSources.GYROSCOPE):
            startingIndex = DataTypes.HEAD
            endingIndex = DataTypes.MAG
        elif(dataSource == DataSources.PROXIMITY):
            startingIndex = DataTypes.PROXIMITY
            endingIndex = DataTypes.PROXIMITY
        i = 0
        for dataType in DataTypes:
            if(dataType.value < startingIndex.value):
                continue
            self._current_data[dataType] = data[i]
            i = i + 1
            if dataType == endingIndex:
                break
        if self.is_dictionary_full():
            self.set_time()
            self._data_list.append(self.dict_to_string())
            self.clear_and_build_current_data()
        if len(self._data_list) == UPLOAD_FREQUENCY:
            self.write_data_to_file()
            self.upload_data()
            del self._data_list[:]

    # update_sensors(self, fr, fl, rr, rl)
    # adds the sensor values in order to member variable _current_data
    # in order to preserve integrity of log file, this function should be called before both
    # update_gyro and update_proximity
    # def update_sensors(self, fr, fl, rr, rl):
    #     self._current_data += ('{time}, {fr}, {fl}, {rr}, {rl}, '.format(
    #         time=datetime.now(),
    #         fr=fr,
    #         fl=fl,
    #         rr=rr,
    #         rl=rl,
    #     ))

    # update_gyro(self, head, roll, pitch, sys, gyro, acc, mag)
    # adds the gyroscope values in order to member variable _current_data
    # in order to preserve integrity of log file, this function should be called after update_sensors and
    # before update_proximity
    # def update_gyro(self, head, roll, pitch, sys, gyro, acc, mag):
    #     self._current_data += ('{head}, {roll}, {pitch}, {sys}, {gyro}, {acc}, {mag}, '.format(
    #         head=head,
    #         roll=roll,
    #         pitch=pitch,
    #         sys=sys,
    #         gyro=gyro,
    #         acc=acc,
    #         mag=mag,
    #     ))

    # update_proximity(self, proximity)
    # adds the proximity value to member variable _current_data
    # in order to preserve integrity of the log file, this function should be called after update_gyro and update_sensors
    # def update_proximity(self, proximity):
    #     self._current_data += str(proximity)

    # def capture_photos(self):
    #     img = self.cam.get_image()
    #     image_file_name = self.image_file_name + str(self.image_counter) + '.jpg'
    #     pygame.image.save(img, image_file_name)
    #     self.image_counter += 1

    # write_data_to_file(self)
    # writes the string _current_data to the local log file
    def write_data_to_file(self):
        for data in self._data_list:
            self.file.write(data)
            self.file.flush()

    # is_server_available(self)
    # tests the connection to the server
    # if the URL in SERVER_URL is valid, returns True. Otherwise returns False
    def is_server_available(self):
        if TEST_ENVIRONMENT:
            return False
        else:
            try:
                if(urlopen(SERVER_URL).getcode() == 204):
                    return True
                else:
                    return False
            except Exception:
                return False

    # is_server_response_set(self)
    # checks if either _response or _server_file_name is None
    # returns False if either variable is None, otherwise returns True
    def is_server_response_set(self):
        if self._response is None or self._server_file_name is None:
            return False
        else:
            return True

    # set_server_response(self)
    # sets the member variables _response and _server_file_name
    def set_server_response(self):
        self._response = requests.post(CREATE_FILE_URL)
        self._server_file_name = json.loads(self._response.content)['file_name']

    # sets _is_upload
    def set_upload_data(self, set_upload):
        self._is_upload = set_upload

    def dict_to_string(self):
        data = ""
        for key in sorted(self._current_data):
            if(key.value != len(self._current_data)):
                data += self._current_data[key]+", "
            else:
                data += self._current_data[key]+"\n"
        return data

    # upload_data(self, data)
    # if the server is available and self._is_upload == True, uploads data to server
    # if data is None then uploads self._current_data
    # returns True if data is uploaded, otherwise returns False
    def upload_data(self):
        if(self.is_server_available()):
            if(not self.is_server_response_set()):
                self.set_server_response()

            for data in self._data_list:
                requests.post(POST_URL, data={
                    'line': data,
                    'file_name': self._server_file_name,
                })
            return True
        else:
            return False


if __name__ == '__main__':
    myLogger = Logger()
    for i in range(0, 100):
        myLogger.add_data(['1','1','1','1','1','1', '1'], DataSources.GYROSCOPE)
        myLogger.add_data(['1','1','1','1','1','1'], DataSources.WEIGHT)
        myLogger.add_data(['1','1','1','1','1','1'], DataSources.PROXIMITY)

