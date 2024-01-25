import DELU

if (__name__ == "__main__"):
    DELU.system.auto_refresher()

    system = DELU.system(['영재'])
    controller = DELU.controller()
    controller.command()
