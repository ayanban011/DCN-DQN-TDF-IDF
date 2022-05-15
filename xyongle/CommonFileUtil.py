__author__ = 'ubuntu'

import math
import os
from cStringIO import StringIO
import cPickle as cp
#from python_util import options
#from python_util.data import *
import itertools as it
import itertools

class Circle:
    # Construct a circle object
    def __init__(self, radius = 1):
        self.radius = radius

    def getPerimeter(self):
        return 2 * self.radius * math.pi

    def getArea(self):
        return self.radius * self.radius * math.pi

    def setRadius(self, radius):
        self.radius = radius


class CommonFile:

    # def wirteTxt(self,value,file):
    #     for m in value:
    #         file.write("%s\n" % m)
    # def __init__(self):
    #     self.name = "class CommonFile"


    @staticmethod
    def copyFiles(sourceDir, targetDir):
        if sourceDir.find(".svn") > 0:
            return
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,file)
            targetFile = os.path.join(targetDir,file)
            if os.path.isfile(sourceFile):
                if os.path.exists(targetDir) == False:
                    os.makedirs(targetDir)
                if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
            if os.path.isdir(sourceFile):
                CommonFile.copyFiles(sourceFile, targetFile)
        if os.path.isfile(sourceFile):
            # if os.path.exists(targetDir) == False:
            #     os.makedirs(targetFile)
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())


    @staticmethod
    def copyFile(sourceDir, sourceFileName, targetDir, targetFileName):
        sourceFile = os.path.join(sourceDir,sourceFileName)
        targetFile = os.path.join(targetDir, targetFileName)
        if os.path.isfile(sourceFile):
            if os.path.exists(targetDir) == False:
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
    @staticmethod
    def mkdirs(path):
        os.path.mkdir(os.path.split(path))

    @staticmethod
    def deleteFile(self,src):
        if os.path.isfile(src):
            try:
                os.remove(src)
            except:
                pass
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc = os.path.join(src,item)
                self.deleteFile(self,itemsrc)
                try:
                    os.rmdir(src)
                except:
                    pass

    @staticmethod
    def writeTxt(value,fileName):
        print type(value)
        # list = [line+'\n' for line in value]
        # file = open("./%s" % (fileName), 'w')
        file = open(fileName,'w')
        file.writelines(["%s\n" % item  for item in value])
        # file.writelines(list)
        file.close()


    @staticmethod
    def displayvalue(list):
        # for m in value:print m
        print list

    # def getFileList(self, path):
    #     listfile=os.listdir(path)
    #
    #     return listfile
    #
    # def getJpgFileList(self, path):
    #     listfile=os.listdir(path)
    #
    #     # for line in listfile:
    #
    #     return listfile

    @staticmethod
    def isSubString(SubStrList,Str):
        flag=True
        for substr in SubStrList:
            if not(substr in Str):
                flag=False

        return flag
    #############################################
    # return the filelist(full name) if Flagstr have value, return the list, other return all.
    ##########################################
    def getFileList(self,filePath,FlagStr=[]):
        FileList=[]
        FileNames=os.listdir(filePath)
        if (len(FileNames)>0):
           for fn in FileNames:
               if (len(FlagStr)>0):
                   # return file name
                   if (self.isSubString(FlagStr,fn)):
                       fullfilename=os.path.join(filePath,fn)
                       FileList.append(fullfilename)
               else:
                   # return file name
                   fullfilename=os.path.join(filePath,fn)
                   FileList.append(fullfilename)

        if (len(FileList)>0):
            FileList.sort()

        return FileList

    @staticmethod
    def readTxtFile(fileName):
        if os.path.exists(fileName) == False:
            return

        fo = open(fileName, 'r')

        rtn = [line.strip() for line in fo]
        fo.close()

        # rtn = [m for m in tmp if len(m) > 0]

        return rtn

    @staticmethod
    def fileExists(filename):
        if os.path.exists(filename):
            return True
        else:
            return False

class CudaResultFile:

    def readResultDictFile(self,fileName):
        fo = open(fileName,'r')
        z = StringIO()
        file_size = os.fstat(fo.fileno()).st_size
        while fo.tell() < file_size:z.write(fo.read(1 << 30))
        fo.close()
        dict = cp.loads(z.getvalue())
        z.close()

        model_state = dict['model_state']
        op = dict['op']
        # test_outputs = model_state['test_outputs']
        return model_state,op

    def getTestErrorResult(self,fileName):
        fo = open(fileName,'r')
        z = StringIO()
        file_size = os.fstat(fo.fileno()).st_size
        while fo.tell() < file_size:z.write(fo.read(1 << 30))
        fo.close()
        dict = cp.loads(z.getvalue())
        z.close()

        model_state = dict['model_state']
        return model_state['test_outputs']

    def getTestErrorRate(self,filename):

        test_outputs = self.getTestErrorResult(filename)

        # for m in test_outputs:print m
        errors =  [o[0]['logprob'][0]/o[1] for o in test_outputs]

        return errors

        # test_errors = np.row_stack(test_errors)
        # test_errors = np.tile(test_errors, (1, self.testing_freq))
        # test_errors = list(test_errors.flatten())
        # test_errors += [test_errors[-1]] * max(0,len(train_errors) - len(test_errors))
        # test_errors = test_errors[:len(train_errors)]

    def getTrainErrorResult(self,fileName):
        fo = open(fileName,'r')
        z = StringIO()
        file_size = os.fstat(fo.fileno()).st_size
        while fo.tell() < file_size:z.write(fo.read(1 << 30))
        fo.close()
        dict = cp.loads(z.getvalue())
        z.close()

        model_state = dict['model_state']
        return model_state['train_outputs']


    def getTrainErrorRate(self,filename):

        outputs = self.getTrainErrorResult(filename)

        # for m in test_outputs:print m
        errors =  [o[0]['logprob'][0]/o[1] for o in outputs]

        return errors

class CudaImageBatchFile:


    def getBatchFile(self,fname):

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



    def getBatchData(self,path):

        fname = path #os.path.join(path, 'data_batch_%d' % batch_num)      #path + '/' + batch_num
        # print 'test'
        rawdics = self.getBatchFile(fname)
        print 'test'

        return rawdics[0]
        # if type(rawdics) != list:
        #     rawdics = [rawdics]
        # nc_total = sum(len(r['data']) for r in rawdics)
        #
        # jpeg_strs = list(it.chain.from_iterable(rd['data'] for rd in rawdics))
        #
        # img_mat = n.empty((nc_total * data_mult, inner_pixels * num_colors), dtype=n.float32)
        #
        # convnet.decodeJpeg(jpeg_strs, img_mat, img_size, inner_size, testFlag, multiview)
        # img_num = len(img_mat)
        #
        # return img_mat, img_num

if __name__ == '__main__':
   sDir = '/home/ubuntu/NTU/paper/paper/tattoo'
   tDir = '/home/ubuntu/NTU/paper/paper/test'
   CommonFile.copyFiles(sDir,tDir)
