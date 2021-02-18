import numpy as np
import matplotlib.pyplot as plt
import cv2
import struct
import os
import sys
import argparse
import liblzfse

def load_depth(filepath):
    with open(filepath, 'rb') as depth_fh:
        raw_bytes = depth_fh.read()
        decompressed_bytes = liblzfse.decompress(raw_bytes)
        depth_img = np.frombuffer(decompressed_bytes, dtype=np.float32)
    depth_img = depth_img.reshape((640, 480))
    return depth_img

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
        typename = 'depth.jpg'
    in_folder = os.path.join(folder, 'rgbd')
    out = os.path.join(folder, typename+'.mp4')
    os.system('ffmpeg -loglevel quiet -threads 2 -y -r 30 -i '+in_folder+'/%d.'+typename+' '+out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True)
    parser.add_argument('--depth', action='store_const', const='depth')
    parser.add_argument('--video', action='store_const', const='video')
    parser.add_argument('--quiet', action='store_const', const='quiet')
    args = parser.parse_args()

    if(not os.path.exists(args.path)):
        print('ERROR: Wrong path!')
        return
    if(os.listdir(args.path)==[]):
        print('ERROR: Empty folder!')
        return
    # unzip r3d
    for r3d in os.listdir(args.path):
        if(r3d[-4:] == '.r3d'):
            os.system('unzip -q -n '+os.path.join(args.path, r3d)+' -d '+args.path+'/'+r3d[:-4])
            os.system('rm '+os.path.join(args.path, r3d[:-4])+'/sound.aac')
    # decoding depth files
    for i in os.listdir(args.path):
        folder = os.path.join(args.path, i)
        if (os.path.isdir(folder)):
            rgbd_folder = os.path.join(folder, 'rgbd')
            if(not os.path.exists(rgbd_folder)):
                continue
            if(args.depth):
                for j in os.listdir(rgbd_folder):
                    if(j[-6:] == '.depth'):
                        depth_path = os.path.join(rgbd_folder, j)
                        os.system('lzfse -decode -i '+depth_path+' -o '+depth_path+'_new')
                        if(args.depth):
                            depth_img = load_depth(depth_path)
                            cv2.imwrite(depth_path+'.jpg', depth_img*255)
                if (not args.quiet): print('Depth data saved at '+rgbd_folder)
                    
            if(args.video):
                # rgb video
                get_video(folder, 'jpg')
                if (not args.quiet): print('RGB video saved at '+folder)
                if(args.depth):
                    # depth video
                    get_video(folder, 'depth_new')
                    if (not args.quiet): print('Depth video saved at '+folder)
                else:
                    continue
        
if __name__ == "__main__":
    main()