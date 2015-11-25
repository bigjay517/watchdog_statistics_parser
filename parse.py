# Author: Jason Learst, Vector CANtech Inc.
# Version: 1.00.00 (2015-11-24)
#
# Info: This script analyzes a CSV file created by the Logic software from the Saleae Logic Analyzer, and generates
#       watchdog timing statistics.
import csv

#########################################################################################################################
# Configuration
#########################################################################################################################
# Configure margins here in ms
Mtime = (0.005, 0.010, 0.020, 0.050, 0.200)

# Configure trigger time in ms
tTrigger = 1

# Configure File here
watchdogData = 'watchdog_testing.csv'

# Character to draw the graph with
graphChar = "X"

#########################################################################################################################
# Variables
#########################################################################################################################
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
divLine = ""
for x in range(0,79):
   divLine = divLine + "-"

#########################################################################################################################
# Functions
#########################################################################################################################

# Output a visual block to the console
def printBlock(message):
   print ""
   print divLine
   print "- " + message
   print divLine

#########################################################################################################################
# Main
#########################################################################################################################
# Open CSV file parse the data
with open(watchdogData, 'rb') as csvfile:
   wdData = csv.reader(csvfile, delimiter=',', quotechar='|', skipinitialspace='true')
   # ignore the column headers
   wdData.next()
   wdData.next()
   initialTime = wdData.next()
   oldTime = float(initialTime[0])
   for row in wdData:
      tDiff = (float(row[0])-oldTime)*1000
      tJitter = tDiff-tTrigger
      # Check for min and max values
      if tJitter>maxValue:
         maxValue = tJitter
      if tJitter<minValue:
         minValue = tJitter
         # Loop through array of Margins and +1 the bucket this tick belongs to
         # break once the bucket is updated so same tick does not add to more than one bucket
      for x in range(len(Mpos)):
         # if we are at last index of Mpos/Mneg, this value goes in the greater than max margin bucket
         if (x == (len(Mpos)-1)):
            if tJitter >=0:
               Mpos[x] = Mpos[x] + 1
               break
            else:
               Mneg[x] = Mneg[x] + 1
               break
         # Check if the value is less than the current margin Mtime[x], if yes it belongs in this bucket if not x++
         if abs(tJitter)<Mtime[x]:
            if tJitter >= 0:
               Mpos[x] = Mpos[x] + 1
               break
            else:
               Mneg[x] = Mneg[x] + 1
               break
      tDiffStr = '%.3f' % tDiff
      tJitterStr = '%.3f' % tJitter
      # Increment data count and update running AvgTime calculation
      count = count + 1
      avgTime = avgTime + tJitter
      oldTime=float(row[0])
   avgTime = avgTime / count

# Print out the calculated data
   printBlock("Watchdog Statistics")
   for x in range(len(Mpos)):
      print "M" + str(x) + "+  : " + str(Mpos[x])
      print "M" + str(x) + "-  : " + str(Mneg[x])
   print "MAX  : " + str(tTrigger + maxValue) + " ms"
   print "MIN  : " + str(tTrigger + minValue) + " ms"
   print "AVG  : " + str(tTrigger + avgTime) + " ms"
   print "CNT  : " + str(count)

# Print out a graph of the data
   printBlock("Graph")
   # Generate the graph data by using the % of counts in each bucket
   for i in range(len(Mneg)):
      for x in range(0,(50*Mneg[i]/count)):
         MnegGraph[i] = MnegGraph[i] + graphChar
      for x in range(0,(50*Mpos[i]/count)):
         MposGraph[i] = MposGraph[i] + graphChar
   # Print the data in order from early calls to late calls of WDTrigger
   for x in reversed(range(len(MnegGraph))):
      print "M" + str(x) + "-  : " + MnegGraph[x]
   for x in range(len(MnegGraph)):
      print "M" + str(x) + "+  : " + MposGraph[x]
