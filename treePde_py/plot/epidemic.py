import matplotlib.pyplot as plt
import sys, os
import numpy as np
import matplotlib.colors as mcolors


class PltStep:
    def __init__(self, bcd, domain, vmap, save=None):
        colors1 = plt.cm.Greens_r(np.linspace(0., 1, 128))  # +ve trees/map
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
        self.domain[np.where(vmap == 0)] = 0.05  # turn insusceptible regions to white-space
        self.sea = sea
        if save is None:
            self.save_dir = os.getcwd()
        else:
            self.save_dir = save
        return

    def labeler(self, c):
        """
        save in binary
        :param c:
        :return:
        """
        if c < 10:
            return '0000' + str(c)
        if c < 100:
            return '000' + str(c)
        if c < 1000:
            return '00' + str(c)
        if c < 10000:
            return '0' + str(c)

    def step(self, u_uk, c=None, title=None, sim_plt=True, show=True, ext=None):
        """
        :param u_uk:
        :param domain:
        :param c:
        :return:
        """

        self.domain[np.where(u_uk > 0.001)] = 0  # take away infection from domain
        # fig, ax = plt.subplots(figsize=(5, 6))
        fig, ax = plt.subplots()
        # im = ax.pcolormesh(((u_uk/u_uk.max()) - self.domain) + self.sea, cmap=self.cmap)
        # im = ax.pcolor(((u_uk/u_uk.max()) - self.domain) + self.sea, cmap=self.cmap)
        # plt.gca().invert_yaxis()
        u = u_uk/u_uk.max()
        im = ax.imshow((u - self.domain) + self.sea, cmap=self.cmap)
        if title is None:
            pass
        else:
            ax.set_title('t = {}'.format(title))

        plt.colorbar(im)
        ax.set_aspect("auto")
        if sim_plt:
            plt.savefig(self.save_dir + '/time_series/{}.pdf'.format(self.labeler(c)))
        else:
            if ext is None:
                plt.savefig(self.save_dir + '/{}'.format(self.labeler(c)))
            else:
                plt.savefig(self.save_dir + '/{}{}'.format(self.labeler(c), ext))
        if show:
            plt.show()
        elif not show:
            plt.close()
        return

