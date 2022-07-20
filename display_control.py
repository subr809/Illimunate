#!/usr/bin/env python3
import sys
import time
import textwrap
import threading
import queue
from enum import Enum

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7789

# SETTINGS
DC_SCROLL_SPD_MIN = 1
DC_SCROLL_SPD_MAX = 5
DC_VISIBLE_LINES = 5
DC_FONT_SIZE = 18
DC_CHAR_WIDTH = 14
DC_TEXT_TIMEOUT = 5
DC_OBJ_DISP_TIME = 2

class ObjType(Enum):
    STOP_SIGN = 1
    TRAFFIC_LIGHT = 2
    

class DisplayControl:
    def __init__(self):
        print("Display Control: init")
        # Create ST7789 LCD display class.
        self.__disp = ST7789.ST7789(
            height=240,
            rotation=180,
            port=0,
            cs=ST7789.BG_SPI_CS_BACK,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
            dc=25,
            spi_speed_hz=80 * 1000 * 1000,
            offset_left=0,
            offset_top=0,
        )
        # Initialize display.
        self.__disp.begin()
        self.__img = Image.new('RGB', (self.__disp.width, self.__disp.height), color=(0, 0, 0))
        self.__draw = ImageDraw.Draw(self.__img)
        self.__font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/courbd.ttf", DC_FONT_SIZE)
        self.__text_x = self.__disp.width // 8
        self.__text_y = self.__disp.height // 3
        self.__scroll_speed = 3

        self.__text_queue = queue.Queue()
        self.__write_time = time.time()
        self.__disp_buf = []

        self.__running = True
        self.__obj_detect_time = time.time()
        self.__obj_timer_running = False

        self.__draw_lock = threading.Lock()
        self.__worker_thread = threading.Thread(target=self.__worker_func)
        self.__worker_thread.start()

    def stop(self):
        self.__running = False

    def write(self, text):
        lines = textwrap.wrap(text, width=DC_CHAR_WIDTH)
        lps = len(lines) / (time.time() - self.__write_time)
        self.__scroll_speed = min(DC_SCROLL_SPD_MAX, max(DC_SCROLL_SPD_MIN, 2*lps)) # constrain scroll speed
        self.__write_time = time.time()
        for line in lines:
            self.__text_queue.put(line)

    def object_detected(self, object):
        if not self.__obj_timer_running:
            print("Display Control: obj_detect called, starting")
            self.__draw_lock.acquire()
            # Clear the img
            self.__draw.rectangle((0, 0, self.__disp.width, self.__disp.height), (0, 0, 0))
            # Draw object alert on img
            if object == ObjType.STOP_SIGN:
                self.__draw.regular_polygon((95, 140, 80), 8, fill=(255, 0, 0))
            elif object == ObjType.TRAFFIC_LIGHT:
                w, h = 220, 190
                shape = [(40, 40), (w - 10, h - 10)]
                self.__draw.rectangle(shape, fill =(0,255,255))
            elif object == ObjType.YIELD_SIGN:
                self.__draw.polygon([(20,10), (200, 200), (100,20)], fill = (255,0,0))
                self.__draw.polygon([(200,10), (200, 200), (150,50)], fill = 'yellow')
            # Draw image to the display
            self.__disp.display(self.__img.transpose(Image.FLIP_LEFT_RIGHT))

            self.__obj_timer_running = True
            threading.Timer(DC_OBJ_DISP_TIME, self.__timer_func).start()
        else:
            print("Display Control: obj_detect called, already running")

    def __timer_func(self):
        # Clear the img
        self.__draw.rectangle((0, 0, self.__disp.width, self.__disp.height), (0, 0, 0))
        self.__obj_timer_running = False
        self.__draw_lock.release()
        print("Display Control: finished object alert")
    
    def __worker_func(self):
        while self.__running or not self.__text_queue.empty():
            # Get the next line to display
            try:
                line = self.__text_queue.get(timeout=DC_TEXT_TIMEOUT) # blocks when queue is empty
            except queue.Empty: #timeout waiting for new text; clear the display
                self.__draw_lock.acquire()
                # Clear the img
                self.__draw.rectangle((0, 0, self.__disp.width, self.__disp.height), (0, 0, 0))
                # Draw image to the display
                self.__disp.display(self.__img.transpose(Image.FLIP_LEFT_RIGHT))
		# Clear the line buffer
                self.__disp_buf.clear()
                self.__draw_lock.release()
                line = self.__text_queue.get()
            self.__disp_buf.append(line)

            # Remove old lines
            if len(self.__disp_buf) > DC_VISIBLE_LINES:
                self.__disp_buf.pop(0)

            self.__draw_lock.acquire()
            # Clear the img
            self.__draw.rectangle((0, 0, self.__disp.width, self.__disp.height), (0, 0, 0))
            # Write text on image
            self.__draw.text((self.__text_x, self.__text_y), "\n".join(self.__disp_buf), font=self.__font, fill=(255, 255, 255))
            # Draw image to the display
            self.__disp.display(self.__img.transpose(Image.FLIP_LEFT_RIGHT))
            # sleep to slow scrolling speed
            time.sleep(1 / self.__scroll_speed)
            self.__draw_lock.release()


if __name__ == "__main__":
    dc = DisplayControl()
    #time.sleep(5)
    dc.write("The Thread class represents an activity that is run in a separate thread of control. There are two ways to specify the activity: by passing a callable object to the constructor, or by overriding the run() method in a subclass. No other methods (except for the constructor) should be overridden in a subclass. In other words, only override the __init__() and run() methods of this class.")
    time.sleep(20)
    for i in range(10):
        dc.object_detected(ObjType.STOP_SIGN)
        time.sleep(1)
    dc.write("Once a thread object is created, its activity must be started by calling the thread’s start() method. This invokes the run() method in a separate thread of control.")
    dc.stop()

