import numpy as np

class StateSpaceModel:
	A: np.ndarray
	B: np.ndarray
	C: np.ndarray
	D: np.ndarray
	dt: float
	x_init: np.ndarray
	t: float
	x: np.ndarray
	dx: np.ndarray
	y: float
	norder: int

	def __init__(self, A: np.ndarray, B: np.ndarray, C: np.ndarray, D: np.ndarray | int = 0, x_init: np.ndarray = np.array([0.0]), dt: float = 0.01):
		self.norder = A.shape[0]
		if B.shape[0] != self.norder:
			raise Exception(f"Matrix B is required to be of size ({self.norder}, 1)")
		if C.shape[1] != self.norder:
			raise Exception(f"Matrix C is required to be of size (1, {self.norder})")
		if isinstance(D, np.ndarray) and D.shape[0] != B.shape[1]:
			raise Exception(f"Matrix D is required to be of size (1, {self.norder})")
		elif isinstance(D, int):
			self.D = np.ones([B.shape[1], B.shape[0]]) * D
		self.A = A
		self.B = B
		self.C = C
		self.D = D
		self.dt = dt
		self.x_init = x_init if x_init.shape == B.shape else x_init[0] * np.ones(B.shape)
		self.reset()

	def getModel(self):
		return self.A, self.B, self.C, self.D

	def computeY(self, u):
		return self.C @ self.x + self.D @ u

	def reset(self):
		self.dx = np.zeros(self.B.shape)
		self.x = self.x_init.copy()
		self.t = 0.0
		self.y = self.computeY(np.array([[0]]))

	def dxdt(self, x, u):
		return self.A @ x + self.B @ u

	def compute(self, u = 0.0):
		if not isinstance(u, np.ndarray):
			u = np.array([u if isinstance(u, list) else [u]]).T

		k1 = self.dxdt(self.x, u)
		k2 = self.dxdt(self.x + 0.5 * self.dt * k1, u)
		k3 = self.dxdt(self.x + 0.5 * self.dt * k2, u)
		k4 = self.dxdt(self.x + self.dt * k3, u)

		self.dx = (k1 + 2*k2 + 2*k3 + k4)
        
		self.x += (self.dt / 6.0) * self.dx
		
		self.y = self.computeY(u)

		return self.y

	def step(self, u: float, t_stop: float = 10.0):
		xs, ys, ts, us = [], [], [], []
		while(self.t < t_stop):
			y = self.compute(u)
			xs.append(self.x.copy())
			ys.append(y.flatten())
			us.append(u)
			ts.append(self.t)
			self.t += self.dt
		return ts, ys, xs, us


