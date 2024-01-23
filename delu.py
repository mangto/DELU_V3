import DELU
from multiprocessing import Process

if (__name__ == "__main__"):
    DELU.system.auto_refresher()

    system = DELU.system(['델루'])
    controller = DELU.controller()
    controller.command()