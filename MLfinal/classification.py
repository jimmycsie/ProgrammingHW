from skimage import data, io
import csv
import numpy as np
import sys
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dropout, LeakyReLU, UpSampling2D
from keras.layers import BatchNormalization
from keras.optimizers import Adam
from keras import losses, regularizers

# parameters
num_classes = 2
epochs = 5
isvalid = 0
train_size = 10000   #21764
train_max_size = 1000
batch_size = 10
width = 1024
height = 1024

origin_pic = []
train_label = []
image_path = "train/"
label_path = "train_labels.csv"

number = []
for i in range(10):
    number.append("0000"+str(i))
for i in range(10, 100):
    number.append("000"+str(i))
for i in range(100, 1000):
    number.append("00"+str(i))
for i in range(1000, 10000):
    number.append("0"+str(i))
for i in range(10000, train_size):
    number.append(str(i))

# get original picture
for i in range(train_size):
    name = image_path + "train" + number[i] + '.png'
    temp = io.imread(name)
    origin_pic.append(temp)
    if(i%1000==0):
        print(i)

origin_pic = np.array(origin_pic)
origin_pic = np.reshape(origin_pic, (train_size, width, height, 1))
# normalize
#origin_pic -= np.sum(origin_pic, axis=0) / train_size
#origin_pic /= ( np.sqrt(np.sum(np.square(origin_pic), axis=0)/train_size ) )


# get training label
index = []
train_label = []
with open(file = label_path, mode = 'r') as csvfile:
    rows = csv.reader(csvfile)
    count = 0
    for row in rows:  
        if(count == 0):
            count = 1
            continue
        for i in range(1, len(row)):
            if(row[i]!=''):
                row[i] = int(float(row[i]))
        row[0] = row[0][5:10] 
        index.append(row[:6])
    csvfile.close()

i = 0
zero = 0
#temp = np.zeros((height, width), dtype=int)
while(i<len(index) and index[i][0]!="10000"):
    #if(index[i][5]==1): 
    #    for j in range(index[i][2], index[i][2]+index[i][4]):
    #        temp[j][index[i][1]:index[i][1]+index[i][3]] = 256
    if(index[i][0]!=index[i+1][0]):
        temp = np.zeros((2), dtype=int)
        if(index[i][5] == 0):
            temp[0] = 1
            zero+=1
        else:
            temp[1] = 1
        train_label.append(temp)
        #temp = np.zeros((height, width), dtype=int)
    i += 1

print("zero", zero)
train_label = np.array(train_label)
train_label = np.reshape(train_label, (train_size, num_classes))
print(train_label.shape)
print(train_label[:10])
#train_label = np.reshape(train_label, (train_size, width*height*1))
#------------------------------------------------------------------------


# Construct the model
model = Sequential()

model.add(Conv2D(32, (3, 3), padding='same', input_shape=(1024,1024,1) ))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
#model.add(Dropout(0.2))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
#model.add(Dropout(0.25))


model.add(Conv2D(128, (3, 3), padding='same'))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
#model.add(Dropout(0.3))

model.add(Conv2D(256, (3, 3), padding='same'))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
#model.add(Dropout(0.4))


model.add(Flatten())

model.add(Dense(8))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
#model.add(Dropout(0.5))

model.add(Dense(num_classes))
model.add(Activation('softmax'))
# finish ----------------------------------------

# compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(origin_pic, train_label, epochs = epochs, batch_size = batch_size, validation_split=0.1)

print(model.summary())

# save the smodel
model.save('auto_encoder.h5')
