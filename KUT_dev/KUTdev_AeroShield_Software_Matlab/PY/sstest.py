import numpy as np
from ssmodel import StateSpaceModel as ss
import qplot

F = 0.0

k = 3
m = 20
c = 5

A = np.array([[0, 1], [-k/m, -c/m]], dtype=np.float32)
B = np.array([[0, 1/m]], dtype=np.float32).T
C = np.array([[1, 0]], dtype=np.float32)
D = np.array([[0]], dtype=np.float32)

x_init = np.array([[0, 0]], dtype=np.float32).T

t = 0.0
t_stop = 60
dt = 0.01

Gs = ss(A, B, C, D, x_init=x_init, dt=dt)

# t, y, x, u = Gs.step(F, t_stop=t_stop)

# xs = np.array(x).T

# qplot.subplots(t, signals=[[y],[u]], ylabels=['Output [rad]','Force [N]'], xlabels=['t [s]'], labels=[['out'],['u']], titles=['Step response', 'Control response'], savepath='pendulum.pdf')
# qplot.plot(xs[0][0], signals=[xs[0][1]], ylabel='x2 [rad/s]', xlabel='x1 [rad]', labels=['traj'], title='Phase portrait', savepath='pendulum_phase_portrait_states.pdf')

Gs.reset()

# PID example

r = np.pi/4

P = 2
I = 1.5
D = 0.75

e_old = 0
e_int = 0
e_der = 0

column_names = ['t','r','y','u','e','de','x1','x2']
logsout = []

y = Gs.y

while t < t_stop:
	e = r - y
	de = (e - e_old)
	e_der = de/dt
	e_int += e * dt
	e_old = e

	u = P * e + I * e_int + D * e_der

	Gs.compute(u)

	y = Gs.y
	x1 = Gs.x.copy().flatten()[0]
	x2 = Gs.x.copy().flatten()[1]

	logsout.append([t, r, y.flatten(), u.flatten(), e.flatten(), de.flatten(), x1, x2])
	t += dt


import pandas as pd
df = pd.DataFrame(logsout, columns=column_names)
df.to_csv("logsout.csv", index=False)

qplot.subplots(df.t, signals=[[df.r, df.y], [df.u]], reference_signal=df.r, xlabels=['t [s]'], ylabels=['angle [rad]', 'input [N]'], titles=['System response', 'Control output'], labels=[['r','y'],'u'], savepath='pendulum_pid.pdf')
qplot.plot(df.e, signals=[df.de], xlabel='x1 [rad]', ylabel='x2 [rad/s]', title='Phase portrait', savepath='pp_pid.pdf')
