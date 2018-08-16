# Some video database:
# - https://media.xiph.org/video/derf (1080dp)

import os
import random
import datetime
import video_scripts as vs
import ffmpeg_utility as ff
import numpy as np
path = 'D:\dataset' # Path of your videos
log_date= datetime.datetime.now().strftime ("%Y%m%d%H%M%S")
log = log_date+'_log' # Create a log
if(not os.path.isfile(path+'\/folders.txt')):
    vs.name_folders(path)

#### OPTIONS #####
video_duration = 12 # secondi
video_cameras = 2 #max 11
clips_per_camera = 3 # max 3
clips_total = video_cameras * clips_per_camera
clip_duration = video_duration / (video_cameras*clips_per_camera)

# Frame extraction
frames_ext = 'jpg'
second_frames_ext = 'no' # type 'no' for extract only in frames_ext extension or specify another one( es. 'bmp')

# select video_cameras randomly
folders = vs.folders_to_array(path)
cameras = random.sample(set(folders), video_cameras)

os.system('mkdir '+log.replace('log','test'))

with open(log.replace('log','test')+'/'+log+".txt", "w") as txt:
    txt.write("Video duration: %s\nTotal clips: %s (%s per camera, %s cameras)\nCameras selected: %s\n\n"
              % (video_duration,clips_total,clips_per_camera ,video_cameras,cameras))

videos = {}
for camera in cameras:
    all_videos = (vs.video_to_array(path+'\/'+camera))
    camera_videos_selected = random.sample(set([camera+'/'+x for x in all_videos]), clips_per_camera)
    videos[camera] = camera_videos_selected

with open(log.replace('log','test')+'/'+log+".txt", "a") as txt:
    txt.write("Selected videos: %s\n\n" % (videos))

os.system('mkdir '+log.replace('log','test')+'\\'+'cuts_tmp')

videos_selected=[]
k=-1
for i in range(video_cameras):
    [videos_selected.append(x) for x in list(videos.values())[i]]
    for x in list(videos.values())[i]:
        k+=1
        with open(log.replace('log','test')+'/'+log+".txt", "a") as txt:
            #txt.write("Clip %s taken from %s\n"% (i*2+list(videos.values())[i].index(x) ,x))
            txt.write("Clip %s taken from %s\n"% (k ,x))
            # print("i k ",i,' ',k)
        os.system('mkdir -pv ' + log.replace('log', 'test') + '\\' + log_date + '_frames')
        ff.ffmpeg_cut_video_and_extract_frames(path+'/'+x, log.replace('log','test')+'/cuts_tmp/'+'cut_'+str(k)+'.mp4', clip_duration*(list(videos.values())[i].index(x)),clip_duration, str(k)+'_frame', log.replace('log', 'test') + '\\' + log_date + '_frames', frames_ext,second_frames_ext)
videos_shuffled_indices=list(range(clips_total))
random.shuffle(videos_shuffled_indices)
print(videos_shuffled_indices)
########## Calcolo wanted_matrix ##########
clustering_matrix = []
with open(log.replace('log', 'test') + '/' + log + ".txt", "a") as txt:
    txt.write("\nWanted Clustering_matrix:\n")
    print('Wanted Clustering_matrix:')
    k_range=[]
    for i in range(clips_total):
        k=0
        for c in range(video_cameras):
            k_range=list(range(k, k + clips_per_camera))
            if videos_shuffled_indices[i] in k_range:break
            else:k=k+clips_per_camera
        k_indices = [videos_shuffled_indices.index(x) for x in k_range]
        k_row = np.zeros(clips_total,int)
        k_row[k_indices]=1
        print(k_row)
        clustering_matrix.append(k_row)
        txt.write("%s\n" % k_row)
##############################################
vs.video_save_paths_from_array([log.replace('log','test')+'\\cuts_tmp\\cut_'+str(i)+'.mp4' for i in videos_shuffled_indices],log.replace('log', 'test') + '/' + log + ".txt")
inputs=''
frames_extracted = 0
for i in videos_shuffled_indices:
    video_i = log.replace('log','test')+'\\cuts_tmp\\cut_'+str(i)+'.mp4'
    inputs = inputs+' -i '+video_i
    #estraggo frames dai cut e li rinomino perchè siano coerenti
    files_i = [x for x in os.listdir(log.replace('log', 'test') + '\\' + log_date + '_frames') if os.path.isfile(os.path.join(log.replace('log', 'test') + '\\' + log_date + '_frames', x)) and str(i)+'_frame' in x and frames_ext in x]
    frames_i=len(files_i)
    k=0
    for frame_i in range(frames_extracted+1,frames_extracted+frames_i+1):
        os.rename(log.replace('log', 'test') + '\\' + log_date + '_frames\\'+files_i[k], (log.replace('log', 'test') + '\\' + log_date + '_frames\\frame_%04d.'+frames_ext) % frame_i)
        k=k+1
    if second_frames_ext!='no':
        files_i = [x for x in os.listdir(log.replace('log', 'test') + '\\' + log_date + '_frames') if
                   os.path.isfile(os.path.join(log.replace('log', 'test') + '\\' + log_date + '_frames', x)) and str(
                       i) + '_frame' in x and second_frames_ext in x]
        frames_i = len(files_i)
        k = 0
        for frame_i in range(frames_extracted + 1, frames_extracted + frames_i + 1):
            os.rename(log.replace('log', 'test') + '\\' + log_date + '_frames\\' + files_i[k],
                      (log.replace('log', 'test') + '\\' + log_date + '_frames\\frame_%04d.' + second_frames_ext) % frame_i)
            k = k + 1
    frames_extracted = frames_extracted+frames_i
print(inputs)
out_path = log.replace('log','test')+'\\'+log.replace("log","")+'output.mp4'
ff.ffmpeg_concatenate_videos(inputs,out_path,clips_total)