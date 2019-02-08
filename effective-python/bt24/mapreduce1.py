import os
from threading import Thread

class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputdata(GenericInputData):
    def __init__(self, path):
        super().__init__()
        self.path = path 

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCounterWorker(GenericWorker):
    def __init__(self, input_data):
        super().__init__(input_data)

    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result

def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    
    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result

def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


if __name__ == "__main__":
    import subprocess
    proc = subprocess.Popen("pwd", stdout=subprocess.PIPE, shell=True)
    out, _ = proc.communicate()
    path = out.decode('utf-8').strip('\n')

    config = {'data_dir': path}
    result = mapreduce(LineCounterWorker, PathInputdata, config)
    print(result)
