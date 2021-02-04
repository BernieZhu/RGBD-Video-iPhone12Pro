# Record RGBD Video with iPhone 12 Pro

## Get the Application
[Record3D](https://record3d.app)

## Export and Share the Videos
Library - Export - r3d - Share  

## Process the Videos
Change the path in r3d_process.py to the folder that contains r3d files.  
python r3d_process.py \[options\]

--depth: Decode depth file.  
--video: Save RGB and depth video.  
--quiet: Disable logs.  
  
## Structure  
*.mp4 is for visualization. Use the data in the rgbd folder instead.  
metadata: Binary file. K is the intrinsic matrix [fx, 0, 0, s, fy, 0, x0, y0, 1].  

Folder: rgbd  
frame#.conf  
frame#.jpg  
frame#.depth: Original depth (lzfse).  
frame#.depth_new: Depth map (float32), use depth2image() to decode.  
frame#.depth_new.jpg: Depth map for visualization.  