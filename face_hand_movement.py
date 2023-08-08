import cv2
import mediapipe as mp
# for calculating distance between two points
import math
# for calculating nervousness
import time

body_language_nervousness = ""


def face_hand_movement(image_path):
    global body_language_nervousness

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    nose_x, nose_y = 0, 0
    rh_x, rh_y = 2000, 0
    lh_x, lh_y = 0, 2000
    nervous_count = 0
    # For webcam input:
    start = time.time()
    image = cv2.imread(image_path)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        frame = cv2.resize(image, (512, 256))
        # To improve performance, optionally mark the frame as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)

        # Draw the pose annotation on the frame.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = frame.shape
                if id in [0, 19, 20]:
                    if id == 0:
                        nose_x, nose_y = lm.x, lm.y
                        nose_x, nose_y = int(nose_x * w), int(nose_y * h)
                        # print("nose coordinates: ({}, {})".format(nose_x, nose_y))
                        nose_list = [nose_x, nose_y]
                        cv2.circle(frame, (nose_x, nose_y), 10, (255, 0, 0), cv2.FILLED)
                    elif id == 19:
                        rh_x, rh_y = lm.x, lm.y
                        rh_x, rh_y = int(rh_x * w), int(rh_y * h)
                        # print("right hand coordinates: ({}, {})".format(rh_x, rh_y))
                        rh_list = [rh_x, rh_y]
                        cv2.circle(frame, (rh_x, rh_y), 10, (255, 0, 0), cv2.FILLED)
                    elif id == 20:
                        lh_x, lh_y = lm.x, lm.y
                        lh_x, lh_y = int(lh_x * w), int(lh_y * h)
                        # print("left hand coordinates: ({}, {})".format(lh_x, lh_y))
                        lh_list = [lh_x, lh_y]
                        cv2.circle(frame, (lh_x, lh_y), 10, (255, 0, 0), cv2.FILLED)

            cv2.line(frame, (nose_x, nose_y), (rh_x, rh_y), (0, 255, 0), 2)
            cv2.line(frame, (nose_x, nose_y), (lh_x, lh_y), (0, 255, 0), 2)
            cv2.line(frame, (rh_x, rh_y), (lh_x, lh_y), (0, 255, 0), 2)
            nose_rh_length = math.hypot(nose_x - rh_x, nose_y - rh_y)
            nose_lh_length = math.hypot(nose_x - lh_x, nose_y - lh_y)
            rh_lh_length = math.hypot(rh_x - lh_x, rh_y - lh_y)
            if (nose_rh_length < 120 or nose_lh_length < 120 or rh_lh_length < 120):
                cv2.circle(frame, (nose_x, nose_y), 20, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (rh_x, rh_y), 20, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (lh_x, lh_y), 20, (0, 255, 0), cv2.FILLED)
                nervous_count = nervous_count + 1
                # print(nervous_count)

        # Flip the frame horizontally for a selfie-view display.
        #cv2.imshow('MediaPipe Pose', cv2.flip(frame, 1))
        #cv2.waitKey(0)

    if nervous_count > 0:
        body_language_nervousness = "True"
        #print("nervous")
        return 1
    else:
        body_language_nervousness = "False"
        #print("neutral")
        return 0

def main():
    image_path = r"C:\Users\Pictures\Camera Roll\WIN_20230518_13_45_36_Pro.jpg"
    print(face_hand_movement(image_path))

if __name__ == "__main__":
    main()