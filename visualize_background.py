# Author: Ankush Gupta
# Date: 2015

"""
Visualize the generated localization synthetic
data stored in h5 data-bases
"""
from __future__ import division
import os
import os.path as osp
import numpy as np
import matplotlib.pyplot as plt 
import h5py 
from common import *
from time import sleep


def viz_imgs(imgs, alpha=1.0):
    """
    text_im : image containing text
    charBB_list : list of 2x4xn_i bounding-box matrices
    wordBB : 2x4xm matrix of word coordinates
    """
    plt.close(1)
    fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)
    
    plt.subplot(2, 2, 1)
    plt.imshow(imgs[0])
    plt.subplot(2, 2, 2)
    plt.imshow(imgs[1])
    plt.subplot(2, 2, 3)
    plt.imshow(imgs[2])
    plt.subplot(2, 2, 4)
    plt.imshow(imgs[3])
    plt.hold(True)
    plt.show(block=False)


def viz_textbb(text_im, charBB_list, wordBB, alpha=1.0):
    """
    text_im : image containing text
    charBB_list : list of 2x4xn_i bounding-box matrices
    wordBB : 2x4xm matrix of word coordinates
    """
    plt.close(1)
    plt.figure(1)
    plt.imshow(text_im)
    plt.hold(True)
    H,W = text_im.shape[:2]

    # plot the character-BB:
    for i in xrange(len(charBB_list)):
        bbs = charBB_list[i]
        ni = bbs.shape[-1]
        for j in xrange(ni):
            bb = bbs[:,:,j]
            bb = np.c_[bb,bb[:,0]]
            plt.plot(bb[0,:], bb[1,:], 'r', alpha=alpha/2)

    # plot the word-BB:
    for i in xrange(wordBB.shape[-1]):
        bb = wordBB[:,:,i]
        bb = np.c_[bb,bb[:,0]]
        plt.plot(bb[0,:], bb[1,:], 'g', alpha=alpha)
        # visualize the indiv vertices:
        vcol = ['r','g','b','k']
        for j in xrange(4):
            plt.scatter(bb[0,j],bb[1,j],color=vcol[j])        

    plt.gca().set_xlim([0,W-1])
    plt.gca().set_ylim([H-1,0])
    plt.show(block=False)

def main(db_fname):
    db = h5py.File(db_fname, 'r')
    dsets = sorted(db['image'].keys())
    print "total number of images : ", colorize(Color.RED, len(dsets), highlight=True)
    for k in dsets:
        rgb    = db['image'][k][...]
        depth  = db['depth'][k][...]
        depth0 = depth[0].transpose((1, 0))
        depth1 = depth[1].transpose((1, 0))
        seg    = db['seg'][k][...]

        #viz_textbb(rgb, [], np.array([]))
        viz_imgs([depth0, depth1, seg, rgb])
        print "image name        : ", colorize(Color.RED, k, bold=True)
        
        #sleep(0.1)
        if 'q' in raw_input("next? ('q' to exit) : "):
            break
    db.close()

if __name__=='__main__':
    #main('results/SynthText_cartoon_viz.h5')
    #main('/media/zhaoke/806602c3-72ac-4719-b178-abc72b3fa783/zhaoke/bgimgs/dset_8000.h5')
    main('/home/zhaoke/justrypython/SynthText_Chinese_version/data/dset.h5')

