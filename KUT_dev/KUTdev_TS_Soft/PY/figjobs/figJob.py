import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from figFcns_TeX import *

# ===== Params =====
figSaveDir = '../fig'
os.makedirs(figSaveDir, exist_ok=True)

figName = 'snimac2_output'

# load CSV
data_main = pd.read_csv(
    '../dataRepo/demo.csv', 
    header=None
).values  

# ===== Panel =====

figPlotParam = fcnDefaultFigSize(6, 0.17, 0.88, 0.12, 0.4, 13)
fig = plt.figure(0, figsize=figPlotParam[0:2])
subPlots = gridspec.GridSpec(1, 1)
ax0 = plt.subplot(subPlots[0])


ax0.plot(data_main[:, 0], data_main[:, 4],
         '-', lw=0.5, color='k',
         drawstyle='default'
         )

fcnDefaultLayoutAdj(fig, figPlotParam[2], figPlotParam[3], figPlotParam[4], figPlotParam[5])
fcn_setFigStyle_basicTimeSeries(fig, figPlotParam, ['Čas [s]', 'Výstup [V]', 'Snímač 2'])
ax0.grid(True, which='both', linestyle='--', linewidth=0.1, color='k')

# ax0.set_xlim(0, 255)
# ax0.set_ylim(0, 1023)

plt.savefig(os.path.join(figSaveDir, f"{figName}.png"))
plt.close()




