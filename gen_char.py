#coding=utf-8
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import cv2;
import numpy as np;
import os;
from math import *


# font = ImageFont.truetype("Arial-Bold.ttf",14)

index = {"京": 0, "沪": 1, "津": 2, "渝": 3, "冀": 4, "晋": 5, "蒙": 6, "辽": 7, "吉": 8, "黑": 9, "苏": 10, "浙": 11, "皖": 12,
         "闽": 13, "赣": 14, "鲁": 15, "豫": 16, "鄂": 17, "湘": 18, "粤": 19, "桂": 20, "琼": 21, "川": 22, "贵": 23, "云": 24,
         "藏": 25, "陕": 26, "甘": 27, "青": 28, "宁": 29, "新": 30, "0": 31, "1": 32, "2": 33, "3": 34, "4": 35, "5": 36,
         "6": 37, "7": 38, "8": 39, "9": 40, "A": 41, "B": 42, "C": 43, "D": 44, "E": 45, "F": 46, "G": 47, "H": 48,
         "J": 49, "K": 50, "L": 51, "M": 52, "N": 53, "P": 54, "Q": 55, "R": 56, "S": 57, "T": 58, "U": 59, "V": 60,
         "W": 61, "X": 62, "Y": 63, "Z": 64};

chars = ["京", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "皖", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂",
             "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A",
             "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
             "Y", "Z"
             ];
def AddSmudginess(img, Smu):
    rows = r(Smu.shape[0] - 50)

    cols = r(Smu.shape[1] - 50)
    adder = Smu[rows:rows + 50, cols:cols + 50];
    adder = cv2.resize(adder, (50, 50));
    #   adder = cv2.bitwise_not(adder)
    img = cv2.resize(img,(50,50))
    img = cv2.bitwise_not(img)
    img = cv2.bitwise_and(adder, img)
    img = cv2.bitwise_not(img)
    return img
def tfactor(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV);

    hsv[:,:,0] = hsv[:,:,0]*(0.8+ np.random.random()*0.2);
    hsv[:,:,1] = hsv[:,:,1]*(0.3+ np.random.random()*0.7);
    hsv[:,:,2] = hsv[:,:,2]*(0.2+ np.random.random()*0.8);

    img = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR);
    return img
def GenCh(f,val):
    img=Image.new("RGB", (45,70),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 3),val,(0,0,0),font=f)
    img =  img.resize((23,70))
    A = np.array(img)
    return A
def GenCh1(f,val):
    img=Image.new("RGB", (23,60),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 2),val.decode('utf-8'),(0,0,0),font=f)
    A = np.array(img)
    return A
def AddGauss(img, level):
    return cv2.blur(img, (level * 2 + 1, level * 2 + 1));
def r(val):
    return int(np.random.random() * val)
def AddNoiseSingleChannel(single):
    diff = 255-single.max();
    noise = np.random.normal(0,1+r(5),single.shape);
    noise = (noise - noise.min())/(noise.max()-noise.min())
    noise= diff*noise;
    noise= noise.astype(np.uint8)
    dst = single + noise
    return dst

def addNoise(img,sdev = 0.5,avg=10):
    img[:,:,0] =  AddNoiseSingleChannel(img[:,:,0]);
    img[:,:,1] =  AddNoiseSingleChannel(img[:,:,1]);
    img[:,:,2] =  AddNoiseSingleChannel(img[:,:,2]);
    return img;


class GenChar:

    def __init__(self,fontCh,fontEng):
        self.fontC =  ImageFont.truetype(fontCh,43,0);
        self.fontE =  ImageFont.truetype(fontEng,60,0);
        self.img=np.array(Image.new("RGB", (35,60),(255,255,255)))
        self.bg  = cv2.resize(cv2.imread("./images/char_tmp.jpg"),(35,60));
        self.smu = cv2.imread("./images/smu2.jpg");
    def draw(self,val):
        offset= 6 ;
        self.img[0:70, offset:offset+23] = GenCh1(self.fontE, val[0])
        return self.img
    def generate(self,text):
        if len(text) == 1:
            print text.decode(encoding = "utf-8")
            fg = self.draw(text.decode(encoding="utf-8"));
            fg = cv2.bitwise_not(fg);
            com = cv2.bitwise_or(fg,self.bg);
            com = AddSmudginess(com,self.smu)
            com = tfactor(com)
            com = AddGauss(com, 1+r(4));
            #com = addNoise(com);
            return com
    def genPlateString(self,pos,val):
        plateStr = "";
        box = [0];
        for unit,cpos in zip(box,xrange(len(box))):
            plateStr += chars[31+r(34)]
        return plateStr;
    def genBatch(self, batchSize,pos,charRange, outputPath,size):
        if (not os.path.exists(outputPath)):
            os.mkdir(outputPath)
        for i in xrange(batchSize):
                plateStr = G.genPlateString(-1,-1)
                img =  G.generate(plateStr);
                cv2.imshow("img", img)
                img = cv2.resize(img,size);
                cv2.waitKey(0);
                cv2.imwrite(outputPath + "/" + str(i).zfill(2) + ".jpg", img);
G = GenChar("./font/platech.ttf",'./font/platechar.ttf')
G.genBatch(1,2,range(31,65),"./plate",(30,70))

