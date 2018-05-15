from datetime import datetime
import requests
import json
from settings import TEST_ENVIRONMENT


class Logger(object):


    def __init__(self):
        file_name = str(datetime.now())
        for char in ('.', ':', ' '):
            file_name = file_name.replace(char, '-')
        file_name += '.txt'
        self.upload_data = True
        self._current_data = ''


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


    def server_connection():
        if TEST_ENVIRONMENT:
            return False
        else:
            try:
                if(urlopen('http://10.173.215.128:8000/').getcode() == 200):
                    return True
                else
                    return False
            except Exception:
                return False

    def set_upload_data(self, upload):
        self.upload_data = upload

if __name__ == '__main__':
    Logger()


class ServerLogger(object):

    def __init__(self):
        response = requests.post('http://10.173.215.128:8000/create_file')
        self.file_name = json.loads(response.content)['file_name']
        self.line = ''

    def update_sensors(self, fr, fl, rr, rl):
        self.line = ('{time}, {fr}, {fl}, {rr}, {rl}, '.format(
            time=datetime.now(),
            fr=fr,
            fl=fl,
            rr=rr,
            rl=rl,
        ))

    def update_gyro(self, head, roll, pitch, sys, gyro, acc, mag):
        self.line += ('{head}, {roll}, {pitch}, {sys}, {gyro}, {acc}, {mag}, '.format(
            head=head,
            roll=roll,
            pitch=pitch,
            sys=sys,
            gyro=gyro,
            acc=acc,
            mag=mag, 
        ))

    def update_proximity(self, proximity):
        self.line += str(proximity)
        requests.post('http://10.173.215.128:8000/add_line', data={
            'line': self.line,
            'file_name': self.file_name,
        })
