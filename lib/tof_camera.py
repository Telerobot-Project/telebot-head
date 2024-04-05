import sys
import cv2
import numpy as np
import ArduCamDepthCamera as ac

MAX_DISTANCE = 4

class ToFCamera:
    def __init__(self) -> None:
        self.cam = ac.ArducamCamera()

        if self.cam.init(ac.TOFConnect.CSI, ac.TOFOutput.DEPTH, 0) != 0:
            print("[TOF CAMERA] Initialization failed")
        elif self.cam.start() != 0:
            print("[TOF CAMERA] Failed to start camera")
        else:
            print("[TOF CAMERA] Started")

    def read(self):
        frame = self.cam.requestFrame(200)
        if frame != None:
            self.depth_buf = frame.getDepthData()
            self.amplitude_buf = frame.getAmplitudeData()
            self.amplitude_buf[self.amplitude_buf < 0] = 0
            self.amplitude_buf[self.amplitude_buf > 255] = 255
            self.cam.releaseFrame(frame)

            self.frame = self.process_frame()


    def process_frame(self) -> np.ndarray:
        self.depth_buf = np.nan_to_num(self.depth_buf)
        self.amplitude_buf[self.amplitude_buf <= 30] = 0
        self.amplitude_buf[self.amplitude_buf > 30] = 255
        self.depth_buf = (1 - (self.depth_buf/2)) * 255
        self.depth_buf = np.clip(self.depth_buf, 0, 255)
        self.result_frame = self.depth_buf.astype(
            np.uint8) & self.amplitude_buf.astype(np.uint8)
        return self.result_frame


def process_frame(depth_buf: np.ndarray, amplitude_buf: np.ndarray) -> np.ndarray:

    depth_buf = np.nan_to_num(depth_buf)

    amplitude_buf[amplitude_buf <= 30] = 0
    amplitude_buf[amplitude_buf > 30] = 255

    depth_buf = (1 - (depth_buf/2)) * 255
    depth_buf = np.clip(depth_buf, 0, 255)
    result_frame = depth_buf.astype(np.uint8) & amplitude_buf.astype(np.uint8)
    return result_frame


if __name__ == "__main__":
    cam = ac.ArducamCamera()

    if cam.init(ac.TOFConnect.CSI, ac.TOFOutput.DEPTH, 0) != 0:
        print("initialization failed")
    if cam.start() != 0:
        print("Failed to start camera")
    
    cam.setControl(ac.TOFControl.RANG, MAX_DISTANCE)

    while True:
        frame = cam.requestFrame(200)
        if frame != None:
            depth_buf = frame.getDepthData()
            amplitude_buf = frame.getAmplitudeData()
            amplitude_buf[amplitude_buf < 0] = 0
            amplitude_buf[amplitude_buf > 255] = 255
            cam.releaseFrame(frame)

            cv2.imshow("amplitude", amplitude_buf.astype(np.uint8))

            result_image = process_frame(depth_buf, amplitude_buf)
            result_image = cv2.applyColorMap(result_image, cv2.COLORMAP_JET)
            cv2.imshow("preview", result_image)

            key = cv2.waitKey(1)
            if key == ord("q"):
                exit_ = True
                cam.stop()
                sys.exit(0)
