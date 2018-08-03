# Utility Scripts

import os
import json
import ffmpeg_utility as ff

path = 'D:\VISION\dataset'
# Save directories in a file
def name_folders(path=path):
    with open(path+"\/folders.txt", "w") as txt:
        [txt.write("%s\n" % name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
# Conta lle cartelle in una directory
def count_folders(path=path):
    return len([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])

# Return array with folders names
def folders_to_array(path=path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

def video_to_array(path=path,type=''):
    return [x for x in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))] if type in x and x.endswith('.mp4')]

def video_save_paths_from_array(array,txt_file,path=''):
    with open(path + txt_file, "a") as txt:
        for v in array:
            txt.write("\n%s frames: %s"% (v,ff.ffmpeg_count_frames(v)))

def get_mb_type_from_json_frames(file,test_path=''):
    with open(test_path+file) as f:
        data = json.load(f)
    frames_count = 0
    for frame in data["frames"]:
        if(frame["media_type"]=="video"):
            frames_count+=1
            row = ''+str(frame["coded_picture_number"])+':'+frame["pict_type"]
            print(row)
            with open(test_path+"frames_from_"+file+".txt", "a") as txt:
                txt.write("%s\n" % row)
    frames_indices = []
    frames_array = [None] * frames_count
    for frame in data["frames"]:
        if(frame["media_type"]=="video"):
            row = ''+str(frame["coded_picture_number"])+':'+frame["pict_type"]
            frames_array[frame["coded_picture_number"]]=row
    with open(test_path+"ordered_frames_from_"+file+".txt", "a") as txt:
        [txt.write("%s\n" % row) for row in frames_array]

def get_real_frames_order(filename):
    frames_indices = []
    with open(filename, 'r') as txt:
        frames = txt.readlines()
        for i in range(len(frames)):
            frame = (frames[i]).split(":")
            frames_indices.append(int(frame[0]))
    return frames_indices