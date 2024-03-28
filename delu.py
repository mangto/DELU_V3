import DELU

if (__name__ == "__main__"):
    DELU.system.auto_refresher()


    system = DELU.system(['영재', '2-1'])
    DELU.bot('2024(2-2반)', lps=5, notification='.\\DELU\\data\\notification\\2-2.json')
    controller = DELU.controller()
    controller.command()