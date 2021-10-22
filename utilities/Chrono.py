from time import perf_counter 

class Chrono:
    def start(self):
        self.start = perf_counter()
    
    def end(self):
        self.end = perf_counter()

    def elapsed(self):
        return self.end - self.start