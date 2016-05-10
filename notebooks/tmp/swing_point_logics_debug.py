from scipy.io import loadmat, savemat
import numpy as np
import pandas as pd


EXO_File = 'strategy_880131'

mat = loadmat('../../mat/'+EXO_File+'.mat')

sphThreshold = 8 # ????
splThreshold = 8 # ????


signalArray = mat['optStr']['entrySignalingSeries'][0][0]
volumeArray =  mat['optStr']['volumeSeries'][0][0][0]

OPEN  = 0; HIGH  = 1; LOW   = 2;  CLOSE = 3;

if len(signalArray) == 1:
    OPEN  = HIGH  = LOW = CLOSE = 0

currentHigh  = -np.inf #intmin('int32');
currentLow   = np.inf #intmax('int32');

currentHVol  = 0
currentLVol  = 0
sphDays      = 0
splDays      = 0
sphStart     = 1
splStart     = 1
sphMaxDay    = 0
splMinDay    = 0
prevHigh     = signalArray[HIGH][0]
prevLow      = signalArray[LOW][0]
prevHVol     = volumeArray[0]
prevLVol     = volumeArray[0]


nDays        = len(signalArray[CLOSE])

sphIndicator = np.zeros(nDays)
splIndicator = np.zeros(nDays)

sphLevel = np.zeros(nDays)
splLevel = np.zeros(nDays)

sphVolume = np.zeros(nDays)
splVolume = np.zeros(nDays)

for dday in range(nDays):

    if signalArray[HIGH][dday] > currentHigh:
        currentHigh = signalArray[HIGH][dday]
        currentHVol = volumeArray[dday]
        sphMaxDay   = dday;
        sphDays     = 0.0;
    else:
        sphDays = sphDays+1;

    if signalArray[LOW][dday] < currentLow:
        currentLow = signalArray[LOW][dday]
        currentLVol = volumeArray[dday]
        splMinDay  = dday
        splDays    = 0
    else:
        splDays = splDays+1;



    if sphDays > sphThreshold:
        sphLevel[dday] = currentHigh;
        sphIndicator[dday] = 1;
        sphVolume[dday] = currentHVol;

        for dd in range(sphStart, dday): #?? or dday-1
            sphLevel[dd] = prevHigh
            sphVolume[dd]= prevHVol

        prevHigh = currentHigh
        prevHVol = currentHVol
        sphStart = dday
        sphDays = 0
        currentHigh = -np.inf #intmin('int32');

    elif dday > 1:
        sphVolume[dday] = sphVolume[dday-1]
    elif dday == 1:
        sphVolume[dday] = volumeArray[dday]




    if splDays > splThreshold:
        splLevel[dday] = currentLow;
        splIndicator[dday] = 1;
        splVolume[dday] = currentLVol;

        for dd in range(splStart, dday):  #??? or dday-1
            splLevel[dd] = prevLow
            splVolume[dd] = prevLVol

        prevLow = currentLow
        prevLVol = currentLVol
        splStart = dday
        splDays = 0
        currentLow =  np.inf #intmax('int32');
    elif dday > 1:
        splVolume[dday] = splVolume[dday-1]
    elif dday == 1:
        splVolume[dday] = volumeArray[dday]

    # fill to the end
    for dd in range(sphStart, nDays):
        sphLevel[dd] = prevHigh;
        sphVolume[dd] = prevHVol;

    for dd in range(splStart, nDays):
        splLevel[dd] = prevLow;
        splVolume[dd] = prevLVol;