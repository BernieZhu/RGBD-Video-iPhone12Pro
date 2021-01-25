import numpy as np
import matplotlib.pyplot as plt
import cv2
import struct
import os
import sys
import argparse

path = '/Users/zhu/Desktop/Salad/'

def depth2image(filename, nx, ny):
    f = open(filename, "rb")
    img = np.zeros((nx, ny))
    for i in range(nx):
        for j in range(ny):
            data = f.read(4)
            elem = struct.unpack("f", data)[0]
            img[i][j] = elem
    f.close()
    return img

def get_video(folder, typename):
    if (typename == 'depth' or typename == 'depth_new'):
        typename = 'depth_new.jpg'
    in_folder = os.path.join(folder, 'rgbd')
    out = os.path.join(folder, typename+'.mp4')
    os.system('ffmpeg -loglevel quiet -threads 2 -y -r 30 -i '+in_folder+'/%d.'+typename+' '+out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', action='store_const', const='depth')
    parser.add_argument('--video', action='store_const', const='video')
    parser.add_argument('--quiet', action='store_const', const='quiet')
    args = parser.parse_args()

    # unzip r3d
    for r3d in os.listdir(path):
        if(r3d[-4:] == '.r3d'):
            os.system('unzip -q -n '+os.path.join(path, r3d)+' -d '+path+'/'+r3d[:-4])

    # decoding depth files
    for i in os.listdir(path):
        folder = os.path.join(path, i)
        if (os.path.isdir(folder)):
            rgbd_folder = os.path.join(folder, 'rgbd')
            if(args.depth):
                for j in os.listdir(rgbd_folder):
                    if(j[-6:] == '.depth'):
                        depth = os.path.join(rgbd_folder, j)
                        os.system('lzfse -decode -i '+depth+' -o '+depth+'_new')
                if (not args.quiet): print('Depth data saved at '+rgbd_folder)
                    
            if(args.video):
                # rgb video
                get_video(folder, 'jpg')
                if (not args.quiet): print('RGB video saved at '+folder)
                if(args.depth):
                    # save depth maps
                    for j in os.listdir(rgbd_folder):
                        if(j[-4:] == '_new'):
                            depth = os.path.join(rgbd_folder, j)
                            depthmap = depth2image(depth, 256, 192)
                            plt.imsave(depth+'.jpg', depthmap, format='jpg', cmap=plt.cm.gray)
                    if (not args.quiet): print('Depth maps saved at '+rgbd_folder)

                    # depth video
                    get_video(folder, 'depth_new')
                    if (not args.quiet): print('Depth video saved at '+folder)
                else:
                    continue
        
if __name__ == "__main__":
    main()