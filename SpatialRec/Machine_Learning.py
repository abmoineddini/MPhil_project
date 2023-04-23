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
# from keras.models import Sequential
# from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout
from keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import classification_report,confusion_matrix
from keras.utils.vis_utils import plot_model
from datetime import datetime
from packaging import version


import tensorflow as tf




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


def CNN_Training(folderTraining, folderTesting, ep, LearningRate, dataType, img_size, label):
    #img_size = 32
    CAT = label
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

    # model.add(Conv2D(64, 3, padding="same", activation="relu"))
    # model.add(MaxPool2D())

    #
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
    #model.add()
    model.add(Dropout(0.25))
    model.add(Dense(num_labels))
    # model.add(Softmax())

    # model = Sequential()
    # model.add(Conv2D(img_size, 3,padding="same", activation="relu", input_shape=x_train.shape[1:]))
    # model.add(MaxPool2D())
    #
    # # model.add(Conv2D(64, 3, padding="same", activation="relu"))
    # # model.add(MaxPool2D())
    # # model.add(Dropout(0.25))
    #
    # model.add(Conv2D(64, 3, padding="same", activation="relu"))
    # model.add(MaxPool2D())
    # model.add(Dropout(0.25))
    #
    # model.add(Flatten())
    # model.add(Dense(128,activation="relu"))
    # #model.add()
    # model.add(Dropout(0.5))
    # model.add(Dense(num_labels))

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
    Name = "Figures/" + dataType+"AccurracyandErrorPlot.png"
    fig.savefig(Name, transparent=True, bbox_inches='tight')

    model.summary()

    #plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

    return model, acc, val_acc, loss, val_loss

def TestingNetwrok(model, folderTesting, img_size, labels):
    testData = get_data(folderTesting, img_size, labels)
    x_val = []
    y_val = []

    for feature, label in testData:
      x_val.append(feature)
      y_val.append(label)

    x_val = np.array(x_val) / 255

    x_val.reshape(-1, img_size, img_size, 1)
    y_val = np.array(y_val)

    #CAT = ['A', 'B', 'C', 'D', 'E', 'F']
    CAT = labels
    DegNum = int(labels[1])
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
    Name = "Figures/" + DegNum + " Confusion Matrix.png"
    fig.savefig(Name, transparent=True, bbox_inches='tight')
    return y_val, predictions

def Save_CNN(model, Name):
    json_model = model.to_json()

    with open(Name, 'w') as json_file:
        json_file.write(json_model)

def CNN_TrainingImprove(folderTraining, folderTesting, ep, LearningRate, dataType, img_size, label):
    #img_size = 32
    CAT = label
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
    model.add(Conv2D(8, 20,padding="same", activation="relu", input_shape=x_train.shape[1:]))
    model.add(MaxPool2D())

    # model.add(Conv2D(64, 3, padding="same", activation="relu"))
    # model.add(MaxPool2D())


    # model.add(Conv2D(5, 30, padding="same", activation="relu"))
    # model.add(MaxPool2D())
    # model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128,activation="relu"))
    #model.add()
    model.add(Dropout(0.25))
    model.add(Dense(num_labels))
    model = tf.keras.models.load_model("DirectionRecCNN")
    model.summary()

    opt = Adam(lr=LearningRate, beta1=0.9, beta2=0.999, epsilon=1e-08,)
    model.compile(optimizer = opt , loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True) , metrics = ['accuracy'])

    history = model.fit(x_train, y_train, epochs = ep , validation_data = (x_val, y_val), callbacks=[tensorboard_callback])

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
    Name = dataType+"AccurracyandErrorPlot.png"
    fig.savefig(Name, transparent=True, bbox_inches='tight')

    model.summary()

    #plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

    return model, acc, val_acc, loss, val_loss