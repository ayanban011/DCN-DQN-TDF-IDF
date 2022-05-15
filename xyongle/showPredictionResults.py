__author__ = 'ubuntu'

import os
import cPickle
import numpy as np
import PIL.Image as Image

from CommonFileUtil import CommonFile

#CNN_DATA = 'nist'
CNN_DATA = 'flickr10000'
PRE_DATA = 'flickr2349'
#PRE_DATA = 'nist'

class showResults():
    def getError(self,path):
        commonfile = CommonFile()
        fileNames = commonfile.getFileList(path,'.txt')

        content = []
        for file in fileNames:
            content = content + commonfile.readTxtFile(file)

        tatt_to_nontatt_num = 0
        nontatt_tatt_num = 0
        tatt_corr_num = 0
        nontatt_corr_num = 0

        targetPath10 = '/home/xyongle/images/ICB/prediction/' + CNN_DATA + '_pred_' + PRE_DATA + '_42_error_10'
        targetPath01 = '/home/xyongle/images/ICB/prediction/' + CNN_DATA + '_pred_' + PRE_DATA + '_42_error_01'
        for value in content:
            values = value.split(' ')
            fileName = values[0].split('/')[-1]
            srcPath = values[0][0:len(value[0])-len(fileName)-2]
            if 'CORRECT_1_1' == values[-1]:
                nontatt_corr_num = nontatt_corr_num + 1
            elif 'CORRECT_0_0' == values[-1]:
                tatt_corr_num = tatt_corr_num + 1
            elif 'ERROR_1_0' == values[-1]:
                tatt_to_nontatt_num = tatt_to_nontatt_num + 1  
                #print value
                commonfile.copyFile(srcPath, fileName, targetPath10, fileName)
            elif 'ERROR_0_1' == values[-1]:
                nontatt_tatt_num = nontatt_tatt_num + 1 
                #print value
                commonfile.copyFile(srcPath, fileName, targetPath01, fileName)
            #if 'ERROR_0_1' == values[-1]:
            #    tatt_nontatt_num = tatt_nontatt_num + 1
            #elif 'ERROR_1_0' == values[-1]:
            #    nontatt_tatt_num = nontatt_tatt_num + 1
        print tatt_corr_num, tatt_to_nontatt_num, nontatt_corr_num, nontatt_tatt_num 
        return tatt_corr_num, tatt_to_nontatt_num, nontatt_corr_num, nontatt_tatt_num 
if __name__ == "__main__":
    print 'test start   ' * 5

    path = '/home/ubuntu/tool/cuda-workspace/cuda-convnet2/make_data/data/flickr_classfy_results'
    path = '/home/xyongle/images/ICB/prediction/nist_pred_nist_42_'
    path = '/home/xyongle/images/ICB/prediction/nist_pred_nist_42_error_01'
    #path = '/home/xyongle/images/ICB/flickr_pre_10000/prediction/nist_42_'
    #path = '/home/xyongle/images/ICB/flickr_pre_10000/prediction/flickr_pre_10000_pred_nist_42_'
    #path = '/home/ubuntu/tool/cuda-workspace/cuda-convnet2/make_data/data/flcikr_pre'
    path = '/home/xyongle/images/ICB/prediction/' + CNN_DATA + '_pred_' + PRE_DATA + '_42_'

    show = showResults()
    tatto_to_notattoo=0
    notattoo_to_tatto=0
    start_num = 1 


    tatt_corr_num = 0
    tatt_err_num = 0
    nontatt_corr_num = 0
    nontatt_err_num = 0 

    total_num = 0
    for ind in range(start_num,start_num + 5):
      work_path = path + str(ind)
      #work_path = path
      #tatt_corr_num,tatt_err_num,nontatt_corr_num,nontatt_err_num = show.getError(work_path)
      a,b,c,d  = show.getError(work_path)
      #total_num = tatt_corr_num + tatt_err_num + nontatt_corr_num + nontatt_err_num

      tatt_corr_num = tatt_corr_num + a
      tatt_err_num = tatt_err_num + b
      nontatt_corr_num = nontatt_corr_num + c
      nontatt_err_num = nontatt_err_num + d 

      total_num = total_num + a + b + c + d
      print work_path
    print '==================================================================='
    #print tatto_to_notattoo,1000- tatto_to_notattoo, notattoo_to_tatto, 1349-notattoo_to_tatto
    print 'total_num = ',total_num
    tatt_total_num = tatt_corr_num + tatt_err_num
    nontatt_total_num = nontatt_corr_num + nontatt_err_num
    print 'tatt_total_num = ',(tatt_corr_num + tatt_err_num), 'nontatt_total_num=',(nontatt_corr_num + nontatt_err_num)
    print  tatt_corr_num,tatt_err_num,nontatt_corr_num,nontatt_err_num
    print 'tatoo and notattoo correct rate:'
    print tatt_corr_num/float(tatt_corr_num + tatt_err_num), nontatt_corr_num/float(nontatt_corr_num + nontatt_err_num)
    print 'tatoo and notattoo error rate:'
    print tatt_err_num/float(tatt_corr_num + tatt_err_num), nontatt_err_num/float(nontatt_corr_num + nontatt_err_num)
    print 'total correct rate:'
    #print tatto_to_notattoo + notattoo_to_tatto,(tatto_to_notattoo + notattoo_to_tatto)/2349.0
    print tatt_corr_num + nontatt_corr_num, (tatt_corr_num + nontatt_corr_num)/float(total_num)
    print 'latex code ==============================='
    print '&  ',  tatt_corr_num,  '&  ',  tatt_err_num, '&  ',  nontatt_corr_num, '&  ',  nontatt_err_num,  '&  ', total_num
    print '&  ',  tatt_corr_num,'/',tatt_total_num,'=',tatt_corr_num/float(tatt_total_num),  '&  ', tatt_err_num,'/',tatt_total_num,'=',tatt_err_num/float(tatt_total_num)
    print '&  ',  nontatt_corr_num,'/',nontatt_total_num,'=',nontatt_corr_num/float(nontatt_total_num), '&  ',  nontatt_err_num,'/',nontatt_total_num,'=',nontatt_err_num/float(nontatt_total_num)
    print '&  ', tatt_corr_num + nontatt_corr_num,'/',total_num,'=',(tatt_corr_num + nontatt_corr_num)/float(total_num)
    #print '&  ',  tatt_corr_num,'/',tatt_total_num,'=',tatt_corr_num/float(tatt_total_num),  '&  ',  tatt_err_num,'/',tatt_total_num,'=',tatt_err_num/float(tatt_total_num) '&  ',  nontatt_corr_num,'/',nontatt_total_num,'=',nontatt_corr_num/float(nontatt_total_num), '&  ',  nontatt_err_num,'/',nontatt_total_num,'=',nontatt_err_num/float(nontatt_total_num),  '&  ', tatt_corr_num + nontatt_corr_num,'/',total_num,'=',(tatt_corr_num + nontatt_corr_num)/float(total_num)

