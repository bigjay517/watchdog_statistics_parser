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
      for x in range(len(Mpos)):
         if (x == (len(Mpos)-1)):
            if tJitter >=0:
               Mpos[x] = Mpos[x] + 1
               break
            else:
               Mneg[x] = Mneg[x] + 1
               break
         if abs(tJitter)<Mtime[x]:
            if tJitter >= 0:
               Mpos[x] = Mpos[x] + 1
               break
            else:
               Mneg[x] = Mneg[x] + 1
               break
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
