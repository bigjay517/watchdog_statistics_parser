import csv
# Configure margins here in ms
M0time = 0.005
M1time = 0.010
M2time = 0.020
M3time = 0.050
M4time = 0.200

# Configure trigger time in ms
tTrigger = 1

# Configure File here
watchdogData = 'watchdog_testing.csv'

# Graph drawing
graphChar = "X"

# Initialize vars
M0pos = 0
M0neg = 0
M1pos = 0
M1neg = 0
M2pos = 0
M2neg = 0
M3pos = 0
M3neg = 0
M4pos = 0
M4neg = 0
MXpos = 0
MXneg = 0
maxValue = 0
minValue = 0
count = 0
avgTime = 0
M0negGraph = ""
M0posGraph = ""
M1negGraph = ""
M1posGraph = ""
M2negGraph = ""
M2posGraph = ""
M3negGraph = ""
M3posGraph = ""
M4negGraph = ""
M4posGraph = ""
MXnegGraph = ""
MXposGraph = ""

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
      if abs(tJitter)<M0time:
         if tJitter >= 0:
            M0pos = M0pos + 1
         else:
            M0neg = M0neg + 1
      elif abs(tJitter)<M1time:
         if tJitter >= 0:
            M1pos = M1pos + 1
         else:
            M1neg = M1neg + 1
      elif abs(tJitter)<M2time:
         if tJitter >= 0:
            M2pos = M2pos + 1
         else:
            M3neg = M2neg + 1
      elif abs(tJitter)<M3time:
         if tJitter >= 0:
            M3pos = M3pos + 1
         else:
            M4neg = M3neg + 1
      elif abs(tJitter)<M4time:
         if tJitter >= 0:
            M4pos = M4pos + 1
         else:
            M4neg = M4neg + 1
      elif abs(tJitter)>=M4time:
         if tJitter >= 0:
            MXpos = MXpos + 1
         else:
            MXneg = MXneg + 1
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
   print "M0+  : " + str(M0pos)
   print "M0-  : " + str(M0neg)
   print "M1+  : " + str(M1pos)
   print "M1-  : " + str(M1neg)
   print "M2+  : " + str(M2pos)
   print "M2-  : " + str(M2neg)
   print "M3+  : " + str(M3pos)
   print "M3-  : " + str(M3neg)
   print "M4+  : " + str(M4pos)
   print "M4-  : " + str(M4neg)
   print "MX+  : " + str(MXpos)
   print "MX-  : " + str(MXneg)
   print "MAX  : " + str(maxValue) + " ms"
   print "MIN  : " + str(minValue) + " ms"
   print "AVG  : " + str(avgTime) + " ms"
   print "CNT  : " + str(count)

# Print out a graph of the data
   print ""
   print tempStr
   print "- Graph"
   print tempStr
   for x in range(0,(50*M0neg/count)):
      M0negGraph = M0negGraph + graphChar
   for x in range(0,(50*M0pos/count)):
      M0posGraph = M0posGraph + graphChar
   for x in range(0,(50*M1neg/count)):
      M1negGraph = M1negGraph + graphChar
   for x in range(0,(50*M1pos/count)):
      M1posGraph = M1posGraph + graphChar
   for x in range(0,(50*M2neg/count)):
      M2negGraph = M2negGraph + graphChar
   for x in range(0,(50*M2pos/count)):
      M2posGraph = M2posGraph + graphChar
   for x in range(0,(50*M3neg/count)):
      M3negGraph = M3negGraph + graphChar
   for x in range(0,(50*M3pos/count)):
      M3posGraph = M3posGraph + graphChar
   for x in range(0,(50*M4neg/count)):
      M4negGraph = M4negGraph + graphChar
   for x in range(0,(50*M4pos/count)):
      M4posGraph = M4posGraph + graphChar
   for x in range(0,(50*MXneg/count)):
      MXnegGraph = MXnegGraph + graphChar
   for x in range(0,(50*MXpos/count)):
      MXposGraph = MXposGraph + graphChar
   print "MX-  : " + MXnegGraph
   print "M4-  : " + M4negGraph
   print "M3-  : " + M3negGraph
   print "M2-  : " + M2negGraph
   print "M1-  : " + M1negGraph
   print "M0-  : " + M0negGraph
   print "M0+  : " + M0posGraph
   print "M1+  : " + M1posGraph
   print "M2+  : " + M2posGraph
   print "M3+  : " + M3posGraph
   print "M4+  : " + M4posGraph
   print "MX+  : " + MXposGraph
