import cv2 as cv
import mediapipe as mp
import time

from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions

from visualization import draw_manual, print_RSP_result

def classify_rps(hand_landmarks):

    tips = [4, 8, 12, 16, 20]
    pips = [2, 6, 10, 14, 18]

    fingers_open = []

    for tip, pip in zip(tips, pips):
        fingers_open.append(hand_landmarks[tip].y < hand_landmarks[pip].y)

    open_count = sum(fingers_open)

    if open_count <= 1:
        return 0          # Rock
    if open_count >= 4:
        return 1          # Paper
    if fingers_open[1] and fingers_open[2] and not fingers_open[3] and not fingers_open[4]:
        return 2          # Scissors

    return None


def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    options = HandLandmarkerOptions(
        base_options=BaseOptions(
            model_asset_path="hand_landmarker.task"
        ),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1
    )

    with HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=frame_rgb
            )

            timestamp = int(time.time() * 1000)

            detection_result = landmarker.detect_for_video(
                mp_image,
                timestamp
            )

            rps_result = None
            if detection_result.hand_landmarks:
                rps_result = classify_rps(detection_result.hand_landmarks[0])

            frame = draw_manual(frame, detection_result)
            frame = print_RSP_result(frame, rps_result)

            cv.imshow("RPS Game", frame)

            if cv.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
