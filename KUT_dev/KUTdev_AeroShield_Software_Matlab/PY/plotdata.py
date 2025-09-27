from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import qplot


datafile = "../DATA/data.csv"

sns.set_theme(style="ticks", palette="gray", context="paper")  # clean look
# sns.set_palette("whiteblack")  # grayscale palette
# sns.set_theme(style="ticks", palette="muted", context="paper")
sns.set_context("paper", font_scale=1.2)


df = pd.read_csv(datafile)
df.columns = df.columns.str.strip()

qplot.plot(df.t, signals=[df.r, df.y], labels=['ref','out'], title='Control Response', reference_signal=df.r, savepath='test.pdf')

qplot.subplots(df.t, signals=[[df.r, df.y], [df.u]], labels=[['r','y'],['u']], titles=['System Response', 'Control Output'], ylabels=['angle [deg]', 'PWM [%]'], xlabels=['t [s]'], reference_signal=df.r, savepath='multiplot.pdf')

# plt.figure(figsize=(8, 5))
# sns.lineplot(df, x='t', y='y', label="output", linestyle='-')
# sns.lineplot(df, x='t', y='r', label="reference", linestyle='--')

# # plt.plot(df.t, df.y)
# # plt.plot(df.t, df.r)

# plt.xlabel("t [s]")
# plt.ylabel("angle [deg]")
# plt.title("PID Control Response")
# plt.legend(frameon=False)
# plt.grid(True)
# sns.despine()  # remove top/right spines for a clean article look
# plt.tight_layout()
# plt.savefig("test.png")



