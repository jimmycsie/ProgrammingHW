import csv
import numpy as np
from skimage import data, io
from keras.models import load_model
import keras.backend as K
import keras.losses


# loss funciton-------------------------------------------------------------------------
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
keras.losses.custom_loss = loss
# -------------------------------------------------------------------------------------


ans_path = 'prediction.csv'
model = load_model("localization2.h5")
#print(model.summary())
image_path = "test/test"
test_size = 10#4998
label_dimension = 10
width = 1024
height = 1024

origin_pic = []
number = []
for i in range(10):
    number.append("000"+str(i))
for i in range(10, 100):
    number.append("00"+str(i))
for i in range(100, 1000):
    number.append("0"+str(i))
for i in range(1000, test_size):
    number.append(str(i))


# get original picture
for i in range(test_size):
    name = image_path + number[i] + '.png'
    temp = io.imread(name)
    if(temp.ndim==2):
        origin_pic.append(temp)
    else:
        temp = temp.transpose(2,0,1)[0]
        temp = np.reshape(temp,(width, height))
        origin_pic.append(temp)
    if(i%1000==0):
        print(i)


origin_pic = np.array(origin_pic)
origin_pic = np.reshape(origin_pic, (test_size, width, height, 1))
print(origin_pic.shape)

predict = model.predict(origin_pic)
predict = np.reshape(predict, (test_size, label_dimension))
predict = np.round(predict*1024).astype(int).clip(0, 1024)
print(predict.shape)
for i in range(10):
    print(predict[i][0], end=" ")

"""
# for auto-encoder
predict = np.round(predict).clip(0,255).astype(np.uint8)
print(predict.shape)
for i in range(test_size):
    io.imsave("./reduction/"+str(i)+".jpg", predict[i])
"""

"""
ans = []
neg = 0
pos = 0
for i in range(test_size):
    if(predict[i][0]>=0.5):
        ans.append(0)
        neg += 1
    elif(predict[i][1]>=0.5):
        ans.append(1)
        pos += 1
print(neg, pos)

"""
zero = 0
with open(ans_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["patientId", "x", "y", "width", "height","Target"])
    for i in range(test_size):
        if(predict[i][0]>512):
            if(predict[i][1]+predict[i][3]<1024 and predict[i][2]+predict[i][4]<1024):
                writer.writerow(["test"+number[i]+".png", predict[i][1], predict[i][2], predict[i][3], predict[i][4], 1])
            else:
                writer.writerow(["test"+number[i]+".png", predict[i][1], predict[i][2], 1000-predict[i][1], 1000-predict[i][2], 1])
        
        if(predict[i][5]>512):
            if(predict[i][6]+predict[i][8]<1024 and predict[i][7]+predict[i][9]<1024):
                writer.writerow(["test"+number[i]+".png", predict[i][6], predict[i][7], predict[i][8], predict[i][9], 1])
            else:
                writer.writerow(["test"+number[i]+".png", predict[i][6], predict[i][7], 1000-predict[i][6], 1000-predict[i][7], 1])
        
        if(predict[i][0]<=512):     #and predict[i][5]<=512
            writer.writerow(["test"+number[i]+".png", '', '', '', '', 0])
            zero += 1
print("zero", zero)