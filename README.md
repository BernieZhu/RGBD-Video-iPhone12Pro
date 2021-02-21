# Record RGBD Video with iPhone 12 Pro

## Get the Application
[Record3D](https://record3d.app)

## Export and Share the Videos
Library - Export - r3d - Share  

## Process the Videos
python r3d_process.py \[options\]  
--path: Path to the folder that contains r3d files.  
--depth: Decode depth file and save depth image.  
--video: Save RGB and depth video.  
--quiet: Disable logs.  

## Resolutions
| Device | RGB | Depth |
|  :-:  |  :-:  |  :-:  |
| iPhone LiDAR | 720\*920 | 192\*256 |
| iPhone TrueDepth | 480\*640 | 480\*640 |
| RealSense | 480\*640 | 480\*640 |  

Be sure to modify the resolution in the code before you run it.  

## Structure  
*.mp4 is for visualization. Use the data in the folders.  
metadata: Binary file. K is the intrinsic matrix in order [fx, 0, 0, s, fy, 0, x0, y0, 1].  

color/frame#.jpg: RGB image  
depth/frame#.png: Depth image  

Folder: rgbd  
frame#.depth: Original depth (lzfse). The data is in float32 format. See load_depth(). Each value is the actual depth value in meters.  
frame#.conf: Confidence map for each frame. The size is the same as the depth map and for each pixel of the depth map it contains an uint8 number in the range 0-2, which suggest the confidence that the sensed LiDAR depth is "correct". In other words, it is a measure of depth data quality.  