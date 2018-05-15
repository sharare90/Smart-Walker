from datetime import datetime
import requests
import json
from settings import TEST_ENVIRONMENT

SERVER_URL = 'http://10.173.215.128:8000/'
POST_URL = SERVER_URL+'add_line'
CREATE_FILE_URL = SERVER_URL+'create_file'
LOG_FILE_DIRECTORY = 'logs/'
FILE_HEADER = 'time, fr, fl, rr, rl, head, roll, pitch, sys, gyro, acc, mag, proximity'

class Logger(object):

    def __init__(self):


        file_name = str(datetime.now())
        for char in ('.', ':', ' '):
            file_name = file_name.replace(char, '-')
        file_name += '.txt'
        self._is_upload = True
        self._current_data = ''
        self._response = None
        self._server_file_name = None
        self.file = open(LOG_FILE_DIRECTORY + file_name, 'w')
        self.write_header()

    # write_header(self)
    # Writes header to file
    def write_header(self):
        self.file.write(FILE_HEADER)
        self.file.write('\n')

    # update_sensors(self, fr, fl, rr, rl)
    # adds the sensor values in order to member variable _current_data
    # in order to preserve integrity of log file, this function should be called before both
    # update_gyro and update_proximity
    def update_sensors(self, fr, fl, rr, rl):
        self._current_data += ('{time}, {fr}, {fl}, {rr}, {rl}, '.format(
            time=datetime.now(),
            fr=fr,
            fl=fl,
            rr=rr,
            rl=rl,
        ))

    # update_gyro(self, head, roll, pitch, sys, gyro, acc, mag)
    # adds the gyroscope values in order to member variable _current_data
    # in order to preserve integrity of log file, this function should be called after update_sensors and
    # before update_proximity
    def update_gyro(self, head, roll, pitch, sys, gyro, acc, mag):
        self._current_data += ('{head}, {roll}, {pitch}, {sys}, {gyro}, {acc}, {mag}, '.format(
            head=head,
            roll=roll,
            pitch=pitch,
            sys=sys,
            gyro=gyro,
            acc=acc,
            mag=mag,
        ))

    # update_proximity(self, proximity)
    # adds the proximity value to member variable _current_data
    # in order to preserve integrity of the log file, this function should be called after update_gyro and update_sensors
    def update_proximity(self, proximity):
        self._current_data += str(proximity)

    # write_data_to_file(self)
    # writes the string _current_data to the local log file
    def write_data_to_file(self):
        self.file.write(_current_data)
        self.file.write('\n')
        self.file.flush()

    # is_server_available()
    # tests the connection to the server
    # if the URL in SERVER_URL is valid, returns True. Otherwise returns False
    def is_server_available():
        if TEST_ENVIRONMENT:
            return False
        else:
            try:
                if(urlopen(SERVER_URL).getcode() == 200):
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

    # upload_data(self, data)
    # if the server is available and self._is_upload == True, uploads data to server
    def upload_data(self, data):
        if(is_server_available() and self._is_upload):
            if(is_server_response_set(self)):
                set_server_response(self)

            requests.post(POST_URL, data={
                'line': data,
                'file_name': self._server_file_name,
            })


if __name__ == '__main__':
    Logger()
