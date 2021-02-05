from os import system
from eta import ETA
from PIL import Image
from time import sleep
from datetime import datetime
# from argparse import ArgumentParser

# parser = ArgumentParser()
# parser.add_argument("--iterations", type=int, help="Number of iterations")
# parser.add_argument("--size", type=int, help="Resolution of image")
# parser.add_argument("--color", type=int, help="The color modifier")
# parser.add_argument("--repeat", type=int, help="The number of repetitions")
# parser.add_argument("--preset", type=str, help="Choose a preset")
# args = parser.parse_args()

presets = {
    "very_low": (50, 0.5),
    "low": (100, 1),
    "medium": (150, 1.5),
    "high": (200, 2),
    "very_high": (300, 2.5),
    "extreme": (400, 4)
}

system('title Mandelbrot Generator')

def title():
    system('color 3F')
    system('cls')
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
    print('\t\t\t\tby @Escartem')
    print('')
    print('==================================================\n')


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
        name = round(datetime.timestamp(datetime.now())*1000000)
        self.img.save(str(name) + '.png')
        print('Saved as ' + str(name) + '.png')
        print('')
        print('==================================================\n')
        for i in range(5):
            print('Closing in ' + str(5-i), end='\r')
            sleep(1)


title()
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
print('Color modifier : (max: 255, recommended: 12)')
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

title()
print("Generating a Mandelbrot fractal with the following settings :")
# print("\t- Preset : " + str(preset))
print("\t- Iterations : " + str(iterations))
print("\t- Resolution : " + str(320 * resolution) + 'x' + str(222 * resolution) + 'px')
print("\t- Color modifier : " + str(color))
print("\t- Repeat : " + str(repeat))
print('')
print('==================================================\n')
sleep(2)

fractal = Mandelbrot(iterations, resolution, repeat, color)
fractal.gen()
