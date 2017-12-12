from datetime import datetime


class Logger(object):
    def __init__(self):
        file_name = str(datetime.now())
        self.file = open('logs/' + file_name, 'w')
        self.write_header()

    def write_header(self):
        self.file.write('time, fr, fl, rr, rl, head, roll, pitch, sys, gyro, acc, mag, proximity')
        self.file.write('\n')

    def update_sensors(self, fr, fl, rr, rl):
        self.file.write('{time}, {fr}, {fl}, {rr}, {rl}, '.format(
            time=datetime.now(),
            fr=fr,
            fl=fl,
            rr=rr,
            rl=rl,
        ))

    def update_gyro(self, head, roll, pitch, sys, gyro, acc, mag):
        self.file.write('{head}, {roll}, {pitch}, {sys}, {gyro}, {acc}, {mag}, '.format(
            head=head,
            roll=roll,
            pitch=pitch,
            sys=sys,
            gyro=gyro,
            acc=acc,
            mag=mag,
        ))

    def update_proximity(self, proximity):
        self.file.write(str(proximity))
        self.file.write('\n')

if __name__ == '__main__':
    Logger()