def dynSysFyzKyv_suchvisk_v0(x, t, p):

    x_1, x_2 = x

    L_T_kyv, m_kyv, I_kyv, Fc0_kyv, Fc1_kyv = p

    g = 9.81  
    hc = 10**6

    if x_2 == 0:
        taus = - (m_kyv * g * L_T_kyv) * np.sin(x_1)
        if np.abs(taus) >= Fc0_kyv:
            tau0 = Fc0_kyv * np.tanh(hc*x_1)
        else:
            tau0 = taus
    else:
        tau0 = Fc0_kyv * np.tanh(hc*x_2)

    tau1 = Fc1_kyv * x_2
  
    dotx_1 = x_2
    dotx_2 = - (1/I_kyv) * (m_kyv * g * L_T_kyv) * np.sin(x_1) - (1/I_kyv) * tau0 - (1/I_kyv) * tau1

    return [dotx_1, dotx_2]