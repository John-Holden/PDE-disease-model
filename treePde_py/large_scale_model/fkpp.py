import numpy as np
from scipy.ndimage import gaussian_filter
from treePde_py.mkdir import setup
import sys, os
import matplotlib.pyplot as plt


class Model:
    def __init__(self,  settings, fd_settings, epi_c=None):
        """
        :param settings:
        :param fd_settings:
        :param epi_c:
        """

        # Set domain and epidemic conditions
        # ______________________________________________________#
        input_dir = os.getcwd()+'/treePde_py/input_Sgm_data/'
        name = 'fkpp_{}_b_{}_ell_{}'.format(settings["data"],
                                                str(settings["beta"]).replace('.', '_'), str(settings['ell']))

        self.out_dir = os.getcwd()+'/model_data/' + name
        setup.mkdir(self.out_dir)  # make directories

        self.domain = 0.01 * np.genfromtxt(input_dir+settings["data"]+'.csv', delimiter=',')  # domain density
        if settings["subset"]:  # sub-set data for tests
            self.domain = self.domain[600:850, 300:550]

        self.shape = self.domain.shape
        self.sea_bcd = np.where(np.isnan(self.domain), 0, 1)  # sea boundary condition
        self.rho_space = np.load(input_dir+'/rho_values.npy')
        self.beta_space = np.load(input_dir+'/beta_values.npy')
        beta_ind = np.where(self.beta_space == settings["beta"])[0]  # get index of beta
        assert len(beta_ind) > 0  # Beta value not defined...
        # max_d = np.load(input_dir+'/max_d_arr.npy')
        # end_t = np.load(input_dir+'/end_t_arr.npy')
        # velocity = max_d/end_t
        velocity = np.load(input_dir+'/com_arr.npy')  # load ensemble velocity
        percolation = np.load(input_dir+'/perc_arr.npy')  # load ensemble percolation
        self.velocity = velocity[:, beta_ind]  # get beta-rho velocity mapping
        self.velocity = self.velocity * percolation[:, beta_ind]  # negate below percolation threshold
        self.velocity_map = self.get_subGrid_map()  # generate velocity mapping
        self.v_factor = 10
        self.d_factor = 5000
        self.g_factor = 0.25
        self.growth_map = np.ones_like(self.velocity_map)  # uniform growth map
        # ______________________________________________________#
        self.dx = fd_settings["dx"]
        self.dy = fd_settings["dy"]
        self.dt = fd_settings["dt"]
        # u_uk & u0_uk : field values of pde
        self.u_uk = np.zeros_like(self.domain)
        if epi_c is None:
            epix, epiy = int(self.domain.shape[0]/2), int(self.domain.shape[1]/2)
            self.u_uk[epiy, epix] = 1.0
        else:
            self.u_uk[epi_c[0], epi_c[1]] = 1

        self.u_uk = gaussian_filter(self.u_uk, sigma=1)
        self.u0_uk = np.copy(self.u_uk)
        assert self.dx == self.dy
        return

    def get_subGrid_map(self):
        """
        From sg_mapping function field vs rho, map to spatial domain
        """
        spatial_map = np.zeros(self.shape)  # define velocity field over UK
        rho_boundaries = {}
        # rho_boundaries : a dictionary with the form {i: [rho_low, rho_high} where is the index in rho-space
        for i in range(len(self.rho_space) - 1):
            rho_boundaries[i] = [self.rho_space[i], self.rho_space[i + 1]]
        max_density = rho_boundaries[i][1]  # maximum density in data
        for i, row in enumerate(self.domain):
            for j, col in enumerate(row):
                d_ij = self.domain[i, j]  # density value at point i,j
                if np.isnan(d_ij):  # if sea, then pass
                    pass
                else:  # if land region: map rho_ij to a velocity-space value
                    for rho_box in rho_boundaries:  # iterate through rho-space $ check against if == density_ij
                        boundary = rho_boundaries[rho_box]
                        # If density in the range interval then set map location density_ij == velocity(density)
                        if boundary[0] <= d_ij < boundary[1]:
                            spatial_map[i, j] = self.velocity[rho_box]
                        # CHECK if density bigger than rho given space
                        # - cap at highest given rho space boundary mapping
                        elif d_ij > max_density:  # if density above max density, cap to max value
                            spatial_map[i, j] = self.velocity[len(rho_boundaries) - 1]

        return spatial_map

    def run_fd_solver(self, tend, animate=False, freq=None):
        """
        Solve finite difference simulations
        :param fd_settings:
        :return:
        """
        from treePde_py.large_scale_model.fd_methods import fd_simulate
        # zeros = np.where(self.velocity_map == 0, 0, 1)
        # self.velocity_map = gaussian_filter(self.velocity_map, sigma=0.1)
        self.velocity_map = self.v_factor * self.velocity_map  # ~ m /day
        d_map = 0.25 * (self.velocity_map ** 2) / self.growth_map
        d_map, self.growth_map = [self.d_factor * d_map, self.g_factor * self.growth_map]  # control thickness of the front
        dd_map = ((d_map[2:, 1:-1] - d_map[:-2, 1:-1] + d_map[1:-1, 2:] - d_map[1:-1, :-2]) / (2 * self.dx))
        bcd = np.where(self.sea_bcd == 0)
        n_steps = int(tend / self.dt)
        freq = int(freq/self.dt)
        cfl = d_map.max() * self.dt / (self.dx ** 2)
        if cfl <= 0.500:  # Check CFL for stability
            pass
        else:
            print('cfl ', cfl)
            raise RuntimeError("Error: CFL is not satisfied.")
        print('cfl ', cfl)
        print('max v', self.velocity_map.max())
        print('nsteps ', n_steps)

        if 0:
            plt.title(' d map ')
            im = plt.imshow(d_map)
            plt.colorbar(im)
            plt.show()

            plt.title(' dd map ')
            im = plt.imshow(dd_map)
            plt.colorbar(im)
            plt.show()

        fd_simulate(domain=self.domain,d_map=d_map, dd_map=dd_map, g_map=self.growth_map,
                    u0_uk=self.u0_uk, u_uk=self.u_uk,
                    dx=self.dx, dy=self.dy, dt=self.dt,
                    n_steps=n_steps, bcd=bcd, animate=animate, freq=freq, save_dir=self.out_dir)

