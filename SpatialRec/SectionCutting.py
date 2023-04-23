import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.signal as sig
from random import randint

def SepWithSTFTAuto(data, time, Fs):
    inst = 100
    normV1 = data[0:len(time), 0]
    f, t, Zxx = sig.stft(normV1, Fs, nperseg=inst)
    fig = plt.figure(frameon=False)
    ax1 = plt.Axes(fig, [0., 0., 1., 1.])
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
    ax1.set_axis_off()
    plt.tight_layout()
    # plt.show()

    z1 = abs(Zxx)

    count = 0
    for i in f:
        if round(i) == 80:
            #print(count)
            minFreq = count
            continue
        count = count + 1

    # print(f[minFreq])

    z = z1[minFreq]
    # print(z)


    upperLim = max(z) * 0.50
    Nullpeaks, _ = sig.find_peaks(z, height=upperLim)
    plt.plot(t, z)
    plt.scatter(t[Nullpeaks], z[Nullpeaks])
    # plt.show()

    def truncate(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    plt.plot(time, normV1, label="Channel 1", linewidth=0.5, alpha=0.3)
    plt.scatter(t[Nullpeaks], z[Nullpeaks], color='k')
    # plt.show()
    print(Nullpeaks)

    if len(Nullpeaks) >1:
        adjPe = int(inst / 2)

        Sectioning = Nullpeaks*adjPe
        f, t, Zxx = sig.stft(normV1[Nullpeaks[0] * adjPe: Nullpeaks[1] * adjPe], Fs, nperseg=inst)
        fig1 = plt.figure(frameon=False)
        ax1 = plt.Axes(fig1, [0., 0., 1., 1.])
        plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
        ax1.set_axis_off()
        plt.tight_layout()
        # plt.show()

    else:
        Sectioning = [0]
    return Sectioning
