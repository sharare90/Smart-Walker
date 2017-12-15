from datetime import datetime


timing_file = open('logs/timing/timing.txt', 'w')


def timing(func):
    def func_wrapper(*args, **kwargs):
        begin = datetime.now()
        result = func(*args, **kwargs)
        timing_file.write('{name}: {duration}\n'.format(name=func.__name__, duration=datetime.now() - begin))
        timing_file.flush()
        return result

    return func_wrapper
