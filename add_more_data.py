import numpy as np
import h5py
import os, sys, traceback
import os.path as osp
import wget, tarfile
import cv2
from PIL import Image
from matplotlib import pyplot as plt


def get_data(DB_FNAME):
    """
    Download the image,depth and segmentation data:
    Returns, the h5 database.
    """
    return h5py.File(DB_FNAME,'r')


def add_more_data_into_dset(DB_FNAME,more_img_file_path,more_depth_path,more_seg_path):
    db=h5py.File(DB_FNAME,'w')
    depth_db=get_data(more_depth_path)
    seg_db=get_data(more_seg_path)
    db.create_group('image')
    db.create_group('depth')
    db.create_group('seg')
    cnt = 0
    for imname in os.listdir(more_img_file_path):
        if imname.endswith('.jpg'):
            full_path=more_img_file_path+imname
            print full_path,imname
            if imname not in depth_db.keys():
                print '%s is not in depth_db'%imname
                continue
            elif imname not in seg_db['mask'].keys():
                print '%s is not in seg_db'%imname
                continue
            
            try:
                img = cv2.imread(full_path)
            except:
                continue
            #imgSize=j.size
            #rawData=j.tobytes()
            #img=Image.frombytes('RGB',imgSize,rawData)
            #img = img.astype('uint16')
            db['image'].create_dataset(imname,data=img[:,:,::-1])
            db['depth'].create_dataset(imname,data=depth_db[imname])
            db['seg'].create_dataset(imname,data=seg_db['mask'][imname])
            db['seg'][imname].attrs['area']=seg_db['mask'][imname].attrs['area']
            db['seg'][imname].attrs['label']=seg_db['mask'][imname].attrs['label']
            cnt += 1
    print 'the total count is %d'%cnt
    db.close()
    depth_db.close()
    seg_db.close()


# path to the data-file, containing image, depth and segmentation:
DB_FNAME = '/media/zhaoke/806602c3-72ac-4719-b178-abc72b3fa783/zhaoke/bgimgs/dset_8000.h5'

#add more data into the dset
more_depth_path='/media/zhaoke/806602c3-72ac-4719-b178-abc72b3fa783/zhaoke/bgimgs/depth.h5'
more_seg_path='/media/zhaoke/806602c3-72ac-4719-b178-abc72b3fa783/zhaoke/bgimgs/seg.h5'
more_img_file_path='/home/zhaoke/justrypython/SynthText_Chinese_version/data/bg_img/'

add_more_data_into_dset(DB_FNAME,more_img_file_path,more_depth_path,more_seg_path)
