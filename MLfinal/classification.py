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
import keras.backend as K


# parameters
num_classes = 2
epochs = 3
isvalid = 0
train_size = 20000   #21764
label_dimension = 10
train_max_size = 1000
batch_size = 15
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
print(origin_pic.shape)
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
                row[i] = float(row[i])
        row[0] = row[0][5:10] 
        index.append(row[:6])
    csvfile.close()

i = 0
count = 0
zero = 0
temp = [0]*label_dimension
while(i<len(index) and index[i][0]!="20000"):
    if(index[i][5]==1):
        if(count==0):
            temp[0] = 1
            temp[1] = index[i][1]/1024
            temp[2] = index[i][2]/1024
            temp[3] = index[i][3]/1024
            temp[4] = index[i][4]/1024   
        
        if(count==1):
            temp[5] = 1
            temp[6] = index[i][1]/1024
            temp[7] = index[i][2]/1024
            temp[8] = index[i][3]/1024
            temp[9] = index[i][4]/1024
        
        count += 1

    if(index[i][0]!=index[i+1][0]):
        train_label.append(temp)
        temp = [0]*label_dimension
        count = 0
    i += 1

train_label = np.array(train_label)
train_label = np.reshape(train_label, (train_size, label_dimension))
print(train_label.shape)
#train_label = np.reshape(train_label, (train_size, width*height*1))
#------------------------------------------------------------------------

#change ratio
real_train_data = []
real_train_label = []
zero_count = 0
size = 0
for i in range(train_size):
    if(train_label[i][0]==0 and zero_count<train_size*0.1):
        #real_train_data.append(origin_pic[i])
        #real_train_label.append(train_label[i])
        zero_count += 1
        #size += 1
    elif(train_label[i][0]==1):
        real_train_data.append(origin_pic[i])
        real_train_label.append(train_label[i])
        size += 1

real_train_data = np.reshape(real_train_data, (size, 1024, 1024, 1))
real_train_label = np.reshape(real_train_label, (size, label_dimension))




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

model.add(Conv2D(128, (3, 3), padding='same'))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
#model.add(Dropout(0.4))


model.add(Flatten())


model.add(Dense(5))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
#model.add(Dropout(0.5))

model.add(Dense(label_dimension))
model.add(Activation('sigmoid'))
# finish ----------------------------------------


def iou_loss(y_true, y_pred, start):
    # iou loss for bounding box prediction
    #--- input must be as [x1, y1, x2, y2]    
    #[pc, x, y, width, height]

    # AOG = Area of Groundtruth box
    #---AoG = K.abs(K.transpose(y_true)[2] - K.transpose(y_true)[0] + 1) * K.abs(K.transpose(y_true)[3] - K.transpose(y_true)[1] + 1)
    AoG = K.transpose(y_true)[start+3] * K.transpose(y_true)[start+4]

    # AOP = Area of Predicted box
    #---AoP = K.abs(K.transpose(y_pred)[2] - K.transpose(y_pred)[0] + 1) * K.abs(K.transpose(y_pred)[3] - K.transpose(y_pred)[1] + 1)
    AoP = K.transpose(y_pred)[start+3] * K.transpose(y_pred)[start+4]

    # overlaps are the co-ordinates of intersection box
    overlap_0 = K.maximum(K.transpose(y_true)[start+1], K.transpose(y_pred)[start+1])
    overlap_1 = K.maximum(K.transpose(y_true)[start+2], K.transpose(y_pred)[start+2])
    overlap_2 = K.minimum(K.transpose(y_true)[start+1]+K.transpose(y_true)[start+3], K.transpose(y_pred)[start+1]+K.transpose(y_pred)[start+3])
    overlap_3 = K.minimum(K.transpose(y_true)[start+2]+K.transpose(y_true)[start+4], K.transpose(y_pred)[start+2]+K.transpose(y_true)[start+4])

    # intersection area
    intersection = (overlap_2 - overlap_0 + 1) * (overlap_3 - overlap_1 + 1)

    # area of union of both boxes
    union = AoG + AoP - intersection
    
    # iou calculation
    if(K.transpose(y_true)[start+0]==1):
        iou = intersection / union
        iou += K.square(K.transpose(y_true)[start+0]-K.transpose(y_pred)[start+0])
    else:
        iou = K.square(K.transpose(y_true)[start+0]-K.transpose(y_pred)[start+0])
    # bounding values of iou to (0,1)
    iou = K.clip(iou, 0.0 + K.epsilon(), 1.0 - K.epsilon())
    
    # loss for the iou value
    iou_loss = -K.log(iou)

    return iou_loss

def loss(y_true, y_pred):
    iou_total = iou_loss(y_true, y_pred, 0) + iou_loss(y_true, y_pred, 5)
    return iou_total


# compile the model
model.compile(loss=loss, optimizer='adam')

model.fit(real_train_data, real_train_label, epochs = epochs, batch_size = batch_size, validation_split=0.05)
#origin_pic
#train_label
print(model.summary())

# save the smodel
model.save('localization2.h5')
