import cv2
import os

def convert_video_to_frames(video_path, save_path):

    # Load the video from the given path
    videoCapture = cv2.VideoCapture(video_path)
    
    # 1 means 1 frame per second (1 frame = 1 second and 0.5 means 2 frames per 1 second)
    fps = 1 
    second = 0
    count = 0

    # Read each frame from the video and save the frame in the save_path
    success, image = videoCapture.read(second)
    while success:
        count = count + 1
        second = second + fps
        second = round(second, 2)

        videoCapture.set(cv2.CAP_PROP_POS_MSEC, second * 1000)
        hasFrames, image = videoCapture.read()
        if hasFrames:
            
            # Add padding to the frame so the frames are saved in ascending order
            paddedFrameCount = str(count).zfill(10)
            cv2.imwrite(os.path.join(save_path, "frame%s.jpg" % paddedFrameCount), image)

        success = hasFrames
