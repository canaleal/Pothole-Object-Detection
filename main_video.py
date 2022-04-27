import cv2
import os


def convertVideoToFrames(video_path, frame_path):
    output_video = f'{video_path}/video.mp4'
    vidcap = cv2.VideoCapture(output_video)
    sec = 0
    frameRate = 1  # //it will capture image in each 0.5 second
    count = 0
    success, image = vidcap.read(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)

        vidcap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        hasFrames, image = vidcap.read()
        if hasFrames:
            cv2.imwrite(os.path.join(frame_path, "frame%d.jpg" % count), image)  # save frame as JPEG file

        success = hasFrames
