import os
import qplot as qplt
import pandas as pd
import numpy as np
import seaborn as sns
from numpy.polynomial import Polynomial

FILE_PATH = './DATA/freq_char.csv'

qplt.set_paper_style(single_column=True)

dfraw = pd.read_csv(FILE_PATH)
dfraw.columns = dfraw.columns.str.strip()

print("Columns: ", dfraw.columns, ' | count: ', dfraw.t.count())

# Clean data: only keep t >= 10s to avoid transients
tidxclean = dfraw['t'] >= 10
df = dfraw[tidxclean]
print("After cleaning, data count: ", df.t.count())
df.to_csv('./DATA/freq_char_clean.csv', index=False)

# Plot the response in a subplot
qplt.subplots(df.t, signals=[[df.y], [df.u], [df.freq]], xlabels=['t [s]'], ylabels=[r'$\varphi [^\circ]$', 'u [%PWM]', 'f [Hz]'], titles=['System Response', 'Input Signal', 'Frequency'], labels=['y','u', 'f'], savepath='freq_char_measurement.pdf')

status_start_idx = np.where(df.status == 1)[0]
status_end_idx = np.where(df.status == -1)[0]
status_changes = list(zip(status_start_idx, status_end_idx))

amps = np.array([])
phases = np.array([])
freqs = np.array([])

for i, (start_idx, end_idx) in enumerate(status_changes):
    print(f"Status change from index {start_idx} to {end_idx}, time {df.t.iloc[start_idx]}s to {df.t.iloc[end_idx]}s")
    y = df.y[start_idx:end_idx]
    u = df.u[start_idx:end_idx]
    t = df.t[start_idx:end_idx]
    yhalf_idx = (start_idx + end_idx) // 2  # midpoint index in df space
    yhalf = y.shape[0] // 2  # midpoint index in segment space
    freq = df.freq.iloc[yhalf_idx]
    # Find the amplitude and phase shift
    amplitude_in = (np.max(u) - np.min(u)) / 2
    amplitude_out = (np.max(y) - np.min(y)) / 2
    amp = amplitude_out / amplitude_in
    phase_shift = t.iloc[np.argmax(y[yhalf:])] - t.iloc[np.argmax(u[yhalf:])]
    phase_shift_deg = (phase_shift * freq * 360) % 360  # in degrees
    phases = np.append(phases, phase_shift_deg)
    freqs = np.append(freqs, freq)
    amps = np.append(amps, amp)
    y_norm_zero = y - np.mean(y).__float__()
    u_norm_zero = u - np.mean(u).__float__()
    qplt.plot(
        t,
        signals=[y_norm_zero/np.max(np.abs(y_norm_zero)), u_norm_zero/np.max(np.abs(u_norm_zero))],
        xlabel='t [s]',
        ylabel='Amplitude',
        title=f"System Response\nf={freq:.1f}Hz, A={amp:.2f}, $\\Delta\\varphi={phase_shift_deg:.1f}^\\circ$",
        savepath=f'y_segment_{freq}Hz.pdf',
        show_plot=False,
        show_legend=False,
    )
    
# Plot Bode plots
qplt.subplots(freqs, signals=[[amps], [phases]], xlabels=['Frequency [Hz]'], ylabels=['Amplitude', 'Phase [deg]'], titles=['Bode Plot - Amplitude', 'Bode Plot - Phase'], labels=['Amplitude', 'Phase'], savepath='freq_char_bode.pdf')

df_bode = pd.DataFrame({'Frequency_Hz': freqs, 'Amplitude': amps, 'Phase_deg': phases})
df_bode.to_csv('./DATA/freq_char_bode.csv', index=False)



print("All done!")