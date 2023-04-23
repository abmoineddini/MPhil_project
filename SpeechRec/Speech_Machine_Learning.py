import cv2
import os
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import tensorflow
from tensorflow import keras
from keras import Sequential, regularizers
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout, Softmax
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report,confusion_matrix
from keras.utils.vis_utils import plot_model
from datetime import datetime
from packaging import version
import tensorflow as tf
import pandas as pd

def get_data(data_dir, img_size, labels):
    data = []
    for label in labels:
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img))[...,::-1] #convert BGR to RGB format
                resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)

def find_labels(DataSetName):
    path_dir = "TrainingData/Spatial_Recognition/"+ DataSetName+"/DataBase/training/"
    print(path_dir)
    labels = os.listdir(path_dir)
    print(labels)
    labelsInt = []
    for i in labels:
        labelsInt.append(int(i))
    labelsInt.sort()
    labels = []
    for i in labelsInt:
        labels.append(str(i))
    return labels


def Start_CNN_Training(self, DataSetName):
    path_dir = "TrainingData/Spatial_Recognition/"+ DataSetName
    figure_path = path_dir +"/Figures/"
    logs_path = path_dir + "/Logs/"
    folderTraining = path_dir+"/DataBase/training/"
    folderTesting = path_dir+"/DataBase/Validation/"
    ep = 150
    LearningRate = 0.00005
    img_size = 150

    label = find_labels(DataSetName)
    CAT = label 
    print(CAT)
    trainData = get_data(folderTraining, img_size, labels=CAT)

    x_train = []
    y_train = []



    for feature, label in trainData:
      x_train.append(feature)
      y_train.append(label)

    # Normalize the data
    x_train = np.array(x_train) / 255

    x_train.reshape(-1, img_size, img_size, 1)
    y_train = np.array(y_train)

    testData = get_data(folderTesting, img_size, labels= CAT)
    x_val = []
    y_val = []

    for feature, label in testData:
        x_val.append(feature)
        y_val.append(label)

    x_val = np.array(x_val) / 255

    x_val.reshape(-1, img_size, img_size, 1)
    y_val = np.array(y_val)

    num_labels = len(CAT)
    datagen = ImageDataGenerator(
            featurewise_center=False,  # set input mean to 0 over the dataset
            samplewise_center=False,  # set each sample mean to 0
            featurewise_std_normalization=False,  # divide inputs by std of the dataset
            samplewise_std_normalization=False,  # divide each input by its std
            zca_whitening=False,  # apply ZCA whitening
            rotation_range = False,  # randomly rotate images in the range (degrees, 0 to 180)
            zoom_range = False,#0.3, # Randomly zoom image
            width_shift_range=False,#0.2,  # randomly shift images horizontally (fraction of total width)
            height_shift_range=False,  # randomly shift images vertically (fraction of total height)
            horizontal_flip = False,  # randomly flip images
            vertical_flip=False)  # randomly flip images


    datagen.fit(x_train)
    logdir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tensorflow.keras.callbacks.TensorBoard(log_dir=logdir)

    model = Sequential()
    model.add(Conv2D(35, 5, padding="same", activation="relu", input_shape=x_train.shape[1:]))
    model.add(MaxPool2D(pool_size=(2, 2), strides=3))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(65, 5, padding="same", activation="relu"))
    model.add(MaxPool2D())
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128, activation="sigmoid",
                    kernel_regularizer= regularizers.L1L2(l1=1e-5, l2=1e-4),
                    bias_regularizer= regularizers.L2(1e-4),
                    activity_regularizer= regularizers.L2(1e-5)))

    model.add(Dense(128, activation="relu",
                    kernel_regularizer= regularizers.L1L2(l1=1e-5, l2=1e-4),
                    bias_regularizer= regularizers.L2(1e-4),
                    activity_regularizer= regularizers.L2(1e-5)))

    model.add(Dropout(0.25))
    model.add(Dense(num_labels))


    model.summary()

    opt = Adam(lr=LearningRate)
    model.compile(optimizer = opt , loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True) , metrics = ['accuracy'])

    history = model.fit(x_train,y_train,epochs = ep , validation_data = (x_val, y_val), callbacks=[tensorboard_callback])

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(ep)

    fig = plt.figure(figsize=(15, 15))
    plt.subplot(2, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()
    Name = figure_path+"/AccurracyandErrorPlot.png"
    fig.savefig(Name, transparent=True, bbox_inches='tight')

    model.summary()
    model.save(path_dir+"/DirectionRecCNN")

    datasheet_name = logs_path+"AccuracyHistory.csv"
    if os.path.exists(datasheet_name):
        pass 
    else:
        pd.DataFrame({'Training Accurary (%)': 0, 
                        'Validation Accuracy (%)': 0, 
                        'Training Loss': 0, 
                        'Validation Loss': 0}, index=[0]).to_csv(datasheet_name,index=False)


    from csv import writer
    for i in range(len(acc)):
        FileAdd = [acc[i], val_acc[i], loss[i], val_loss[i]]
        with open(datasheet_name, 'a+', newline='') as f_object:
            # Pass the CSV  file object to the writer() function
            writer_object = writer(f_object)
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(FileAdd)
            # Close the file object
            f_object.close()
            FileAdd = []



    ## Start esting
    folderTesting = path_dir+"/DataBase/Testing/"
    img_size = 150
    testData = get_data(folderTesting, img_size, CAT)
    x_val = []
    y_val = []
    
    for feature, label in testData:
      x_val.append(feature)
      y_val.append(label)

    x_val = np.array(x_val) / 255

    x_val.reshape(-1, img_size, img_size, 1)
    y_val = np.array(y_val)
    label = CAT
    print(label)
    DegNum = label[1]
    DegNum = str(DegNum)
    predictions = model.predict(x_val)
    predictions = np.argmax(predictions,axis=1)
    print(classification_report(y_val, predictions, target_names = CAT))
    fig = plt.figure()
    confusion_mtx = tf.math.confusion_matrix(y_val, predictions)
    sns.heatmap(confusion_mtx, xticklabels=CAT, yticklabels=CAT,
                annot=True, fmt='g')
    plt.rc('font', family='Helvetica')
    plt.xlabel('Prediction',fontsize=20)
    plt.xticks(rotation=90)
    plt.ylabel('Label',fontsize=20)
    plt.yticks(rotation=90)
    plt.show()
    Name = figure_path + " Confusion Matrix.png"
    fig.savefig(Name, transparent=True, bbox_inches='tight')

    Test_datasheet_name = logs_path+"TestingValidationCNN.csv"
    if os.path.exists(Test_datasheet_name):
        pass 
    else:
        pd.DataFrame({'Actual label': 0, 
                        'prediction': 0}, index=[0]).to_csv(Test_datasheet_name,index=False)


    for i in range(len(y_val)):
        FileAdd = [y_val[i], predictions[i]]
        with open(Test_datasheet_name, 'a+', newline='') as f_object:
            # Pass the CSV  file object to the writer() function
            writer_object = writer(f_object)
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(FileAdd)
            # Close the file object
            f_object.close()
            FileAdd = []

def Save_CNN(model, Name):
    json_model = model.to_json()

    with open(Name, 'w') as json_file:
        json_file.write(json_model)


    