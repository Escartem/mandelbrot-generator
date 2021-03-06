from os import system
from eta import ETA
from PIL import Image
from time import sleep
from datetime import datetime
# from numba import jit
from argparse import ArgumentParser
# from win10toast import ToastNotifier

# toaster = ToastNotifier()
parser = ArgumentParser()
# parser.add_argument("--iterations", type=int, help="Number of iterations")
# parser.add_argument("--size", type=int, help="Resolution of image")
parser.add_argument("--color", type=int, help="The color modifier")
parser.add_argument("--repeat", type=int, help="The number of repetitions")
parser.add_argument("--preset", type=str, help="Choose a preset")
args = parser.parse_args()

version = "1.1.1"

presets = {
    "very_low": (50, 0.5),
    "low": (100, 1),
    "medium": (150, 1.5),
    "high": (200, 2),
    "very_high": (300, 2.5),
    "extreme": (400, 4)
}

system('title Mandelbrot Generator - V.' + str(version))
system('mode con: cols=53 lines=34')


def title():
    system('color 3F')
    system('cls')
    print('=====================================================\n')
    print(' __  __                 _      _ _               _')
    print('|  \/  |               | |    | | |             | |')
    print('| \  / | __ _ _ __   __| | ___| | |__  _ __ ___ | |_')
    print('| |\/| |/ _` | \'_ \ / _` |/ _ \ | \'_ \| \'__/ _ \| __|')
    print('| |  | | (_| | | | | (_| |  __/ | |_) | | | (_) | |_')
    print('|_|  |_|\__,_|_| |_|\__,_|\___|_|_.__/|_|  \___/ \__|')
    print('')
    print(' _____                            _')
    print('/ ____|                          | |')
    print('| |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ _')
    print('| | |_ |/ _ \ \'_ \ / _ \ \'__/ _` | __/ _ \| \'_|')
    print('| |__| |  __/ | | |  __/ | | (_| | || (_) | |')
    print(' \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|')
    print('V.' + version + '\t\t\t\tby @Escartem')
    print('')
    print('=====================================================\n')


class Mandelbrot:
    def __init__(self, i=100, res=1, p=1, c=12):
        self.i = i
        self.p = p
        self.c = c

        self.sx = round(320 * res)
        self.sy = round(222 * res)

        self.eta = ETA(self.sx * self.sy)

        self.img = Image.new('RGB', (self.sx, self.sy), "white")
        self.pixels = self.img.load()

    def gen(self):
        for x in range(self.sx):
            for y in range(self.sy):
                z = complex(0, 0)
                c = complex(3.5 * x / (self.sx - 1) - 2.5, -2.5 * y / (self.sy - 1) + 1.25)
                i = 0
                while (i < self.i) and abs(z) < 2:
                    i = i + 1
                    z = c + z * z ** self.p
                    rgb = int(255 * i / self.i)
                    col = (int(rgb * 0.82 * self.c), int(rgb * 0.13 * self.c), int(rgb * 0.18 * self.c))

                    self.pixels[x, y] = col
                self.eta.print_status(x * self.sy)
            # print(round((x/self.sx)*100, 1), end='\r')

        self.eta.done()
        self.export()

    def export(self):
        name = round(datetime.timestamp(datetime.now()) * 1000000)
        self.img.save(str(name) + '.png')
        print('Saved as ' + str(name) + '.png')
        print('')
        # toaster.show_toast("Generation done !", "Your fractal is now fully generated !", threaded=True)
        print('==================================================\n')
        system('pause')


preset = None


def setup1():
    title()
    global iterations
    global resolution
    global color
    global repeat
    print('Setup :')
    print('Number of iterations : (max: 400, recommended: 100)')
    try:
        entry = int(input("> "))
    except:
        entry = 100
    if entry > 400:
        iterations = 400
    elif entry < 1:
        iterations = 1
    else:
        iterations = entry
    print('Resolution of fractal : (max: 5, recommended: 1)')
    try:
        entry = int(input("> "))
    except:
        entry = 1
    if entry > 5:
        resolution = 5
    elif entry < 1:
        resolution = 1
    else:
        resolution = entry
    print('Saturation : (max: 255, recommended: 12)')
    try:
        entry = int(input("> "))
    except:
        entry = 12
    if entry > 255:
        color = 255
    elif entry < 1:
        color = 1
    else:
        color = entry
    print('Fractal repeat : (max: 20, recommended: 1)')
    try:
        entry = int(input("> "))
    except:
        entry = 1
    if entry > 20:
        repeat = 20
    elif entry < 1:
        repeat = 1
    else:
        repeat = entry
    print('')
    print('Configuration done !')
    print('Starting soon...')
    sleep(2.5)
    setup2()


def setup2():
    title()
    print("Generating a fractal with the following settings :")
    if preset is not None:
        print("\t- Preset : " + str(preset))
    print("\t- Iterations : " + str(iterations))
    print("\t- Resolution : " + str(round(320 * resolution)) + 'x' + str(round(222 * resolution)) + 'px')
    print("\t- Color modifier : " + str(color))
    print("\t- Repeat : " + str(repeat))
    print('')
    print('=====================================================\n')
    sleep(2)

    fractal = Mandelbrot(iterations, resolution, repeat, color)
    fractal.gen()


if args.preset is None or args.preset not in presets:
    setup1()
    preset = None
else:
    preset = args.preset
    iterations = presets[args.preset][0]
    resolution = presets[args.preset][1]
    if args.color is not None:
        if args.color > 255:
            color = 255
        elif args.color < 1:
            color = 1
        else:
            color = args.color
    else:
        color = 12
    if args.repeat is not None:
        if args.repeat > 20:
            repeat = 20
        elif args.repeat < 1:
            repeat = 1
        else:
            repeat = args.repeat
    else:
        repeat = 1
    setup2()
