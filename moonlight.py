import time
import datetime
import ephem

knoxville = ephem.Observer()
knoxville.name = 'Knoxville'
knoxville.lat = '35:57:53'
knoxville.long = '-83:55:35'
knoxville.elevation = 270
knoxville.date = datetime.date.today()

def printMoon():
  print( knoxville.date )
  print( time.time() )
  m = ephem.Moon()
  m.compute(knoxville)
  p = m.phase
  print(p)
  return

print( "print"  )

printMoon()

