__author__ = 'ubuntu'

import tarfile
from StringIO import StringIO
from random import shuffle
import sys
from time import time
from pyext._MakeDataPyExt import resizeJPEG
import itertools
import os
import cPickle
import scipy.io
import math
import random

from xyongle.CommonFileUtil import CommonFile

##########################################################################
##
##  write by xyongle on 2015-10-30
##
###############################################################################
class  MakeData:

    CROP_TO_SQUARE          = True
    OUTPUT_IMAGE_SIZE       = 256
    # Number of threads to use for JPEG decompression and image resizing.
    NUM_WORKER_THREADS      = 8
    # Don't worry about these.
    OUTPUT_BATCH_SIZE = 1000
    OUTPUT_SUB_BATCH_SIZE = 1000

    def pickle(self,filename, data):
        with open(filename, "w") as fo:
            cPickle.dump(data, fo, protocol=cPickle.HIGHEST_PROTOCOL)

    def unpickle(self,filename):
        fo = open(filename, 'r')
        contents = cPickle.load(fo)
        fo.close()
        return contents

    def partition_list(self,l, partition_size):
        divup = lambda a,b: (a + b - 1) / b
        return [l[i*partition_size:(i+1)*partition_size] for i in xrange(divup(len(l),partition_size))]

    def open_tar(self,path, name):
        if not os.path.exists(path):
            print " %s not found at %s. Make sure to set SRC_DIR correctly at the top of this file (%s)." % (name, path, sys.argv[0])
            sys.exit(1)
        return tarfile.open(path)

    def makedir(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def parse_devkit_meta(self,ILSVRC_DEVKIT_TAR):
        tf = self.open_tar(ILSVRC_DEVKIT_TAR, 'devkit tar')
        fmeta = tf.extractfile(tf.getmember('data/meta.mat'))
        meta_mat = scipy.io.loadmat(StringIO(fmeta.read()))
        labels_dic = dict((m[0][1][0], m[0][0][0][0]-1) for m in meta_mat['synsets'] if m[0][0][0][0] >= 1 and m[0][0][0][0] <= 1000)
        label_names_dic = dict((m[0][1][0], m[0][2][0]) for m in meta_mat['synsets'] if m[0][0][0][0] >= 1 and m[0][0][0][0] <= 1000)
        label_names = [tup[1] for tup in sorted([(v,label_names_dic[k]) for k,v in labels_dic.items()], key=lambda x:x[0])]

        fval_ground_truth = tf.extractfile(tf.getmember('data/test_ground_truth.txt'))
        validation_ground_truth = [[int(line.strip()) - 1] for line in fval_ground_truth.readlines()]
        tf.close()
        return labels_dic, label_names, validation_ground_truth

    def getDataStr(self, full_names,tgt_size):

        tempOpenFiles = [open(jpeg) for jpeg in full_names]
        jpeg_strings = list(itertools.chain.from_iterable(resizeJPEG([jpeg.read() for jpeg in tempOpenFiles], self.OUTPUT_IMAGE_SIZE, self.NUM_WORKER_THREADS, self.CROP_TO_SQUARE)))
        return jpeg_strings

    def write_batches(self,out_size, target_dir, name, start_batch_num, labels, jpeg_files_names):
        # self.OUTPUT_BATCH_SIZE = len(labels) ######  do not partition
        # self.OUTPUT_SUB_BATCH_SIZE = len(labels)
        self.OUTPUT_IMAGE_SIZE = out_size

        jpeg_files_names = self.partition_list(jpeg_files_names, self.OUTPUT_BATCH_SIZE)
        labels = self.partition_list(labels, self.OUTPUT_BATCH_SIZE)
        self.makedir(target_dir)
        print "Writing %s batches..." % name

        target_file_name = []

        for i,(labels_batch, jpeg_file_batch) in enumerate(zip(labels, jpeg_files_names)):
            t = time()
            #jpeg_strings = list(itertools.chain.from_iterable(resizeJPEG([jpeg.read() for jpeg in jpeg_file_batch], OUTPUT_IMAGE_SIZE, NUM_WORKER_THREADS, CROP_TO_SQUARE)))
            tempOpenFiles = [open(jpeg) for jpeg in jpeg_file_batch]
            jpeg_strings = list(itertools.chain.from_iterable(resizeJPEG([jpeg.read() for jpeg in tempOpenFiles], self.OUTPUT_IMAGE_SIZE, self.NUM_WORKER_THREADS, self.CROP_TO_SQUARE)))
            batch_path = os.path.join(target_dir, 'data_batch_%d' % (start_batch_num + i))
            self.makedir(batch_path)
            print '============================================================================'
            print 'name_size=%d, filenames_size = %d'%(len(name),len(jpeg_file_batch))
            for j in xrange(0, len(labels_batch), self.OUTPUT_SUB_BATCH_SIZE):
                self.pickle(os.path.join(batch_path, 'data_batch_%d.%d' % (start_batch_num + i, j/self.OUTPUT_SUB_BATCH_SIZE)),
                       {'data': jpeg_strings[j:j+self.OUTPUT_SUB_BATCH_SIZE],
                        'labels': labels_batch[j:j+self.OUTPUT_SUB_BATCH_SIZE],
                        'inner_size':self.OUTPUT_IMAGE_SIZE*self.OUTPUT_IMAGE_SIZE*3,
                        'num_cases_per_batch': self.OUTPUT_BATCH_SIZE,
                        'filenames': jpeg_file_batch[j:j+self.OUTPUT_SUB_BATCH_SIZE],
                        'name':name})
            print "Wrote %s (%s batch %d of %d) (%.2f sec)" % (batch_path, name, i+1, len(jpeg_files_names), time() - t)

            target_file_name = batch_path #(batch_path, name, i+1, len(jpeg_files_names))

            ## close open file
            for m in tempOpenFiles:
                m.close()
        return i + 1,target_file_name


    def doMakeDataForFileNameList(self,fileNameList, data_img_label, out_size=256, tgt_dir=[], out_batch_size = 500, start_batch_num= 1000):
        listfile = fileNameList
        data_img_fullname = [m for m in listfile]
        # data_img_label = [[1] for m in listfile]
        self.OUTPUT_BATCH_SIZE = out_batch_size
        num,fileName = self.write_batches(out_size,tgt_dir, 'test', start_batch_num, data_img_label, data_img_fullname)
        return data_img_fullname

    def doMakeData(self,img_path, out_size=256, tgt_dir=[], out_batch_size = 500, start_batch_num= 1000):
        #
        if len(img_path) == 0:
            img_path = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/flickr/test'
        commonFile = CommonFile()
        listfile = commonFile.getFileList(img_path,FlagStr=['.jpg'])

        data_img_fullname = [m for m in listfile]
        data_img_label = [[1] for m in listfile]
        # makeData = MakeData()
        self.OUTPUT_BATCH_SIZE = out_batch_size
        num,fileName = self.write_batches(out_size,tgt_dir, 'test', start_batch_num, data_img_label, data_img_fullname)
        print tgt_dir
        return fileName

class NistData:
    ############################################################
    ##
    ##  txtPath: NIST image data and txt file path
    ##  testIndex: the index of testing data:[1-5], 1: probes1.txt, 2:probes2.txt and so on.
    ##  reutrn the traing, validation and testing data-set
 
class FlickrData:
    def getCorrectData(self, filename, flag = ''):
        data=CommonFile.readTxtFile(filename)

        if flag == '':
            return data

        rtn = []
        for m in data:
            if flag in m:#value[1]:
                rtn.insert(0,m)
        return rtn
    def getAllMakeData(self,fileList, flag):
        rtn = []
        for fileName in fileList:
            value = self.getCorrectData(fileName,flag)
            for v in value:
                rtn.insert(0,v)
        return rtn

    def getDataFromTxt(self,data_path, num = -1):

        commonFile = CommonFile()
        listfile = commonFile.getFileList(data_path,FlagStr=['.txt'])

        tattooFiles = []
        nontattooFiles = []
        for v in listfile:
            if 'predictions_batch_1' in v:
                tattooFiles.insert(0,v)
            elif 'predictions_batch_2' in v:
                nontattooFiles.insert(0,v)
            else:
                print 'file error!!!!!!!!!!!!!!!!!!!!'
                print 'error file names: %s' % (v)
                os._exit()

        tattooImgNames = self.getAllMakeData(tattooFiles, 'CORRECT')
        nontattooImgNames = self.getAllMakeData(nontattooFiles, 'CORRECT')

        ## the little of the two
        ## 1:1 add data
        if num == -1:
            num = len(tattooImgNames)

        if num > len(tattooImgNames):
            num = len(tattooImgNames)

        if num > len(nontattooImgNames):
            num = len(nontattooImgNames)

        ## the forest num for data
        ## tattoo is 0 and nontattoo is 1
        jpegLabelsDict = {}
        for ind in range(0, num):
            value = tattooImgNames[ind].split(' ')
            tattooImgNames[ind] = value[0]
            jpegLabelsDict[tattooImgNames[ind]] = 0

            value = nontattooImgNames[ind].split(' ')
            nontattooImgNames[ind] = value[0]
            jpegLabelsDict[nontattooImgNames[ind]] = 1
        imgNames = tattooImgNames[0:num] + nontattooImgNames[0:num]

        return imgNames,jpegLabelsDict
if __name__ == "__main__":

    img_path = '/media/win8/xyongle/Flickr/flickr_classfiy_results'
        #
        # commonFile = CommonFile()
        # listfile = commonFile.getFileList(img_path,FlagStr=['.txt'])
        # # listfile = commonFile.
        # for m in listfile:print m
        # data_img_fullname = [m for m in listfile]
        # data_img_label = [[1] for m in listfile]
        # tgt_dir =''
        # print data_img_label
        # write_batches(self,tgt_dir, 'vali', 1000, data_img_label, data_img_fullname)
    # nist = NISTMakeData()
    # nist.getNameListFormNistFold()
