import cv2
import os


def convert_video_to_frames(video_path, frame_path):

    videoCapture = cv2.VideoCapture(video_path)
    second = 0
    frameRate = 1  # 1 means 1 frame per second (1 frame = 1 second and 0.5 means 2 frames per 1 second)
    count = 0

    success, image = videoCapture.read(second)
    while success:
        count = count + 1
        second = second + frameRate
        second = round(second, 2)

        videoCapture.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
        hasFrames, image = videoCapture.read()
        if hasFrames:
            cv2.imwrite(os.path.join(frame_path, "frame%d.jpg" % count), image)  # save frame as JPEG file

        success = hasFrames
