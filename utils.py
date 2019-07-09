import numpy as np
import math

class Counter:
    def __init__(self):
        self.dict = {}

    def add(self, key, count):
        if key in self.dict:
            self.dict[key] = self.dict[key] + count
        else:
            self.dict[key] = count

    def get(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return 0

    def numPresentKeys(self):
        return len(self.dict.keys())

    def freqArray(self):
        return np.array([math.log(float(i)) for i in self.dict.values()])

    def items(self):
        return self.dict.items()

    def keys(self):
        return self.dict.keys()