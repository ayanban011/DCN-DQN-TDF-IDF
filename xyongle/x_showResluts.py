__author__ = 'xyongle'

import os
from cStringIO import StringIO
import cPickle as cp
from python_util import  options

if __name__ == "__main__":
    filename = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/NIST_Tatt/tatt-c_ongoing/tattoo_detection/NIST_tmp4/ConvNet__2015-10-11_18.51.20/200.0'
    filename = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/NIST_Tatt/tatt-c_ongoing/tattoo_detection/NIST_tmp3/ConvNet__2015-10-11_15.22.17/200.0'
    filename = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/NIST_Tatt/tatt-c_ongoing/tattoo_detection/NIST_tmp2/ConvNet__2015-10-11_13.02.51/200.0'
    filename = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/NIST_Tatt/tatt-c_ongoing/tattoo_detection/NIST_tmp1/ConvNet__2015-10-11_10.03.56/200.0'
    filename = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/NIST_Tatt/tatt-c_ongoing/tattoo_detection/NIST_tmp0/ConvNet__2015-10-10_19.52.05/100.0'

    filename = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/flickr/Tattoo_tmp/ConvNet__2015-10-02_16.31.13/100.1'
    filename = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/flickr_batches/data_batch_0/data_batch_0.0'

    filename = '/media/ubuntu/7E02BE0002BDBD89/xyongle/Images/flickr_20000_tmp/ConvNet__2015-10-14_19.43.26/200.5'

    fo = open(filename,'r')
    z = StringIO()
    file_size = os.fstat(fo.fileno()).st_size
    while fo.tell() < file_size:z.write(fo.read(1 << 30))
    fo.close()
    dict = cp.loads(z.getvalue())
    z.close()
    model_state = dict['model_state']
    test_outputs = model_state['test_outputs']
    for m in test_outputs:print m
    # fo = open(filename,'r')
    # z = StringIO()
    # file_size = os.fstat(fo.fileno()).st_size
    # while fo.tell() <file_size:z.write(fo.read(1 << 30))
    # fo.close()
    # dict = cp.loads(z.getvalue())
    # z.close()
    #
    #
    # model_state = dict['model_state']
    # train_outputs = model_state['train_outputs']
    # test_outputs = model_state['test_outputs']

    # print test_outputs

