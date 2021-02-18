# Record RGBD Video with iPhone 12 Pro

## Get the Application
[Record3D](https://record3d.app)

## Export and Share the Videos
Library - Export - r3d - Share  

## Process the Videos
python r3d_process.py \[options\]
--path: Folder that contains r3d files.  
--depth: Decode depth file.  
--video: Save RGB and depth video.  
--quiet: Disable logs.  
  
## Structure  
*.mp4 is for visualization. Use the data in the rgbd folder instead.  
metadata: Binary file. K is the intrinsic matrix [fx, 0, 0, s, fy, 0, x0, y0, 1].  

Folder: rgbd  
frame#.jpg: 256\*192 or 960\*720 rgb.  
frame#.depth: Original depth (lzfse).  
frame#.depth_new: Depth map (float32), 256\*192. Each value is the actual depth value in meters. USE THIS ONE.  
frame#.depth_new.jpg: Depth map for visualization.  
frame#.conf: Confidence map for each frame. The size is the same as the depth map and for each pixel of the depth map it contains an uint8 number in the range 0-2, which suggest the confidence that the sensed LiDAR depth is "correct". In other words, it is a measure of depth data quality.  

