import qplot as qplt
import pandas as pd
import numpy as np
import seaborn as sns
from numpy.polynomial import Polynomial

FILE_PATH = './DATA/freq_char.csv'

qplt.set_paper_style(single_column=True)

df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()

print("Columns: ", df.columns, ' | count: ', df.t.count())

# Plot the response in a subplot
qplt.subplots(df.t, signals=[[df.y], [df.u], [df.status]], ylabels=[r'$\varphi [^\circ]$', 'u [%PWM]', 'status'], titles=['System Response', 'Input Signal', 'Measurement Status'], labels=[r'$\varphi$','u', 'status'], savepath='freq_char_measurement.pdf')



print("All done!")