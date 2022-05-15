__author__ = 'ubuntu'

import cPickle as cp
import pickle
import numpy as np
from numpy import *

from PIL import Image
import io
import glob

from xyongle.CommonFileUtil import CommonFile


class CommonUtilImage:

    def converteImgedataToArray(self,imgData):

        data=[]
        filenames = []
        class_list = []

        try:
           r, g, b = imgData.split()
           reseqImage = list(r.getdata()) + list(g.getdata()) + list(b.getdata())
           data.append(reseqImage)
           # filenames.append(imagePath)
                # class_list.append(1)
        except:
           print 'error' + 1
        data_array = np.array(data, dtype = np.uint8)

        return data_array


    def readImgArray(self,imagePath):
        inputImage = Image.open(imagePath)
        (width,height) = inputImage.size
        print inputImage.size

        # data_array = self.converteImgedataToArray(inputImage)

        return inputImage

    def imgResizeFromImage(self,inputImage, dest_size):
        small_image = inputImage.resize((dest_size, dest_size),Image.ANTIALIAS)

        return small_image
        # data_array = self.converteImgedataToArray(small_image)
        #
        # return data_array

    def imgResizeFromPath(self,imagePath, dest_size):
        inputImage = self.readImgArray(imagePath)
        small_image = inputImage.resize((dest_size, dest_size),Image.ANTIALIAS)

        return small_image

    def imageshow(self,imgPath):
        im= Image.open(imgPath)
        print im
        im.show()

    def checkRGB(self,imagePathList):
        print 'check'
        curr_no =0;
        total_num = len(imagePathList)
        for name in imagePathList:
            curr_no += 1
            if curr_no%1000 == 0:
                print curr_no, total_num
            # im = Image.open(name)
            img_type = self.getImageChannle(name)
            # print img_type
            if 'RGB' != img_type:
                print name

    def getImageChannle(self, name):
        im = Image.open(name)
        return im.mode



if __name__ == '__main__':

    print 'test'
    imStr='/media/win8/xyongle/Images/flickr/test/10_6.jpg'
    imPath='/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/flickr/test/'

    imStr = '/media/ubuntu/My Passport/flickr-images'

    commonUtilImage = CommonUtilImage()
    commonFile = CommonFile
    fileNameList = commonFile.getFileList(imStr,'jpg')
    print len(fileNameList)
    print 'check start!!'
    commonUtilImage.checkRGB(fileNameList)

    print 'check out!!'

    # self.readImgArray(self,imStr,256)
    # im= Image.open(imStr)
    # print im
    # im.show()
    # print im.tile




