from .sor import *
import os

def bulk(directory: str, filter : callable = lambda x: True):
    for file in os.listdir(directory):
        if filter(file):
            yield SOR(
                os.path.join(directory, file),
            )
