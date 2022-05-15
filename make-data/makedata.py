__author__ = 'ubuntu'

import sys
import os

curr_path = os.path.split(os.path.realpath(__file__))[0]
parent_path = curr_path[0:len(curr_path)-10]
print parent_path
sys.path.append(curr_path)
sys.path.append(parent_path)
sys.path.append(os.path.join(parent_path,'xyongle'))

from CommonMakeData import MakeData, NistData, FlickrData
from xyongle.CommonFileUtil import CommonFile

from convnet import ConvNet
from python_util.options import *
import numpy as np
import random

class xyongleError(Exception):
    pass
class xMakeData:

    def doMakeData(self,fileNames,imgLabels,tgt_dir,out_size=256, out_batch_size=2000, out_sub_batch_size=1000, start_batch_num= 1000):

        makeData = MakeData()
        fileName = makeData.doMakeDataForFileNameList(fileNames, imgLabels, out_size, tgt_dir, out_batch_size, out_sub_batch_size, start_batch_num)
        return fileName
    ##############################################################################################################
    ##
    ## from the correct data file.txt read the file and then make data
    ##
    ##
    def exeFlickrTxt(self,op, type):
        data_path = op.options['data_path'].value
        target_path = op.options['target_path'].value
        out_size = op.options['out_size'].value
        start_batch_num = op.options['start_batch_num'].value
        out_batch_size = op.options['out_batch_size'].value

        # out_size = 256
        # out_batch_size = 2000

	root_path = '/mnt/ICB/data/Flickr'
        txt_path = os.path.join(root_path)
	img_path = os.path.join(root_path, 'images')
        commonFile = CommonFile()
	content1 = CommonFile.readTxtFile(os.path.join(root_path,type + '1.txt'))
	content2 = CommonFile.readTxtFile(os.path.join(root_path,type + '2.txt'))
	content3 = CommonFile.readTxtFile(os.path.join(root_path,type + '3.txt'))
	content4 = CommonFile.readTxtFile(os.path.join(root_path,type + '4.txt'))
	content5 = CommonFile.readTxtFile(os.path.join(root_path,type + '5.txt'))
	ground = CommonFile.readTxtFile(os.path.join(root_path,'ground_truth.txt'))
        ground_dict = {}
        for v in ground:
            temp = v.split('|')
            ground_dict[temp[1]]=temp[0]
	### group1
        target_path = os.path.join(root_path, type, 'batches1')	
        self.makeDataNIST_Flickr(content1, content2+content3+content4+content5, target_path, ground_dict, img_path, out_size, out_batch_size)
        target_path = os.path.join(root_path, type, 'batches2')	
        self.makeDataNIST_Flickr(content2, content1+content3+content4+content5, target_path, ground_dict, img_path, out_size, out_batch_size)
        target_path = os.path.join(root_path, type, 'batches3')	
        self.makeDataNIST_Flickr(content3, content1+content2+content4+content5, target_path, ground_dict, img_path, out_size, out_batch_size)
        target_path = os.path.join(root_path, type, 'batches4')	
        self.makeDataNIST_Flickr(content4, content1+content2+content3+content5, target_path, ground_dict, img_path, out_size, out_batch_size)
        target_path = os.path.join(root_path, type, 'batches5')	
        self.makeDataNIST_Flickr(content5, content1+content2+content3+content4, target_path, ground_dict, img_path, out_size, out_batch_size)

    
    

    @classmethod
    def get_options_parser(cls):
        op = OptionsParser()

        op.add_option("data-path", "data_path", StringOptionParser, "xyongle data-path for processing: --data-path", default="")
        op.add_option("target-path", "target_path", StringOptionParser, "xyongle output-data-path after processing: target-path", default="")
        op.add_option("out-size", "out_size", IntegerOptionParser, "xyongle the out-size size for every times --out-size", default=0)
        op.add_option("start-batch-num", "start_batch_num", IntegerOptionParser, "xyongle the start_batch_num for every times --start-batch-num", default=0)
        op.add_option("output-batch-size", "out_batch_size", IntegerOptionParser, "xyongle the batch size for every times --output-batch-size", default=0)
        op.add_option("x-label", "x_label", IntegerOptionParser, "xyongle the batch size for every times --x-label", default=0)

        op.add_option("x-type", "x_type", IntegerOptionParser, "xyongle exec different method: -x-type", default=0)
        #op.add_option("txt-file-name", "txt_file_name", StringOptionParser, "xyongle output-data-path after processing: txt_file_name", default="")

        return op
    ## parameter process
    @staticmethod
    def parse_options(op):
        try:
            options = op.parse()
            load_location = None
#            print options['load_file'].value_given, options['save_file_override'].value_given
#            print options['save_file_override'].value

            op.eval_expr_defaults()
            return op
        except OptionMissingException, e:
            print e
            op.print_usage()
        except OptionException, e:
            print "Error loading checkpoint:"
            print e
        sys.exit()
if __name__ == "__main__":


    try:
        op = xMakeData.get_options_parser()
        # options = op.parse()
        op = xMakeData.parse_options(op)
        for o in op.options.keys():print o, op.options[o].prefixed_letter, op.options[o].value
        xdata = xMakeData()

        xdata.exeFlickrTxt(op, 'flickr2349_group')
        xdata.exeFlickrTxt(op, 'flickr3500_group')
        xdata.exeFlickrTxt(op, 'flickr5000_group')
        xdata.exeFlickrTxt(op, 'flickr10000_group')

  


    except (xyongleError), e:
        print "----------------"
        print "Error:"

    # model = xMakeData()
    # value = model.exe(img_path)
    #
    # print len(value)

