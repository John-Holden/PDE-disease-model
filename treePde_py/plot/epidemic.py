import matplotlib.pyplot as plt
import sys, os
import numpy as np
import matplotlib.colors as mcolors


class PltStep:
    def __init__(self, bcd, domain, save):
        colors1= plt.cm.Greens_r(np.linspace(0., 1, 128))  # +ve trees/map
        colors2 = plt.cm.Reds(np.linspace(0, 1, 128))  # -nve infection
        colors = np.vstack((colors1, colors2))
        self.cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
        sea = np.zeros_like(domain)
        sea[bcd] = np.nan
        self.domain = np.copy(domain)
        self.domain[bcd] = 0
        self.domain[np.where(self.domain > 0.1)] = 0.1
        self.domain = self.domain + 0.05
        self.domain = self.domain / self.domain.max()
        self.sea = sea
        self.save_dir = save
        return

    def step(self, u_uk, c=None, freq=None, dt=None, title=True, sim_plt=True):
        """
        :param u_uk:
        :param domain:
        :param c:
        :return:
        """

        self.domain[np.where(u_uk > 0.001)] = 0  # take away infection from domain
        fig, ax = plt.subplots(figsize=(5, 6))
        # fig, ax = plt.subplots()

        # im = ax.pcolormesh(((u_uk/u_uk.max()) - self.domain) + self.sea, cmap=self.cmap)
        # im = ax.pcolor(((u_uk/u_uk.max()) - self.domain) + self.sea, cmap=self.cmap)
        # plt.gca().invert_yaxis()

        im = ax.imshow(((u_uk/u_uk.max()) - self.domain) + self.sea, cmap=self.cmap)
        if title:
            ax.set_title('t = {}'.format(c * freq * dt))
        plt.colorbar(im)
        ax.set_aspect("auto")
        if sim_plt:
            plt.savefig(self.save_dir + '/time_series/{}.pdf'.format(c))
        else:
            plt.savefig(self.save_dir + '/{}.pdf'.format(c))
        plt.show()
        return

