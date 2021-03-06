__author__ = 'xyongle'

# function: read from the batches and computer the mean
#       Then save then mean data to meta-data
import ctypes



import sys
import os

curr_path = os.getcwd()
parent_path = curr_path[0:len(curr_path)-10]

import itertools as it

import numpy as np
from numpy import array
import numpy as n
import itertools
from python_util.data import *
import cudaconvnet._ConvNet as convnet
from PIL import Image

def get_batch(path,batch_num):
        fname = os.path.join(path, 'data_batch_%d' % batch_num)      #path + '/' + batch_num
        print fname
        if os.path.isdir(fname): # batch in sub-batches
            sub_batches = sorted(os.listdir(fname), key=alphanum_key)
            num_sub_batches = len(sub_batches)
            tgts = [[] for i in xrange(num_sub_batches)]
            threads = [DataLoaderThread(os.path.join(fname, s), tgt) for (s, tgt) in zip(sub_batches, tgts)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            return [t[0] for t in tgts]
          
        return unpickle(fname)
def makeMean (load_path, img_size, start_batch_num, end_batch_num):
    data_mult = 1
    # img_size = 256
    inner_pixels = img_size*img_size                          ## inner_size^2  80*80
    num_colors = 3                                   #RGB

    inner_size = img_size
    testFlag = False
    multiview = 0

    img_num = 0
    sum_mat = n.empty((inner_pixels * num_colors), dtype=n.float32)
#    for batch_num in range(1,25):
    for batch_num in range(start_batch_num, end_batch_num+1):
        # batch_num = 0       #  0-5
        # load_path = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/flickr_batches_20000'
    #     #####################################################################################
    #     ###
    #     ### convdata.py  Line 40
    #     ######################################################################
        rawdics = get_batch(load_path,batch_num)
        if type(rawdics) != list:
            rawdics = [rawdics]
        nc_total = sum(len(r['data']) for r in rawdics)

        jpeg_strs = list(it.chain.from_iterable(rd['data'] for rd in rawdics))
        #labels = list(it.chain.from_iterable(rd['labels'] for rd in rawdics))


        img_mat = n.empty((nc_total * data_mult, inner_pixels * num_colors), dtype=n.float32)

        convnet.decodeJpeg(jpeg_strs, img_mat, img_size, inner_size, testFlag, multiview)

        img_num = img_num + len(img_mat)

        sum_mat = n.add(sum_mat, sum(img_mat))

    return sum_mat/img_num
def getImgData (img_path, img_size,inner_size):

    rawdics = get_batch(img_path,0)
    if type(rawdics) != list:
        rawdics = [rawdics]
    nc_total = sum(len(r['data']) for r in rawdics)
    jpeg_strs = list(it.chain.from_iterable(rd['data'] for rd in rawdics))
    #labels = list(it.chain.from_iterable(rd['labels'] for rd in rawdics))

    num_colors = 3
    inner_size = img_size
    testFlag = False
    multiview = 0
    img_mat = n.empty((nc_total * 1, inner_size * inner_size * num_colors), dtype=n.float32)

    convnet.decodeJpeg(jpeg_strs, img_mat, img_size, inner_size, testFlag, multiview)

    print img_mat
    return img_mat
def getImgData2(img_path,img_size,inner_size):
    image = Image.open(img_path)
    image = np.array( image )           # 32 x 32 x 3
    image = np.rollaxis( image, 2 )     # 3 x 32 x 32
    image = image.reshape( -1 )         # 3072

    print image

    
def makeNistFlickrMeta(load_path,start_batch_num, end_batch_num):
    OUTPUT_BATCH_SIZE = 2000
    OUTPUT_SUB_BATCH_SIZE = 1000
    OUTPUT_IMAGE_SIZE = 256
#    load_path = '/home/xyongle/images/ICB/nist_flickr_batch' + str(ind)
# 1-24: start=1 and end = 25
    start_batch_num = 1
    end_batch_num = end_batch_num + 1
    
    tgt_dir = load_path

    meanData = makeMean(load_path, OUTPUT_IMAGE_SIZE, start_batch_num, end_batch_num)

    label_names = ['tattoo','nontattoo']
        # Write meta file
    meta = unpickle('make-data/input_meta')
    meta_file = os.path.join(tgt_dir, 'batches.meta')
    meta.update({'batch_size': OUTPUT_BATCH_SIZE,
                 'num_vis': OUTPUT_IMAGE_SIZE**2 * 3,
                 'inner_size': OUTPUT_IMAGE_SIZE**2 * 3,
                 'label_names': label_names,
                 'data_mean': meanData})
    pickle(meta_file, meta)


    print "Wrote %s" % meta_file
    print "All done!  batches are in %s" % tgt_dir
if __name__ == "__main__":

    #tgt_dir = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/flickr_batches_20000_96'
    # makeNistMeta()
    flickr_root_path = '/mnt/ICB/data/Flickr/'
    nist_root_path = '/mnt/ICB/data/NIST/'
    for ind in range(1,6)
      load_path = os.path.join(flickr_root_path, 'flickr2349_group/batches' + str(ind))
      makeNistFlickrMeta(load_path, 1, 1)

      load_path = os.path.join(flickr_root_path, 'flickr3500_group/batches' + str(ind))
      makeNistFlickrMeta(load_path, 1, 2)

      load_path = os.path.join(flickr_root_path, 'flickr5000_group/batches' + str(ind))
      makeNistFlickrMeta(load_path, 1, 2)

      load_path = os.path.join(flickr_root_path, 'flickr10000_group/batches' + str(ind))
      makeNistFlickrMeta(load_path, 1, 4)

