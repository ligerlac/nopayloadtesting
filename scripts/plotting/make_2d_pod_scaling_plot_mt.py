import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys, json, glob
from datetime import datetime, timedelta
from nopayloadtesting.plotter import Plotter, MTPlotter
from matplotlib import cm
from matplotlib.ticker import LinearLocator


def main(args):

    plotters = []
    for f in glob.glob(f'{args.folder}/*'):
        nginx_pods, django_pods = [int(i) for i in f.split('/')[-1].split('_')]
        p = MTPlotter(folder=f)
        p.nginx_pods = nginx_pods
        p.django_pods = django_pods
        print(f'f = {f}')
        plotters.append(p)

    Z = np.zeros((5, 5))
    print(Z)
    print(Z[0][0])

    for p in plotters:
        Z[p.nginx_pods-1][p.django_pods-1] = p.mean_freq

    X = np.arange(1, 6)
    Y = np.arange(1, 6)
    X, Y = np.meshgrid(X, Y)

    print(f'X = {X}')
    print(f'Y = {X}')
    print(f'Z = {X}')

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})


    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    #ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.1f}')
    ax.set_title("'moderate' scenario, 10 threads, 10 calls")
    ax.set_zlabel('mean response frequency [Hz]')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.xlabel('django pods')
    plt.ylabel('nginx pods')
    plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='output/latest', help='folder with test evaluation data')
    args = parser.parse_args()
    main(args)
