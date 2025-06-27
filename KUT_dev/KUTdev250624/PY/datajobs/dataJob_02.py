# -*- coding: utf-8 -*-

import numpy as np




#------------------------------------------------------------------------------

dataRepoDir = './dataRepo/'





#------------------------------------------------------------------------------


# assuming datasetDict and data_pot are defined

data_main = np.loadtxt(
    datasetDict[data_pot]['dataRepoPath'] + datasetDict[data_pot]['dataFile_main'], 
    delimiter=',', 
)

data_inputTable = np.loadtxt(
    datasetDict[data_pot]['dataRepoPath'] + datasetDict[data_pot]['dataFile_inputTable'], 
    delimiter=',', 
)

steadyDurationPercent = datasetDict[data_pot]['steadyDurationPercent']

#-------------------------------------

for tmpidx in range(0,len(data_inputTable[:,0])):

    stairTime_start = data_inputTable[tmpidx,0]

    if tmpidx < len(data_inputTable[:,0])-1:
        stairTime_stop = data_inputTable[tmpidx+1,0]
    else:
        stairTime_stop = data_main[-1,0]

    steadyTime_start = stairTime_start + (stairTime_stop-stairTime_start)*(100-steadyDurationPercent)/100

    tmp_mask = (data_main[:,0] >= steadyTime_start) & (data_main[:,0] < stairTime_stop)

    tmp_time = data_main[tmp_mask,0]
    tmp_sigOut = data_main[tmp_mask,1]
    tmp_sigIn = data_main[tmp_mask,3]


    np.savetxt(dataRepoDir + 'SCH_' + data_pot + '_span_{:02d}'.format(tmpidx) + '.csv',
        np.column_stack((tmp_time, tmp_sigOut, tmp_sigIn)),
        delimiter=',',
        fmt='%.3f',
        header='time,sigOut,sigIn',
        comments='',
    )










