# -*- coding: utf-8 -*-

import numpy as np

# Pomocne moduly a funkcie ku kresleniu obrazkov
import sys
sys.path.append('./figjobs/')
from figFcns_TeX import *

import os

#------------------------------------------------------------------------------


figSaveDir = './fig/'

figName = 'fj_01_' + selectedFile











#------------------------------------------------------------------------------

PANELNAME = 'panel_1'

#------------------

figPlotParam = fcnDefaultFigSize(5.5, 0.17, (1-0.14), 0.14, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])

subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(workdata_t, workdata_y,
         '-', lw=0.7, color='k',
        #  ms=2, mfc='none', mec='k', mew=0.3,
         drawstyle='steps-post',
        #  label='meranie',
         )



#---------------------------------------------
# determine y lim for LinearLocator
tmpMax = np.ceil(np.max(np.abs(  workdata_y  )))
ax0.set_ylim([-tmpMax, tmpMax])

#---------------------------------------------

XYT_labels = ['čas [s]', '[°]', 'Výstupný signál (poloha, uhol ramena kyvadla)']

fcn_setFigStyle_basicTimeSeries_var2(fig, figPlotParam, XYT_labels)

#---------------------------------------------

plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()


# save plotted data for panel_1 as CSV
plotData = np.vstack((workdata_t, workdata_y)).T
np.savetxt(figSaveDir + figName + '_' + PANELNAME +'.csv', 
           plotData, 
           delimiter=',', header='plotData_x,plotData_y', fmt='%.6e',
           )







#------------------------------------------------------------------------------

PANELNAME = 'panel_2'

#------------------

figPlotParam = fcnDefaultFigSize(4.25, 0.17, (1-0.15), 0.15, 0.5, 13)
fig = plt.figure(figsize=figPlotParam[0:2])


subPlots = gridspec.GridSpec(1, 1,
                             # height_ratios=[40, 40, 20],
                             )

#---------------------------------------------
ax0 = plt.subplot(subPlots[0])


ax0.plot(workdata_t, np.deg2rad(workdata_dy),
         '-', lw=0.7, color='k',
        #  ms=2, mfc='none', mec='k', mew=0.3,
         drawstyle='steps-post',
        #  label='meranie',
         )


#---------------------------------------------
# determine y lim for LinearLocator
tmpMax = np.ceil(np.max(np.abs(np.deg2rad(workdata_dy))))
ax0.set_ylim([-tmpMax, tmpMax])

#---------------------------------------------

XYT_labels = ['čas [s]', '[rad/s]', 'Uhlová rýchlosť ']

fcn_setFigStyle_basicTimeSeries_var2(fig, figPlotParam, XYT_labels)

#---------------------------------------------

plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.png', dpi=240)
plt.savefig(figSaveDir + figName + '_' + PANELNAME +'.pdf')

plt.close()

# save plotted data for panel_1 as CSV
plotData = np.vstack((workdata_t, workdata_y)).T
np.savetxt(figSaveDir + figName + '_' + PANELNAME +'.csv', 
           plotData, 
           delimiter=',', header='plotData_x,plotData_y', fmt='%.6e',
           )








