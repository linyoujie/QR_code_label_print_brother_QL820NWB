#!/usr/bin/env python3
# chmod a+x hello.py

# pip install Pillow 
# brew install libusb
# pip install brother-ql==0.8.3
# pip install https://github.com/pklaus/brother_ql/archive/master.zip --upgrade
from PIL import Image, ImageDraw, ImageFont
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
import sys
from threading import Thread
import time
import re

# pip3 install pyqrcode
# pip3 install pypng

import pyqrcode
import png
from pyqrcode import QRCode


from threading import Thread
import time
global thread_running
thread_running = [True]
enter = ''

def my_forever_while():

    start_time = time.time()

    # run this while there is no input
    while thread_running[0]:
        time.sleep(0.1)

        if time.time() - start_time >= 5:
            start_time = time.time()
            # print('Another 5 seconds has passed')


def take_input():
    while thread_running[0]:
        user_input = input('(Type "!q" to quit) Type your input: ')
        # doing something with the input
        # printLabel("TestQRCode", "TestQRCodeTitle", "subtitle subtitle subtitle",  "11/29/2021",  'network', 'tcp://10.72.252.87:9100')
        if user_input == '!q' or user_input == '!Q':
            thread_running[0] = False
            print('Enter !q, program exit!')
        else:
            updated_date = time.strftime('%Y-%m-%d %H:%M:%S')
            user_input = re.sub(' +', ' ', user_input)

            input_arr = user_input.split('\t')
            print(input_arr)
            
            title, subtitle = '', ''
            for each in input_arr:
                if each:

                    if re.match(r'^\sIT([a-zA-Z]{2}[0-9]|[0-9])', each) or re.match(r'^IT([a-zA-Z]{2}[0-9]|[0-9])', each):
                        each = re.sub(' I', 'I', each)

                        title = each
                    else:
                        subtitle = each

            # labelPrinter.printLabel(title, title, subtitle, updated_date,  'network', 'tcp://10.72.252.87:9100')
            # labelPrinter.printLabel(title, title, subtitle,  updated_date,  'pyusb', 'usb://0x04f9:0x209d')
            print('Your title is: ', title, 'Your subtitle is: ',subtitle)

class labelPrinter:
    def printLabel(QRCodeText, title, subtitle,   date,  backend, printer):
        # Set up parameters
        w_cm, h_cm = (9.3, 2.9)             # Real label size in cm
        res_x, res_y = (270.7, 268.7)           # Desired resolution
        res_y_old = 214                      # Old y resolution (204 / 5.5 * 2.54)

        # Inch-to-cm factor
        f = 2.54

        # Determine image size w.r.t. resolution
        w = int(w_cm / f * res_x)
        h = int(h_cm / f * res_y)
        # w = 991
        # h = 306


        # Create new image with proper size
        img = Image.new('RGB', (w, h), color=(256, 256, 256))

        # Draw elements
        draw = ImageDraw.Draw(img)

        # font = ImageFont.load_default()

        def draw_text(content, x_cm, y_cm, font_size):           # 25/0.836 = 250
            font = ImageFont.truetype('arial.ttf', int(font_size / (res_y_old / res_y)))
            # font = ImageFont.load_default()

            x, y = (int(x_cm / f * res_x), int(y_cm / f * res_y))
            draw.text((x, y), content, (0, 0, 0), font=font)


        Subtitle = subtitle
        Subtitle2 = ''
        if len(Subtitle) > 28:
            if Subtitle[27] != ' ':
                Subtitle2 = Subtitle[27:]
                Subtitle =  Subtitle[:27]+'-'
            else:
                Subtitle2 = Subtitle[28:]
                Subtitle =  Subtitle[:28]
            

        # Draw texts
        if Subtitle:
            draw_text(title, 3, 0.2, 60)

            draw_text(Subtitle, 3, 1, 40)
            draw_text(Subtitle2, 3, 1.4, 40)
            draw_text(str(date), 3, 1.9, 40)
        else:
            draw_text(title, 3, 0.6, 60)

            draw_text(str(date), 3, 1.6, 40)

        # Polygon
        # coords_cm = [(0.15, 0.5), (1.35, 0.9), (1.35, 0.1)]
        # coords = [(int(c[0] / f * res_x), int(c[1] / f * res_y)) for c in coords_cm]
        # draw.polygon(tuple(coords), fill=(0, 0, 0))


        # Save image
        img.save('image.png', dpi=(res_x, res_y))
        im = Image.open('image.png')
        im.resize((306, 991)) 

        # QRcodeContent = pyqrcode.create('Marry X\'mas')
        # QRcodeContent.png('tempQRCode.png', scale=8, module_color=[0,0,0,128], quiet_zone=6) 
        # QRcodeImg=Image.open('tempQRCode.png')

        QRcodeContent = pyqrcode.create(QRCodeText)
        QRcodeContent.png('tempQRCode.png', scale=8, module_color=[0,0,0,128], quiet_zone=6) 
        QRcodeImg=Image.open('tempQRCode.png')


        im.paste(QRcodeImg, (0,0))

        im.save('image2.png', dpi=(res_x, res_y))

        # backend = 'pyusb'    # 'pyusb', 'linux_kernal', 'network'
        # printer = 'usb://0x04f9:0x209d'    # Get these values from the Windows usb driver filter.  Linux/Raspberry Pi uses '/dev/usb/lp0'.

        model = 'QL-820NWB' # your printer model.
        # backend = 'network'    # 'pyusb', 'linux_kernal', 'network'
        # printer = 'tcp://10.72.252.87:9100'    # Get these values from the Windows usb driver filter.  Linux/Raspberry Pi uses '/dev/usb/lp0'.

        qlr = BrotherQLRaster(model)
        qlr.exception_on_warning = True

        instructions = convert(
                qlr=qlr, 
                images=[im],    #  Takes a list of file names or PIL objects.
                label='29x90', 
                rotate='90',    # 'Auto', '0', '90', '270'
                threshold=70.0,    # Black and white threshold in percent.
                dither=False, 
                compress=False, 
                red=False,    # Only True if using Red/Black 62 mm label tape.
                dpi_600=False, 
                hq=True,    # False for low quality.
                cut=True
        )

        send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)

    # printLabel("TestQRCode", "TestQRCodeTitle", "subtitle subtitle subtitle",  "11/29/2021",  'network', 'tcp://10.72.252.87:9100')

if __name__ == '__main__':
    t1 = Thread(target=my_forever_while)
    t2 = Thread(target=take_input)

    t1.start()
    t2.start()
    while(thread_running[0]):
        t2.join() 

        # interpreter will wait until your process get completed or terminated

        # print('The end')