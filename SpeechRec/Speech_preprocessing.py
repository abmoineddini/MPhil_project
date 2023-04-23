import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
# from SectionCutting import *
from os import listdir
from PIL import Image
import os
from os.path import isdir
from scipy.fft import fft, fftfreq
import random
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
    print("z1 is {}".format(z1))
    Nullpeaks = []

    count = 0
    for i in f:
        if round(i) == Fs/2-50:
            #print(count)
            minFreq = count
            break
        count = count + 1

    # print(f[minFreq])
    try:
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
    except:
        pass

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


def ProcessIm(Im1, Im2, fileName):
    image1 = Image.open(Im1)
    image1 = image1.rotate(90)

    image2 = Image.open(Im2)
    image1_size = image1.size
    new_image = Image.new('RGB', (2 * image1_size[0], image1_size[1]), (250, 250, 250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.save(fileName)

def ProcessConcat(Im1, Im2, Im3, Im4, fileName):
    image1 = Image.open(Im1)
    image2 = Image.open(Im2)
    image3 = Image.open(Im3)
    image4 = Image.open(Im4)

    image1_size = image1.size

    new_image = Image.new('RGB', (2 * image1_size[0], 2*image1_size[1]), (250, 250, 250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.paste(image3, (0, image1_size[1]))
    new_image.paste(image4, (image1_size[0], image1_size[1]))
    new_image.save(fileName)

def ProcessConcatAuto(Im, fileName):
    image1 = Image.open("Temp/"+Im[0])
    ChannelCount = 1
    if len(Im) > 1:
        image2 = Image.open("Temp/"+Im[1])
        ChannelCount = 2
        if len(Im) > 2:
            image3 = Image.open("Temp/"+Im[2])
            ChannelCount = 3
            if len(Im) > 3:
                image4 = Image.open("Temp/"+Im[3])
                ChannelCount = 4
                if len(Im) > 4:
                    image5 = Image.open("Temp/"+Im[4])
                    ChannelCount = 5
                    if len(Im) > 5:
                        image6 = Image.open("Temp/"+Im[5])
                        ChannelCount = 6
                        if len(Im) > 6:
                            image7 = Image.open("Temp/"+Im[6])
                            ChannelCount = 7
                            if len(Im) > 7:
                                image8 = Image.open("Temp/"+Im[7])
                                ChannelCount = 8
                                if len(Im) > 8:
                                    image9 = Image.open("Temp/" + Im[8])
                                    ChannelCount = 9

    image1_size = image1.size
    BlackImage = np.zeros([image1_size[1], image1_size[0], 3] ,dtype=np.uint8)
    BlackImage = Image.fromarray(BlackImage)

    if ChannelCount == 1:
        new_image = Image.new('RGB', (image1_size[0], image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.save(fileName)

    if ChannelCount == 2:
        new_image = Image.new('RGB', (2 * image1_size[0], 2*image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(BlackImage, (image1_size[0], 0))
        new_image.paste(image2, (image1_size[0], image1_size[1]))
        new_image.paste(BlackImage, (0, image1_size[1]))
        new_image.save(fileName)

    if ChannelCount == 3:
        new_image = Image.new('RGB', (2 * image1_size[0], 2*image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.paste(image3, (0, image1_size[1]))
        new_image.save(fileName)

    if ChannelCount == 4:
        new_image = Image.new('RGB', (2 * image1_size[0], 2*image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.paste(image3, (0, image1_size[1]))
        new_image.paste(image4, (image1_size[0], image1_size[1]))
        new_image.save(fileName)

    if ChannelCount == 5:
        new_image = Image.new('RGB', (3 * image1_size[0], 2*image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.paste(image3, (0, image1_size[1]))
        new_image.paste(image4, (image1_size[0], image1_size[1]))
        new_image.paste(image5, (2*image1_size[0], 0))
        new_image.save(fileName)

    if ChannelCount == 6:
        new_image = Image.new('RGB', (3 * image1_size[0], 2*image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.paste(image3, (0, image1_size[1]))
        new_image.paste(image4, (image1_size[0], image1_size[1]))
        new_image.paste(image5, (2*image1_size[0], 0))
        new_image.paste(image6, (2*image1_size[0], image1_size[1]))
        new_image.save(fileName)

    if ChannelCount == 7:
        new_image = Image.new('RGB', (4 * image1_size[0], 3*image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.paste(image3, (0, image1_size[1]))
        new_image.paste(image4, (image1_size[0], image1_size[1]))
        new_image.paste(image5, (2*image1_size[0], 0))
        new_image.paste(image6, (2*image1_size[0], image1_size[1]))
        new_image.paste(image7, (0, 2*image1_size[0]))
        new_image.save(fileName)

    if ChannelCount == 9:
        new_image = Image.new('RGB', (3 * image1_size[0], 3 * image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.paste(image3, (0, image1_size[1]))
        new_image.paste(image4, (image1_size[0], image1_size[1]))
        new_image.paste(image5, (2*image1_size[0], 0))
        new_image.paste(image6, (2*image1_size[0], image1_size[1]))
        new_image.paste(image7, (0, 2*image1_size[0]))
        new_image.paste(image8, (image1_size[0], 2*image1_size[1]))
        new_image.paste(image9, (2 * image1_size[0], 2 * image1_size[1]))
        new_image.save(fileName)

    if ChannelCount == 9:
        new_image = Image.new('RGB', (3 * image1_size[0], 3*image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.paste(image3, (0, image1_size[1]))
        new_image.paste(image4, (image1_size[0], image1_size[1]))
        new_image.paste(image5, (2*image1_size[0], 0))
        new_image.paste(image6, (2*image1_size[0], image1_size[1]))
        new_image.paste(image7, (0, 2*image1_size[1]))
        new_image.paste(image8, (image1_size[0], 2*image1_size[1]))
        new_image.paste(image9, (2 * image1_size[0], 2 * image1_size[1]))
        new_image.save(fileName)


def Start_spatial_preprocessing(self, DataSetName):


    path_dir = "TrainingData/Spatial_Recognition/"+DataSetName

    Raw_data_dir = path_dir+"/RawData/"


    for dataFileName in os.listdir(Raw_data_dir):
        FolderSTFTTraining = path_dir+"/DataBase/training/" + str(dataFileName.split("-")[0]) 
        FolderSTFTTesting = path_dir+"/DataBase/Testing/" + str(dataFileName.split("-")[0])
        FolderValTesting = path_dir+"/DataBase/Validation/" + str(dataFileName.split("-")[0])

        if isdir(FolderSTFTTraining):
            print("Folders Already Excits!")
        else:
            os.mkdir(FolderSTFTTraining)
            os.mkdir(FolderSTFTTesting)
            os.mkdir(FolderValTesting) 
        
        TrainingDirectory = [f for f in listdir(FolderSTFTTraining)]
        TestDirectory = [f for f in listdir(FolderSTFTTesting)]
        ValidationDirectory = [f for f in listdir(FolderValTesting)]
        
        countTrain = int(len(TrainingDirectory))
        countTest = int(len(TestDirectory))
        countVal = int(len(ValidationDirectory))

        df = pd.read_csv(Raw_data_dir+dataFileName)
        data = df.to_numpy()

        data = np.delete(data, 0, 1)
        ChannelNum = len(data[0]) - 1
        print(ChannelNum)

        

        time = data[200:len(data) - 1, 0]

        time_period = time[5]-time[4]
        Fs = 1/time_period

        row = len(time)
        print(row)
        col = len(data[0]) - 1
        print(col)

        normData = np.empty(shape=(row, col))

        for ch in range(ChannelNum):
            Detrend = sig.detrend(data[200:len(data) - 1, ch + 1])
            # plt.plot(time, Detrend)
            # plt.ylabel('some numbers')
            # plt.show()
            filter = sig.butter(2, [10, Fs/2-50], 'bandpass', fs=Fs, output='sos')
            corrdet = sig.sosfilt(filter, Detrend)
            corrdet = (corrdet * 5) / 1023

            maxVal = max(corrdet)
            normData[:, ch] = corrdet #/ maxVal

        Num = random.randint(0, 10)
        seperationPoints = SepWithSTFTAuto(normData, time, Fs)


        print(seperationPoints)
        if len(seperationPoints)>1 and len(seperationPoints)<=5:
            for ch in range(ChannelNum):
                if len(seperationPoints) <= 2:
                    Ch1pp = normData[int(seperationPoints[0]):int(seperationPoints[0]+Fs+10), ch]

                if len(seperationPoints) > 2:
                    Ch1pp = normData[int(seperationPoints[1]):int(seperationPoints[1]+Fs+10), ch]

        ##################################################### STFT Plots##################################################

                f1, t1, Zxx1 = sig.stft(Ch1pp, Fs, nperseg=75)
                fig1 = plt.figure(frameon=False)
                ax1 = plt.Axes(fig1, [0., 0., 1., 1.])
                plt.pcolormesh(t1, f1, np.abs(Zxx1), shading='gouraud', cmap='gray')
                plt.axis('off')
                plt.ylim([70, 500])
                ax1.set_axis_off()
                plt.tight_layout()
                # plt.show()
                Figname = 'Temp/STFTTestingFigure'+ str(ch) + '.png'
                fig1.savefig(Figname, bbox_inches='tight', pad_inches=0)


            if Num in range(0, 7):
                nameTrain = str(countTrain)
                countTrain += 1
                FileName = FolderSTFTTraining + "/" + nameTrain + '.png'
                Figures = os.listdir("Temp/")
                print(FileName)
                print(Figures)
                ProcessConcatAuto(Figures, FileName)

                # ProcessConcat('Temp/Ch1fft.png', 'Temp/Ch2fft.png','Temp/Ch3fft.png', 'Temp/Ch4fft.png', FileName)

            if Num in range(7, 9):
                nameVal = str(countVal)
                countVal += 1
                FileName = FolderValTesting + "/" + nameVal + '.png'
                Figures = os.listdir("Temp/")
                print(FileName)
                print(Figures)
                ProcessConcatAuto(Figures, FileName)


            if Num in range(9, 11):
                nameTest = str(countTest)
                countTest += 1
                FileName = FolderSTFTTesting + "/" + nameTest + '.png'
                Figures = os.listdir("Temp/")
                print(FileName)
                print(Figures)
                ProcessConcatAuto(Figures, FileName)

            for i in Figures:
                FigureName = "Temp/"+i
                os.remove(FigureName)
        
        else:
            for ch in range(ChannelNum):
                    
                Ch1pp = normData[:, ch]

        ##################################################### STFT Plots##################################################

                f1, t1, Zxx1 = sig.stft(Ch1pp, Fs, nperseg=75)
                fig1 = plt.figure(frameon=False)
                ax1 = plt.Axes(fig1, [0., 0., 1., 1.])
                plt.pcolormesh(t1, f1, np.abs(Zxx1), shading='gouraud', cmap='gray')
                plt.axis('off')
                plt.ylim([70, 500])
                ax1.set_axis_off()
                plt.tight_layout()
                # plt.show()
                Figname = 'Temp/STFTTestingFigure'+ str(ch) + '.png'
                fig1.savefig(Figname, bbox_inches='tight', pad_inches=0)


            if Num in range(0, 7):
                nameTrain = str(countTrain)
                countTrain += 1
                FileName = FolderSTFTTraining + "/" + nameTrain + '.png'
                Figures = os.listdir("Temp/")
                print(FileName)
                print(Figures)
                ProcessConcatAuto(Figures, FileName)

                # ProcessConcat('Temp/Ch1fft.png', 'Temp/Ch2fft.png','Temp/Ch3fft.png', 'Temp/Ch4fft.png', FileName)

            if Num in range(7, 9):
                nameVal = str(countVal)
                countVal += 1
                FileName = FolderValTesting + "/" + nameVal + '.png'
                Figures = os.listdir("Temp/")
                print(FileName)
                print(Figures)
                ProcessConcatAuto(Figures, FileName)


            if Num in range(9, 11):
                nameTest = str(countTest)
                countTest += 1
                FileName = FolderSTFTTesting + "/" + nameTest + '.png'
                Figures = os.listdir("Temp/")
                print(FileName)
                print(Figures)
                ProcessConcatAuto(Figures, FileName)

            for i in Figures:
                FigureName = "Temp/"+i
                os.remove(FigureName)


def PreprocessingMeth2(data, FolderSTFTTraining, FolderSTFTTesting, dataFileName):
    time = data[0:len(data)-4000, 1]
    voltage = data[0:len(data)-4000, 2]
    Fs = 4000

    TrainingDirectory = [f for f in listdir(FolderSTFTTraining)]
    TestDirectory = [f for f in listdir(FolderSTFTTesting)]
    detenV = sig.detrend(voltage)

    filter = sig.butter(2, [95, 1500], 'bandpass', fs=4000, output='sos')
    corrVoltage = sig.sosfilt(filter, detenV)
    corrVoltage = (corrVoltage*5)/1023

    maxV = max(corrVoltage)
    normV = corrVoltage/maxV

    countTrain = int(len(TrainingDirectory))
    countTest = int(len(TestDirectory))

    fig0 = plt.figure()
    ax0 = plt.Axes(fig0, [0., 0., 1., 1.])
    plt.style.use('dark_background')
    plt.scatter(time, normV, c=abs(normV * normV), s=abs(normV))
    plt.gray()
    plt.axis('off')
    ax0.set_axis_off()
    plt.tight_layout()
    plt.show()
    fig0.savefig('ScattTestingFigure.png', bbox_inches='tight', pad_inches=0)

    f1, t1, Zxx1 = sig.stft(normV, Fs, nperseg=1000)
    fig1 = plt.figure(frameon=False)
    ax1 = plt.Axes(fig1, [0., 0., 1., 1.])
    plt.pcolormesh(t1, f1, np.abs(Zxx1), shading='gouraud', cmap='gray')
    plt.axis('off')
    plt.ylim([90, 500])
    ax1.set_axis_off()
    plt.tight_layout()
    plt.show()
    fig1.savefig('STFTTestingFigure.png', bbox_inches='tight', pad_inches=0)

    Training = [1, 3, 4]

    from PIL import Image
    def ProcessIm(Im1, Im2, fileName):
        image1 = Image.open(Im1)
        image1 = image1.rotate(90)

        image2 = Image.open(Im2)
        image1_size = image1.size
        new_image = Image.new('RGB', (2 * image1_size[0], image1_size[1]), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1_size[0], 0))
        new_image.save(fileName)


    i = randint(1, 4)
    if i in Training:
        nameTrain = str(countTrain)
        countTrain += 1
        FileName = FolderSTFTTraining + "/" + nameTrain + '.png'
        print(FileName)
        ProcessIm('STFTTestingFigure.png', 'ScattTestingFigure.png', FileName)

    else:
        nameTest = str(countTest)
        countTest += 1
        FileName = FolderSTFTTesting + "/" + nameTest + '.png'
        print(FileName)
        ProcessIm('STFTTestingFigure.png', 'ScattTestingFigure.png', FileName)

    os.remove("STFTTestingFigure.png")
    os.remove("ScattTestingFigure.png")