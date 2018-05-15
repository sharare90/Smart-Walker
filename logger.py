from datetime import datetime
import requests
import json
from settings import TEST_ENVIRONMENT


class Logger(object):


    def __init__(self):
        SERVER_URL = 'http://10.173.215.128:8000/'
        POST_URL = SERVER_URL+'add_line'
        CREATE_FILE_URL = SERVER_URL+'create_file'

        file_name = str(datetime.now())
        for char in ('.', ':', ' '):
            file_name = file_name.replace(char, '-')
        file_name += '.txt'
        self._is_upload = True
        self._current_data = ''
        self._response = None
        self._server_file_name = None
        self.file = open('logs/' + file_name, 'w')
        self.write_header()

    def write_header(self):
        self.file.write('time, fr, fl, rr, rl, head, roll, pitch, sys, gyro, acc, mag, proximity')
        self.file.write('\n')

    def update_sensors(self, fr, fl, rr, rl):
        self._current_data += ('{time}, {fr}, {fl}, {rr}, {rl}, '.format(
            time=datetime.now(),
            fr=fr,
            fl=fl,
            rr=rr,
            rl=rl,
        ))

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

    def update_proximity(self, proximity):
        self._current_data += str(proximity)

    def write_data_to_file(self):
        self.file.write(_current_data)
        self.file.write('\n')
        self.file.flush()


    def is_server_available():
        if TEST_ENVIRONMENT:
            return False
        else:
            try:
                if(urlopen('http://10.173.215.128:8000/').getcode() == 200):
                    return True
                else:
                    return False
            except Exception:
                return False

    def is_server_response_set(self):
        if self._response is None or self._server_file_name is None:
            return False
        else:
            return True

    def set_server_response(self):
        self._response = requests.post(CREATE_FILE_URL)
        self._server_file_name = json.loads(self._response.content)['file_name']

    def set_upload_data(self, set_upload):
        self._is_upload = set_upload

    def upload_data(self):
        if(is_server_available() and self._is_upload):
            if(is_server_response_set(self)):
                set_server_response(self)

            requests.post(POST_URL, data={
                'line': self._current_data,
                'file_name': self._server_file_name,
            })


if __name__ == '__main__':
    Logger()


# class ServerLogger(object):

#     def __init__(self):
#         response = requests.post('http://10.173.215.128:8000/create_file')
#         self.file_name = json.loads(response.content)['file_name']
#         self.line = ''

#     def update_sensors(self, fr, fl, rr, rl):
#         self.line = ('{time}, {fr}, {fl}, {rr}, {rl}, '.format(
#             time=datetime.now(),
#             fr=fr,
#             fl=fl,
#             rr=rr,
#             rl=rl,
#         ))

#     def update_gyro(self, head, roll, pitch, sys, gyro, acc, mag):
#         self.line += ('{head}, {roll}, {pitch}, {sys}, {gyro}, {acc}, {mag}, '.format(
#             head=head,
#             roll=roll,
#             pitch=pitch,
#             sys=sys,
#             gyro=gyro,
#             acc=acc,
#             mag=mag, 
#         ))

#     def update_proximity(self, proximity):
#         self.line += str(proximity)
#         requests.post('http://10.173.215.128:8000/add_line', data={
#             'line': self.line,
#             'file_name': self.file_name,
#         })
