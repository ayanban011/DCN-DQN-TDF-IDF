
##############################################################################################
##
## write by xyongle@163.com on 2015-11-19
##
###################################################################################################

## make data path from origin JPEG for tattoo
## batch num start 10000
echo "Start tattoo makedata......................"

#srun -p gpu -n 1 --gres=gpu:1 python x_makedata.py \
python ICB_makedata.py \
    --data-path /no-use/ \
    --target-path /home/batch \
    --out-size 256 \
    --start-batch-num 1 \
    --output-batch-size 2000 \
    --x-label 0 \
    --x-type 32

echo "Finisih tattoo makedata......................"
#python ../x_makemeta.py
