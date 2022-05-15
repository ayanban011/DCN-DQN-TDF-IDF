
##############################################################################################
##
## convnet.py train a CNN networks
## author: xu qingyong
## mail: n1509179сп@e.ntu.edu.sg, xyongle@163.com
##
###############################################################################################
DT=`date '+%Y-%m-%d_%H.%M.%S'`
SRCROOT=/home/xyongle/images/layers
DSTROOT=/home/xyongle/images/ICB/Flickr10000
LAYERS=nist-layers-1gpu-42.cfg
LPARAMS=nist-layer-params-1gpu.cfg

mkdir -p $DSTROOT
cp {$SRCROOT,$DSTROOT}/$LAYERS
cp {$SRCROOT,$DSTROOT}/$LPARAMS

#python convnet.py \
#srun -x pdccmc1 -p gpu -n 1 --gres=gpu:1 python convnet.py \
# --data-path=/home/xyongle/images/Cifar \/home/xyongle/images/Cifar
  #--data-path=/home/xyongle/images/nist/nist_batch$ind \
  #--data-path=/home/xyongle/images/tatt-c_ongoing/tattoo_detection/NIST_batches0 \
ind=1
train_range=1-4
#while (($ind <= 5))
#do
  #mkdir $DSTROOT/$ind
 srun -p gpu -n 1 --gres=gpu:1 python convnet.py \
  --data-path=$DSTROOT/batch$ind \
  --save-path=$DSTROOT/batch$ind/ConvNet_42_$train_range \
  --test-range=1000 \
  --train-range=$train_range \
  --layer-def=$DSTROOT/$LAYERS \
  --layer-params=$DSTROOT/$LPARAMS \
  --data-provider=image \
  --gpu=0 \
  --epochs=1000 \
  --test-freq=10 \
  --inner-size 227 
#  --write-feature=$DSTROOT 
#  --inner-size 24 \ 
#  --test-freq=20
  echo $ind
  let "ind=ind+1"
#done

#srun -p gpu -n 1 python convnet.py  --data-path=./cifar-10-py-colmajor  --save-path=$DSTROOT --test-range=6 --train-range=1-5  --layer-def=$DSTROOT/$LAYERS --layer-params=$DSTROOT/$PARAMS  --data-provider=cifar-cropped --test-freq=13
