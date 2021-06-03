import sys
import time
import datetime
from datetime import datetime as dt
import ephem
import schedule
import RPi.GPIO as GPIO
from array import *

sys.stdout.write('Starting moonlight')

GPIO.setmode(GPIO.BCM)

LIGHT_COUNT = 0
# holds touch counter
LIGHT_MODE = 0
# actual light mode
# 0 IS ALL ON
# 1 IS BEZEL OFF, MOON ON
# 2 IS BEZEL ON, MOON OFF
# 3 IS ALL OFF
LIGHT_ARRAY = array( 'b', [0,0,0,0,0,0,0,0] )

CAP_PIN= 21
LED_BEZEL_PIN = 4
LED_PIN_1= 17
LED_PIN_2= 22
LED_PIN_3= 6
LED_PIN_4= 19
LED_PIN_5= 18
LED_PIN_6= 23
LED_PIN_7= 12
LED_PIN_8= 16

#LED PIN SETUP
GPIO.setup(LED_BEZEL_PIN, GPIO.OUT)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)
GPIO.setup(LED_PIN_3, GPIO.OUT)
GPIO.setup(LED_PIN_4, GPIO.OUT)
GPIO.setup(LED_PIN_5, GPIO.OUT)
GPIO.setup(LED_PIN_6, GPIO.OUT)
GPIO.setup(LED_PIN_7, GPIO.OUT)
GPIO.setup(LED_PIN_8, GPIO.OUT)


TOUCH_STATE = 0

def setLEDs( a,b,c,d,e,f,g,h ):
  print "setting LEDs"
  print a, b, c, d, e, f, g, h
  GPIO.output(LED_PIN_1, GPIO.HIGH if a else GPIO.LOW)
  GPIO.output(LED_PIN_2, GPIO.HIGH if b else GPIO.LOW)
  GPIO.output(LED_PIN_3, GPIO.HIGH if c else GPIO.LOW)
  GPIO.output(LED_PIN_4, GPIO.HIGH if d else GPIO.LOW)
  GPIO.output(LED_PIN_5, GPIO.HIGH if e else GPIO.LOW)
  GPIO.output(LED_PIN_6, GPIO.HIGH if f else GPIO.LOW)
  GPIO.output(LED_PIN_7, GPIO.HIGH if g else GPIO.LOW)
  GPIO.output(LED_PIN_8, GPIO.HIGH if h else GPIO.LOW)


def setLightMode(mode):
  global LIGHT_MODE
  LIGHT_MODE = mode
  print "setting light mode to:"
  print mode
  if LIGHT_MODE == 0:
    GPIO.output(LED_BEZEL_PIN, 1)
    setLEDs( LIGHT_ARRAY[0],LIGHT_ARRAY[1],LIGHT_ARRAY[2],LIGHT_ARRAY[3],LIGHT_ARRAY[4],LIGHT_ARRAY[5],LIGHT_ARRAY[6],LIGHT_ARRAY[7])
  if LIGHT_MODE == 1:
    GPIO.output(LED_BEZEL_PIN, 0)
    setLEDs( LIGHT_ARRAY[0],LIGHT_ARRAY[1],LIGHT_ARRAY[2],LIGHT_ARRAY[3],LIGHT_ARRAY[4],LIGHT_ARRAY[5],LIGHT_ARRAY[6],LIGHT_ARRAY[7])
  elif LIGHT_MODE == 2:
    GPIO.output(LED_BEZEL_PIN, 1)
    setLEDs( 0,0,0,0,0,0,0,0 )
  elif LIGHT_MODE == 3:
    GPIO.output(LED_BEZEL_PIN, 0)
    setLEDs( 0,0,0,0,0,0,0,0 )

def touch_callback(channel):
  global TOUCH_STATE
  global LIGHT_COUNT
  #print "BOTH DETECTED"
  #print channel
  #print GPIO.input(channel)
  read = GPIO.input(channel)
  if read:
    if read != TOUCH_STATE:
      print "+++++++++++ touch started"
    #print "rising!"
  else:
    if read != TOUCH_STATE:
      print "----------- touch ended"
      LIGHT_COUNT += 1
      if LIGHT_COUNT > 3:
        LIGHT_COUNT = 0
      setLightMode(LIGHT_COUNT)
    #print "falling!"
  TOUCH_STATE = read

def touch_callback_rising(channel):
  print "RISING edge detected on:"
  print channel

def touch_callback_falling(channel):
  print "FALLING EDGE on"
  print channel

#CAP SENSOR PIN
GPIO.setup(CAP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(CAP_PIN, GPIO.BOTH, callback=touch_callback)
#GPIO.add_event_detect(CAP_PIN, GPIO.RISING, callback=touch_callback_rising, bouncetime=500)

#LED PIN SETUP
GPIO.setup(LED_BEZEL_PIN, GPIO.OUT)
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


def setLEDs( a,b,c,d,e,f,g,h ):
  print "setting LEDs"
  print a, b, c, d, e, f, g, h
  GPIO.output(LED_PIN_1, GPIO.HIGH if a else GPIO.LOW)
  GPIO.output(LED_PIN_2, GPIO.HIGH if b else GPIO.LOW)
  GPIO.output(LED_PIN_3, GPIO.HIGH if c else GPIO.LOW)
  GPIO.output(LED_PIN_4, GPIO.HIGH if d else GPIO.LOW)
  GPIO.output(LED_PIN_5, GPIO.HIGH if e else GPIO.LOW)
  GPIO.output(LED_PIN_6, GPIO.HIGH if f else GPIO.LOW)
  GPIO.output(LED_PIN_7, GPIO.HIGH if g else GPIO.LOW)
  GPIO.output(LED_PIN_8, GPIO.HIGH if h else GPIO.LOW)



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
  global LIGHT_ARRAY
  today_minus_yesterday = p-p_y
  tomorrow_minus_today = p_t-p
  
  print today_minus_yesterday
  print tomorrow_minus_today
  
  print "--$$$$$$$$$$--"
  if p < 6.25:
    print "phase less than 6.25"
    print "NEW MOON - ALL OFF"
    print "0 0 0 0 0 0 0 0"
    LIGHT_ARRAY = array('b', [0,0,0,0,0,0,0,0])
    if LIGHT_MODE == 0 or LIGHT_MODE == 1:
      setLEDs(0,0,0,0,0,0,0,0)
  elif p < 18.75:
    print "phase less than 18.75"
    if today_minus_yesterday < 0:
      print "waning crescent"
      print "1 0 0 0 0 0 0 0"
      LIGHT_ARRAY = array( 'b', [1,0,0,0,0,0,0,0])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(1,0,0,0,0,0,0,0)
    else:
      print "waxing crescent"
      print "0 0 0 0 0 0 0 1"
      LIGHT_ARRAY = array( 'b', [0,0,0,0,0,0,0,1])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(0,0,0,0,0,0,0,1)
  elif p < 31.25:
    print "phase less than 31.25"
    if today_minus_yesterday < 0:
      print "last quarter"
      print "1 1 0 0 0 0 0 0"
      LIGHT_ARRAY = array( 'b', [1,1,0,0,0,0,0,0])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(1,1,0,0,0,0,0,0)
    else:
      print "first quarter"
      print "0 0 0 0 0 0 1 1"
      LIGHT_ARRAY = array( 'b', [0,0,0,0,0,0,1,1])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(0,0,0,0,0,0,1,1)
  elif p < 43.75:
    print "phase less than 43.75"
    if today_minus_yesterday < 0:
      print "waning GIBBOUS"
      print "1 1 1 0 0 0 0 0"
      LIGHT_ARRAY = array( 'b', [1,1,1,0,0,0,0,0])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(1,1,1,0,0,0,0,0)
    else:
      print "waxing GIBBOUS"
      print "0 0 0 0 0 1 1 1"
      LIGHT_ARRAY = array( 'b', [0,0,0,0,0,1,1,1])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1: 
        setLEDs(0,0,0,0,0,1,1,1)
  elif p < 56.25:
    print "phase less than 56.25"
    if today_minus_yesterday < 0:
      print "waning half"
      print "1 1 1 1 0 0 0 0"
      LIGHT_ARRAY = array( 'b', [1,1,1,1,0,0,0,0])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(1,1,1,1,0,0,0,0)
    else:
      print "waxing half"
      print "0 0 0 0 1 1 1 1"
      LIGHT_ARRAY = array( 'b', [0,0,0,0,1,1,1,1])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(0,0,0,0,1,1,1,1)
  elif p < 68.75:
    print "phase less than 68.75"
    if today_minus_yesterday < 0:
      print "waning GIBBOUS"
      print "1 1 1 1 1 0 0 0"
      LIGHT_ARRAY = array( 'b', [1,1,1,1,1,0,0,0])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(1,1,1,1,1,0,0,0)
    else:
      print "waxing GIBBOUS"
      print "0 0 0 1 1 1 1 1"
      LIGHT_ARRAY = array( 'b', [0,0,0,1,1,1,1,1])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(0,0,0,1,1,1,1,1)
  elif p < 81.25:
    print "phase less than 81.25"
    if today_minus_yesterday < 0:
      print "waning LAST QUARTER"
      print "1 1 1 1 1 1 0 0"
      LIGHT_ARRAY = array( 'b', [1,1,1,1,1,1,0,0])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(1,1,1,1,1,1,0,0)
    else:
      print "waxing LAST QUARTER"
      print "0 0 1 1 1 1 1 1"
      LIGHT_ARRAY = array( 'b', [0,0,1,1,1,1,1,1])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(0,0,1,1,1,1,1,1)
  elif p < 93.75:
    print "phase less than 93.75"
    if today_minus_yesterday < 0:
      print "waning almost full"
      print "1 1 1 1 1 1 1 0"
      LIGHT_ARRAY = array( 'b', [1,1,1,1,1,1,1,0])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(1,1,1,1,1,1,1,0)
    else:
      print "waxing almost full"
      print "0 1 1 1 1 1 1 1"
      LIGHT_ARRAY = array( 'b', [0,1,1,1,1,1,1,1])
      if LIGHT_MODE == 0 or LIGHT_MODE == 1:
        setLEDs(0,1,1,1,1,1,1,1)
  else:
    print "FULLLLLLLLLLLLLLL"
    print "1 1 1 1 1 1 1 1"
    LIGHT_ARRAY = array( 'b', [1,1,1,1,1,1,1,1])
    if LIGHT_MODE == 0 or LIGHT_MODE == 1:
      setLEDs(1,1,1,1,1,1,1,1)


sequenceTime = 0.1

def initSequence():
  GPIO.output(LED_BEZEL_PIN, GPIO.HIGH)
  for count in range(4):
    setLEDs(0,0,0,0,0,0,0,0)
    time.sleep(sequenceTime)
    setLEDs(1,0,0,0,0,0,0,0)
    time.sleep(sequenceTime)
    setLEDs(1,1,0,0,0,0,0,0)
    time.sleep(sequenceTime)
    setLEDs(1,1,1,0,0,0,0,0)
    time.sleep(sequenceTime)
    setLEDs(1,1,1,1,0,0,0,0)
    time.sleep(sequenceTime)
    setLEDs(1,1,1,1,1,0,0,0)
    time.sleep(sequenceTime)
    setLEDs(1,1,1,1,1,1,0,0)
    time.sleep(sequenceTime)
    setLEDs(1,1,1,1,1,1,1,0)
    time.sleep(sequenceTime)
    setLEDs(1,1,1,1,1,1,1,1)
    time.sleep(sequenceTime)
    setLEDs(0,1,1,1,1,1,1,1)
    time.sleep(sequenceTime)
    setLEDs(0,0,1,1,1,1,1,1)
    time.sleep(sequenceTime)
    setLEDs(0,0,0,1,1,1,1,1)
    time.sleep(sequenceTime)
    setLEDs(0,0,0,0,1,1,1,1)
    time.sleep(sequenceTime)
    setLEDs(0,0,0,0,0,1,1,1)
    time.sleep(sequenceTime)
    setLEDs(0,0,0,0,0,0,1,1)
    time.sleep(sequenceTime)
    setLEDs(0,0,0,0,0,0,0,1)
    time.sleep(sequenceTime)
    setLEDs(0,0,0,0,0,0,0,0)
    time.sleep(sequenceTime)
  time.sleep(5)
  #GPIO.output(LED_BEZEL_PIN, GPIO.LOW)


print( "print"  )

init()

initSequence()

try:
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

except KeyboardInterrupt:
  print "keyboard interrupt"

except:
  print "other exception"

finally:
  print "cleaning up"
  GPIO.cleanup()
