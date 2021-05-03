import time
import datetime
from datetime import datetime as dt
import ephem
import schedule
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


def CAP_PIN 5
def LED_PIN_1 17
def LED_PIN_2 22
def LED_PIN_3 6
def LED_PIN_4 19
def LED_PIN_5 16
def LED_PIN_6 12
def LED_PIN_7 23
def LED_PIN_8 18


#CAP SENSOR PIN
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(5, GPIO.RISING, callback=touch_callback_rising, bouncetime=500)


#LED PIN SETUP
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)
GPIO.setup(LED_PIN_3, GPIO.OUT)
GPIO.setup(LED_PIN_4, GPIO.OUT)
GPIO.setup(LED_PIN_5, GPIO.OUT)
GPIO.setup(LED_PIN_6, GPIO.OUT)
GPIO.setup(LED_PIN_7, GPIO.OUT)
GPIO.setup(LED_PIN_8, GPIO.OUT)

#TIME STUFF
TIME = time.time()

yesterday = datetime.date.fromtimestamp(TIME-86400)
tomorrow = datetime.date.fromtimestamp(TIME+86400)


knoxville = ephem.Observer()
knoxville.name = 'Knoxville'
knoxville.lat = '35:57:53'
knoxville.long = '-83:55:35'
knoxville.elevation = 270
knoxville.date = dt.now()
#knoxville.date = datetime.date.today()

knoxville_yesterday = ephem.Observer()
knoxville_yesterday.name = knoxville.name
knoxville_yesterday.lat = knoxville.lat
knoxville_yesterday.long = knoxville.long
knoxville_yesterday.elevation = knoxville.elevation
knoxville_yesterday.date = yesterday

knoxville_tomorrow = ephem.Observer()
knoxville_tomorrow.name = knoxville.name
knoxville_tomorrow.lat = knoxville.lat
knoxville_tomorrow.long = knoxville.long
knoxville_tomorrow.elevation = knoxville.elevation
knoxville_tomorrow.date = tomorrow


print yesterday
print tomorrow

print time.time()

moon = ephem.Moon()
moon.compute(knoxville)

phase = moon.phase

#YESTERDAY
moon_yesterday = ephem.Moon()
moon_yesterday.compute(knoxville_yesterday)
phase_yesterday = moon_yesterday.phase

#TOMORROW
moon_tomorrow = ephem.Moon()
moon_tomorrow.compute(knoxville_tomorrow)
phase_tomorrow = moon_tomorrow.phase


def touch_callback_rising(channel):
  print "RISING edge detected on 4"


def init():
  print "init"


def printMoon():
  print( knoxville.date )
  print( time.time() )
  m = ephem.Moon()
  m.compute(knoxville)
  p = m.phase
  print(p)
  return


def checkDaily():
  print "daily check"
  knoxville.date = datetime.date.fromtimestamp(TIME)
  #knoxville.date = dt.now()
  moon.compute(knoxville)
  phase = moon.phase
  
  knoxville_yesterday.date = datetime.date.fromtimestamp(TIME-86400)
  moon_yesterday = ephem.Moon()
  moon_yesterday.compute(knoxville_yesterday)
  phase_yesterday = moon_yesterday.phase
  
  knoxville_tomorrow.date = datetime.date.fromtimestamp(TIME+86400)
  moon_tomorrow.compute(knoxville_tomorrow)
  phase_tomorrow = moon_tomorrow.phase
  
  print "today's phase"
  print phase
  print "yesterday's phase"
  print phase_yesterday
  print "tomorrow's phase"
  print phase_tomorrow
  print "--"
  
  calculatePhase( phase, phase_yesterday, phase_tomorrow )

def calculatePhase(p, p_y, p_t):
  #print "today's phase"
  #print p
  #print "yesterday's phase"
  #print p_y
  #print "tomorrow's phase"
  #print p_t
  #print "--"

  today_minus_yesterday = p-p_y
  tomorrow_minus_today = p_t-p
  
  print today_minus_yesterday
  print tomorrow_minus_today
  
  print "--$$$$$$$$$$--"
  if p < 6.25:
    print "phase less than 6.25"
    print "NEW MOON - ALL OFF"
    print "0 0 0 0 0 0 0 0"
  elif p < 18.75:
    print "phase less than 18.75"
    if today_minus_yesterday < 0:
      print "waning crescent"
      print "1 0 0 0 0 0 0 0"
    else:
      print "waxing crescent"
      print "0 0 0 0 0 0 0 1"
  elif p < 31.25:
    print "phase less than 31.25"
    if today_minus_yesterday < 0:
      print "last quarter"
      print "1 1 0 0 0 0 0 0"
    else:
      print "first quarter"
      print "0 0 0 0 0 0 1 1"
  elif p < 43.75:
    print "phase less than 43.75"
    if today_minus_yesterday < 0:
      print "waning GIBBOUS"
      print "1 1 1 0 0 0 0 0"
    else:
      print "waxing GIBBOUS"
      print "0 0 0 0 0 1 1 1"
  elif p < 56.25:
    print "phase less than 56.25"
    if today_minus_yesterday < 0:
      print "waning half"
      print "1 1 1 1 0 0 0 0"
    else:
      print "waxing half"
      print "0 0 0 0 1 1 1 1"
  elif p < 68.75:
    print "phase less than 68.75"
    if today_minus_yesterday < 0:
      print "waning GIBBOUS"
      print "1 1 1 1 1 0 0 0"
    else:
      print "waxing GIBBOUS"
      print "0 0 0 1 1 1 1 1"
  elif p < 81.25:
    print "phase less than 81.25"
    if today_minus_yesterday < 0:
      print "waning LAST QUARTER"
      print "1 1 1 1 1 1 0 0"
    else:
      print "waxing LAST QUARTER"
      print "0 0 1 1 1 1 1 1"
  elif p < 93.75:
    print "phase less than 93.75"
    if today_minus_yesterday < 0:
      print "waning almost full"
      print "1 1 1 1 1 1 1 0"
    else:
      print "waxing almost full"
      print "0 1 1 1 1 1 1 1"
  else:
    print "FULLLLLLLLLLLLLLL"
    print "1 1 1 1 1 1 1 1"


print( "print"  )

init()

while True:
  print "-----------------------------------------------"
  print "     calculating for "
  print datetime.date.fromtimestamp(TIME)
  print "  |||||||||  "
  #printMoon()
  
  checkDaily()
  #checkPhase()
  
  TIME += 86400
  
  time.sleep(5)
