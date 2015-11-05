import csv
# Configure margins here in ms
Mtime = (0.005, 0.010, 0.020, 0.050, 0.200)

# Configure trigger time in ms
tTrigger = 1

# Configure File here
watchdogData = 'watchdog_testing.csv'

# Graph drawing
graphChar = "X"

# Initialize vars
Mneg = []
Mpos = []
MposGraph = []
MnegGraph = []
for x in range(len(Mtime)+1):
   Mneg.append(0)
   Mpos.append(0)
   MposGraph.append("")
   MnegGraph.append("")
maxValue = 0
minValue = 0
count = 0
avgTime = 0

# Open CSV file and calculate the statistics
with open(watchdogData, 'rb') as csvfile:
   wdData = csv.reader(csvfile, delimiter=',', quotechar='|', skipinitialspace='true')
   wdData.next()
   wdData.next()
   initialTime = wdData.next()
   oldTime = float(initialTime[0])
   for row in wdData:
      tDiff = (float(row[0])-oldTime)*1000
      tJitter = tDiff-tTrigger
      if tJitter>maxValue:
         maxValue = tJitter
      if tJitter<minValue:
         minValue = tJitter
      if abs(tJitter)<Mtime[0]:
         if tJitter >= 0:
            Mpos[0] = Mpos[0] + 1
         else:
            Mneg[0] = Mneg[0] + 1
      elif abs(tJitter)<Mtime[1]:
         if tJitter >= 0:
            Mpos[1] = Mpos[1] + 1
         else:
            Mneg[1] = Mneg[1] + 1
      elif abs(tJitter)<Mtime[2]:
         if tJitter >= 0:
            Mpos[2] = Mpos[2] + 1
         else:
            Mneg[2] = Mneg[2] + 1
      elif abs(tJitter)<Mtime[3]:
         if tJitter >= 0:
            Mpos[3] = Mpos[3] + 1
         else:
            Mneg[3] = Mneg[3] + 1
      elif abs(tJitter)<Mtime[4]:
         if tJitter >= 0:
            Mpos[4] = Mpos[4] + 1
         else:
            Mneg[4] = Mneg[4] + 1
      elif abs(tJitter)>=Mtime[4]:
         if tJitter >= 0:
            Mpos[5] = Mpos[5] + 1
         else:
            Mneg[5] = Mneg[5] + 1
      tDiffStr = '%.3f' % tDiff
      tJitterStr = '%.3f' % tJitter
      count = count + 1
      avgTime = avgTime + tJitter
      oldTime=float(row[0])
   avgTime = avgTime / count

# Print out the calculated data
   tempStr = ""
   for x in range(0,79):
      tempStr = tempStr + "-"
   print ""
   print tempStr
   print "- Watchdog Statistics"
   print tempStr
   for x in range(len(Mpos)):
      print "M" + str(x) + "+  : " + str(Mpos[x])
      print "M" + str(x) + "-  : " + str(Mneg[x])
   print "MAX  : " + str(maxValue) + " ms"
   print "MIN  : " + str(minValue) + " ms"
   print "AVG  : " + str(avgTime) + " ms"
   print "CNT  : " + str(count)

# Print out a graph of the data
   print ""
   print tempStr
   print "- Graph"
   print tempStr
   for i in range(len(Mneg)):
      for x in range(0,(50*Mneg[i]/count)):
         MnegGraph[i] = MnegGraph[i] + graphChar
      for x in range(0,(50*Mpos[i]/count)):
         MposGraph[i] = MposGraph[i] + graphChar
   for x in reversed(range(len(MnegGraph))):
      print "M" + str(x) + "-  : " + MnegGraph[x]
   for x in range(len(MnegGraph)):
      print "M" + str(x) + "+  : " + MposGraph[x]
