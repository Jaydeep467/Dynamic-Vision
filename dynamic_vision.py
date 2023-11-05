from typing import List
import cv2
import numpy as np
from imageai.Detection import VideoObjectDetection
import os


class DynamicVision:
    def __init__(self) -> None:
        self.input_folder_path = "input_videos"
        self.output_folder_path = "output_videos"
        self.model_folder_path = "models"
        self.model = None

    def capture_video(self, file_name: str) -> List[np.ndarray]:
        video_frames = []
        cap = cv2.VideoCapture(os.path.join(self.input_folder_path, file_name))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            video_frames.append(frame)

        cap.release()
        cv2.destroyAllWindows()

        return video_frames

    def detect_objects(self, input_video_path: str):
        if not self.model:
            raise Exception("Model not set. Set model using obj.set_model()")
        vid_obj_detect = VideoObjectDetection()
        vid_obj_detect.setModelTypeAsYOLOv3()
        vid_obj_detect.setModelPath(os.path.join(self.model_folder_path, self.model))
        vid_obj_detect.loadModel()
        detected_vid_obj = vid_obj_detect.detectObjectsFromVideo(
            input_file_path=os.path.join(self.input_folder_path, input_video_path),
            output_file_path=os.path.join(
                self.output_folder_path, f"{input_video_path[:-4]}_output"
            ),
            frames_per_second=15,
            log_progress=True,
            return_detected_frame=True,
        )

    def set_model(self, model: str):
        if not os.path.exists(os.path.join(self.model_folder_path, model)):
            raise Exception("Model not present in directory")

        self.model = model