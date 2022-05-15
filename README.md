# DCN-DQN-TF-IDF
#########################################################################################
##
## The code is prepared based on the deformable convolution network proposed at https://github.com/msracver/Deformable-ConvNets
## 
## Please refer the document if you want to run the code.
##
########################################################################################

1. Install Cuda-convnet
   The version is cuda-convnet2. The detail installed command is showed in the web:
   https://code.google.com/archive/p/cuda-convnet2/.
2. make-data for cuda-convnet
   The code is showed in ./make-data/ICB_makedata.py and the code to generate the meta 
   file is showed with code ./ICB_makemeta.py
3. Net define
   The net file is located ./layers/
4. The train commond is showed in the fold ./xyongle_sh
