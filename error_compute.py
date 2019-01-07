import numpy as np
import matplotlib.pyplot as plt

#Read the file
teamName = 'zhra'
teamName_ = 'zhra'

gtStartTime = 0
gtDataList = []
with open("IPSN2018_officialData\\ipsn3D\\" +teamName + "\\gt.txt", "rt") as file:
    for line in file:
        if(gtStartTime < 1):
            gtStartTime = float(line)
        else: 
            gtDataList.append([float(x) for x in line.split(',')])
gtData = np.array(gtDataList, dtype = 'float64')


myStartTime = 0
myDataList = []
with open("IPSN2018_officialData\\ipsn3D\\" + teamName + "\\team-" + teamName_ + ".txt", "rt") as file:
    for line in file:
        if(myStartTime < 1):
            myStartTime = float(line)
        else:
            myDataList.append([float(x) for x in line.split(',')])
myData = np.array(myDataList, dtype = 'float64')            

#step 1: calibration of time

#broadcasting
gtData = gtData - np.array([0,0,0,gtStartTime])
myData = myData - np.array([0,0,0,myStartTime])

#step 2: delete useless myData
while(myData[-1][3] > gtData[-1][3]):
    myData = np.delete(myData,-1,axis = 0)

#step 3: compute error
errors = np.zeros(myData.shape[0])

j = 0# gtData pointer
for i in range(myData.shape[0]):
    while(myData[i][3]>gtData[j][3]):
        j = j + 1
    #插值后的真值
    gtCoordinate = (gtData[j-1][0:3] * (myData[i][3] - gtData[j-1][3]) + gtData[j][0:3] * (gtData[j][3] - myData[i][3]))/(gtData[j][3] - gtData[j-1][3])
    #测量值
    myCoordinate = myData[i][0:3]
    errors[i] = np.linalg.norm(gtCoordinate - myCoordinate)


#analysis

meanError = np.average(errors)
print('meanError = ', meanError)

stdError = np.std(errors)
print('stdError= ', stdError)

maxError = np.max(errors)
print('maxError= ', maxError)

minError = np.min(errors)
print('minError= ', minError)

#CDF
errorsSorted = np.sort(errors)
p = np.arange(len(errors)) / (len(errors) - 1)
plt.plot(errorsSorted,p)
plt.grid(True)