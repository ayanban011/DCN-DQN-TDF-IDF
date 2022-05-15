__author__ = 'ubuntu'

from xyongle.CommonFileUtil import *
from xyongle.CommonDataAnalysis import DataAnalysis

if __name__ == '__main__':
    print 'test'

    # batchFile = CudaImageBatchFile()
    # batchFile.getBatchData('../data/data_batch_1000')

    # test data format
    tgt_dir ='/media/ubuntu/My Passport/flickr_images/flickr_batch/data_batch_1000/data_batch_1000.0'

    ayanlysis = DataAnalysis()
    filenames = ayanlysis.JpegDictAyalysis(tgt_dir)
    print filenames