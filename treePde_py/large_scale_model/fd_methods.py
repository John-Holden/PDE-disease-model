"""
Methods and functions used to numerically simulate model.
do
"""
import sys
import numpy as np

def do_timestep(u0, u, d, dd, g, dt, dx, dy, dx2, dy2):
    """
    FTCD solver
    :param u0: field value at t-1
    :param u:  field value at t
    :param D:  diffusion coefficient
    :param gamma: growth constant
    :param dt: time step function
    :param dx2: x direction discreteization
    :param dy2: y...
    :return: u0, u arrays containing field values at t, t+1
    """

    # Advection term
    u[1:-1, 1:-1] = u[1:-1, 1:-1] + dt * dd * \
                    ((u0[2:, 1:-1] - u0[:-2, 1:-1] + u0[1:-1, 2:] - u0[1:-1, :-2]) / (2*dy))  # Advection

    # Laplacian term
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + d[1:-1, 1:-1] * dt * (
                 (u0[2:, 1:-1] - 2 * u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
                 + (u0[1:-1, 2:] - 2 * u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2)

    # Logistic growth
    u[1:-1, 1:-1] = u[1:-1, 1:-1] + dt * g[1:-1, 1:-1] * u[1:-1, 1:-1] * (1 - u[1:-1, 1:-1])

    if u.min() < 0:
        print('min: ', u.min())
        u[np.where(u < 0)] = 0  # correct for errors ?
        sys.exit()

    if u.max() > 1:
        print('max: ', u.max())
        u[np.where(u > 1)] = 1  # correct for errors ?


    u0 = u.copy()
    return u0, u


def fd_simulate(dx, dy, dt, d_map, dd_map, bcd, g_map, u0_uk, u_uk, n_steps):
    """
    :param model_params: dict of parameters used
    :param FD_settings:  Finite Difference setup
    :param maps:  Data sources used
    :param save_path: output data location
    :return: inf_tseries, the number of infected trees per step
    """

    # ------- Begin Finite Difference Simulations ------- #
    #
    import matplotlib.pyplot as plt

    for t in range(n_steps):
        # Call FTCD function
        u0_uk, u_uk = do_timestep(u0_uk, u_uk, d_map, dd_map , g_map, dt, dx, dy, dx2=dx ** 2, dy2=dy ** 2)
        u_uk[0], u_uk[-1], u_uk[:, 1], u_uk[:, -1] = [0, 0, 0, 0]  # Enforce boundary conditions
        u0_uk[0], u0_uk[-1], u0_uk[:, 1], u0_uk[:, -1] = [0, 0, 0, 0]
        u_uk[bcd], u0_uk[bcd] = 0, 0
        if t % 2000 == 0:
            plt.title('t = {}'.format(t))
            im = plt.imshow(u_uk)
            plt.colorbar(im)
            plt.show()


