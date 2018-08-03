import os
import datetime

def ffmpeg_cut_video(input,output,start,duration):
    #Original: ffmpeg -i movie.mp4 -ss 00:00:03 -t 00:00:08 -async 1 -strict -2 cut.mp4
    ffmpeg_command = 'ffmpeg -i '+input+' -ss '+str(datetime.timedelta(seconds=start))+' -t '+str(datetime.timedelta(seconds=duration))+' -async 1 -strict -2 '+output
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

def ffmpeg_cut_video_and_extract_frames(input,output,start,duration,filename="frame",outputframes_folder="frames",ext='bmp',second_ext='no'):
    #Original: ffmpeg -i movie.mp4 -ss 00:00:03 -t 00:00:08 -async 1 -strict -2 cut.mp4
    ffmpeg_command = 'ffmpeg -i '+input+' -ss '+str(datetime.timedelta(seconds=start))+' -t '+str(datetime.timedelta(seconds=duration))+' -async 1 -vsync 1 '+output
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

    # ffmpeg -i output.mp4 -ss 00:00:03 -t 00:00:05 -async 1 -strict -2 frame_%04d.jpg
    ffmpeg_command = 'ffmpeg -i ' + input +' -ss '+str(datetime.timedelta(seconds=start))+' -t '+str(datetime.timedelta(seconds=duration))+' ' + outputframes_folder + '/' + filename + '_%04d.' + ext
    print('execute ' + ffmpeg_command)
    os.system(ffmpeg_command)

    if(second_ext!='no'):
        ffmpeg_command = 'ffmpeg -i ' + input + ' -ss ' + str(datetime.timedelta(seconds=start)) + ' -t ' + str(
            datetime.timedelta(seconds=duration)) + ' ' + outputframes_folder + '/' + filename + '_%04d.' + second_ext
        print('execute ' + ffmpeg_command)
        os.system(ffmpeg_command)

def ffmpeg_concatenate_videos(inputs,output,clips):
    #Original: ffmpeg -f concat -safe 0 -i mylist.txt -c copy output
    #ffmpeg_command = 'ffmpeg -f concat -safe 0 -i '+txt+' -c copy '+output
    ffmpeg_command = 'ffmpeg '+inputs+' -filter_complex "[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n='+str(clips)+':v=1:a=1 [v] [a]" -map "[v]" -map "[a]" '+output+' -async 1 -vsync 1'
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

def ffmpeg_concatenate_videos_v2(cut_folder,output,clips):
    #Original: ffmpeg -i input0.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate0.ts
    #Original: ffmpeg -i input1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
    #Original: ffmpeg -i "concat:intermediate0.ts|intermediate1.ts" -c copy -bsf:a aac_adtstoasc output.mp4
    inputs_tmp = ''
    for i in range(clips):
        ffmpeg_command = 'ffmpeg -i '+cut_folder+'\\cut_'+str(i)+'.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate'+str(i)+'.ts'
        print('execute ' + ffmpeg_command)
        os.system(ffmpeg_command)
        inputs_tmp += 'intermediate'+str(i)+'.ts'
        if i != (clips-1) :
            inputs_tmp += '|'
    ffmpeg_command = 'ffmpeg -i "concat:'+inputs_tmp+'" -c copy -bsf:a aac_adtstoasc '+output
    print('execute ' + ffmpeg_command)
    os.system(ffmpeg_command)
    for i in range(clips):
        os.remove('intermediate'+str(i)+'.ts')



def ffmpeg_convert_to_2Bframe(input,output):
    #Original: ffmpeg -i input.mp4 -vcodec mpeg4 -bf 2 output.mp4
    ffmpeg_command = 'ffmpeg -i '+input+' -vcodec mpeg4 -g 15 -bf 2 '+output
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

def ffmpe_pad_to_resolution(x,y,input,output):
    #Original: ffmpeg -i input -vf "scale=-1:720,pad=1280:ih:(ow-iw)/2" output
    ffmpeg_command = 'ffmpeg -i '+input+' -vf "scale=-1:'+y+',pad='+x+':ih:(ow-iw)/2" '+output
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

def ffmpeg_extract_frames(input,filename="frame",output="frames",ext='bmp'):
    #Original: ffmpeg -i cut_0.mp4 $filename%03d.bmp
    os.system('mkdir -pv '+output)
    #ffmpeg_command = 'ffmpeg -i '+input+' -filter:v fps=fps='+str(fps)+' frames_'+input.replace(".mp4","")+'/'+input+'_frame%04d.'+ext
    ffmpeg_command = 'ffmpeg -i '+input+' '+output+'/'+filename+'_%04d.'+ext
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

def ffmpeg_create_video_with_mb_type(input,mb_type='I'):
    #Original: ffmpeg -i input.mp4 -vf select='eq(pict_type\,I)' i_frames.mp4
    ffmpeg_command = 'ffmpeg -i '+input+' -vf select="eq(pict_type\,'+mb_type+')" '+mb_type+'_frames.mp4'
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

def ffmpeg_extract_frames_with_frame_type(input,mb_type='I',ext='bmp'):
    #Original: ffmpeg -i input.mp4 -vf select='eq(pict_type\,I)' i_frames.mp4
    ffmpeg_create_video_with_mb_type(input,mb_type)
    os.system('mkdir '+mb_type+'_frames_'+input.replace(".mp4",""))
    ffmpeg_command = 'ffmpeg -i '+mb_type+'_frames.mp4 -vf mpdecimate,setpts=N/FRAME_RATE/TB '+mb_type+'_frames_'+input.replace(".mp4","")+'/'+mb_type+'_frame%03d.'+ext
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

def ffmpeg_extract_mb_type_for_frame(input,txt='mb_frames_report.txt'):
    #Original: ffmpeg -debug mb_type -thread_type none -i cut_0.mp4 out.mp4 2>prova.txt
    ffmpeg_command = 'ffmpeg -debug mb_type  -thread_type none -i '+input+' out.mp4 2>'+txt
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)
    os.remove('out.mp4')

def ffmpeg_create_frames_report(input,output):
    #Original: ffprobe input.mp4 -show_frames -print_format json -loglevel quiet >> input.json
    ffmpeg_command = 'ffprobe '+input+' -show_frames -print_format json -loglevel quiet >> '+output
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)

def ffmpeg_count_frames(input):
    #Original: ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 input.mkv
    ffmpeg_command = 'ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1  '+input+' >> tmp_frames_count.txt'
    print('execute '+ffmpeg_command)
    os.system(ffmpeg_command)
    file = open('tmp_frames_count.txt', 'r')
    frames_count = str(file.read())
    file.close()
    os.remove('tmp_frames_count.txt')
    return frames_count
