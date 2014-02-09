#!/usr/bin/env python
from __future__ import division
import time
import RPi.GPIO as GPIO
import plotly
import datetime
from random import randint
import os
import sys

LOGGER = True # if not true, wont log!
FIRST_POST = True
spaces = (" "*50)

#init GPIO
GPIO.setmode(GPIO.BCM)

def question(question, poss_ans):
    response = False
    while response == False:
        answer = raw_input(question)
        if answer not in poss_ans:
            print b.ERR+'Not a Valid Answer, please try again...'+b.END
        else:
            response = True
            return answer

#Set Colors for the Prompt
class b:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARN = '\033[93m'
    ERR = '\033[91m'
    END = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.BLUE = ''
        self.GREEN = ''
        self.WARN = ''
        self.FAIL = ''
        self.END = ''

os.system('clear')
print(b.WARN+"========================================================")
print("Plot.ly + Raspberry Pi + TMP36 Temperature Visualization")
print("========================================================\n"+b.END)

#Questions
FILENAME = raw_input(b.BLUE+"Enter your Graph Name: \n>>  "+b.END)
USERNAME = raw_input(b.BLUE+"Enter your Plotly Username: \n>>  "+b.END)
API_KEY = raw_input(b.BLUE+"Enter your Plotly Api Key: \n>>  "+b.END)
TEMP_TYPE = question(b.BLUE+"Do you want to plot Celius for Farenheit? (c/f)  \n>>  "+b.END, ['c','f'])
BAR_SCATTER = question(b.BLUE+"Scatter or Bar Chart? (s/b)  \n>>  "+b.END, ['s','b'])
DELAY = int(raw_input(b.BLUE+"How frequently do you want to post data? (in seconds, minimum is 30)  \n>>  "+b.END))
if DELAY < 30:
    print b.ERR+'You chose a frequency less than 30 seconds.... defaulting to 30 seconds'+b.END
    DELAY = 30


#Set Temp Scale for legend
if TEMP_TYPE == 'c':
    TEMP_LEGEND = 'Temperature (C)'
elif TEMP_TYPE == 'f':
    TEMP_LEGEND = 'Temperature (F)'

if BAR_SCATTER == 's':
    chart_type = 'scatter'
elif BAR_SCATTER == 'b':
    chart_type = 'bar'

#Set Layout
LAYOUT = {
    'title' : FILENAME,
    'showlegend' : True,
    'yaxis' : {
        'title' : TEMP_LEGEND
    }
}

#init plotly
py = plotly.plotly(USERNAME, API_KEY)

while True:
        temp_C = randint(19,22)
        temp_F = randint(32,99)
        temp_C = "%.1f" % temp_C
        temp_F = "%.1f" % temp_F

        if LOGGER:

            if TEMP_TYPE == 'c':
                TEMP_READING = temp_C
            elif TEMP_TYPE == 'f':
                TEMP_READING = temp_F

            date_stamp = datetime.datetime.now()
            data = [{
            'x': date_stamp,
            'y': TEMP_READING,
            'name' : TEMP_LEGEND,
            'type' : chart_type
            }]

            response = py.plot(data, filename=FILENAME, fileopt='extend', layout=LAYOUT)
            if response[u'error'] != '' or response[u'message'] != '' or response[u'warning'] != '':
                quit()
            else:
                if FIRST_POST == True:
                    os.system('clear')
                    print(b.GREEN+"========================================================")
                    print("Successfully Posted to Plot.ly! Here is your Graph info:")
                    print("========================================================\n")
                    print(b.WARN+"Graph URL:       "+response[u'url'])
                    print("Graph Title:     "+response[u'filename']+'\n'+b.END)
                    print(b.GREEN+"========================================================\n"+b.END)
                    print(b.WARN+"Readings Posted to Plotly:\n"+b.END)
                    if TEMP_TYPE == 'c':
                        print(b.BLUE+"Temperature (C):    "+temp_C+b.END)
                    if TEMP_TYPE == 'f':
                        print(b.BLUE+"Temperature (F):    "+temp_F+b.END)

                    FIRST_POST = False
                else:
                    if TEMP_TYPE == 'c':
                        print(b.BLUE+"Temperature (C):    "+temp_C+b.END+spaces)
                    if TEMP_TYPE == 'f':
                        print(b.BLUE+"Temperature (F):    "+temp_F+b.END+spaces)

        # Delay between POSTs to Plot.ly
        toolbar_width = 54
        sleep_time = DELAY / toolbar_width
        # setup toolbar
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

        for i in xrange(toolbar_width):
            time.sleep(sleep_time)
            sys.stdout.write(b.WARN+"-"+b.END)
            sys.stdout.flush()
            if i == toolbar_width - 1:
                sys.stdout.write("\b" * (toolbar_width+1))

