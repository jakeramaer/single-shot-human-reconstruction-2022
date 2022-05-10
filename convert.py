import subprocess
import os
import cv2
import sys
import shutil


# Helper Functions ###############################

def video_to_image(path, frameRate=30):
    # converts .mp4 to .png
    if os.path.exists('png'):
        shutil.rmtree('png')
    os.mkdir('png')
    vidcap = cv2.VideoCapture(path)
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite("/content/technical_question/png/image"+str(count)+".png", image)
        return hasFrames
    sec = 0
    count=1
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + 1/frameRate
        sec = round(sec, 2)
        success = getFrame(sec)


# Main Function ##################################

print('Converting .mp4 to .png...') 
if len(sys.argv) > 2:
    video_to_image(sys.argv[1], int(sys.argv[2]))
else:
    video_to_image(sys.argv[1])

print('Launching ICON...')
os.chdir('/content/technical_question/ICON/apps')
subprocess.Popen("python infer.py -cfg ../configs/icon-filter.yaml -loop_smpl 100 -loop_cloth 0 -colab -gpu 0 -export_video -in_dir /content/technical_question/png".split())

