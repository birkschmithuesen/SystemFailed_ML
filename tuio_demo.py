#!/bin/env python3

from pythontuio import TuioClient
from pythontuio import Cursor
from pythontuio import TuioListener
from threading import Thread
import time

def print_cursor(cursor):
    print(str(round(time.time() * 1000)) + '|' + str(cursor.session_id) + '|' + str(cursor.position[0]) + '|' + str(cursor.position[1]))

class MyListener(TuioListener):
    def add_tuio_cursor(self, cursor: Cursor):
        print("detect a new Cursor")
        print_cursor(cursor)
    def update_tuio_cursor(self, cursor: Cursor):
        print_cursor(cursor)
    def remove_tuio_cursor(self, cursor: Cursor):
        print("a cursor was removed")
        print_cursor(cursor)


client = TuioClient(("localhost",3333))
t = Thread(target=client.start)
listener = MyListener()
client.add_listener(listener)

t.start()
