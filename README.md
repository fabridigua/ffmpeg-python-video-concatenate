# ffmpeg-python-video-concatenate

Purpose
------
Create video concatenating scenes coming from different video.

Languages and libraries used
------
+ __Python 3.6__ for scripting.
+ __ffmpeg__ for video editing.
+ __numpy__ 

Files
------
This little project consists in three files:
1. `ffmpeg_utility.py`: contains the calls to the ffmpeg function
2. `video_scripts.py`: just some utility functions
3. `ffmpeg_video_maker.py`: the real script for create videos

Usage
------

- Open `ffmpeg_video_maker.py`.
- Define the `path` variable 
> __Important note__: The script is thought for concatenating video coming from different camera, so the video files have to be in different folder basing on the original camera. You can simply change this behaviour editing `ffmpeg_video_maker.py`.
- Personalize the video in the "OPTIONS" section in the file.
- Run the script!

Result
------
In a folder naming `CURRENT_TIMESTAMP_test` will be saved:
- the generated a video `CURRENT_TIMESTAMP_output.mp4` basing on the options you setted
- a log file with some informations abut the video
- a folder `cuts_tmp` with the scenes extracted
- a folder `CURRENT_TIMESTAMP_frames` with the video frames