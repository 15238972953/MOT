import cv2

# 全局变量
drawing = False
point1 = None
point2 = None
paused = False
lines = []  # 存储所有划线：((frame_number, pt1, pt2))
frame_number = 0
current_frame = None  # 当前帧，用于暂停时显示
base_frame = None     # 当前帧基础图像（用于实时画线）

def draw_line(event, x, y, flags, param):
    global point1, point2, drawing, current_frame, base_frame, lines

    if not paused:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        point1 = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        # 实时显示正在画的线
        temp_frame = base_frame.copy()
        cv2.line(temp_frame, point1, (x, y), (0, 255, 0), 2)
        # 加上已有线
        for fid, p1, p2 in lines:
            cv2.line(temp_frame, p1, p2, (0, 0, 255), 2)
        cv2.imshow("Video", temp_frame)

    elif event == cv2.EVENT_LBUTTONUP:
        point2 = (x, y)
        drawing = False
        if point1 and point2:
            lines.append((frame_number, point1, point2))
            # 更新 base_frame 并刷新窗口
            cv2.line(base_frame, point1, point2, (0, 0, 255), 2)
            current_frame = base_frame.copy()
            cv2.imshow("Video", current_frame)

def main():
    global paused, frame_number, current_frame, base_frame

    cap = cv2.VideoCapture("inference\\input\\1.mp4")  # 可改为 0 使用摄像头

    if not cap.isOpened():
        print("❌ 无法打开视频")
        return

    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", draw_line)

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            frame_number += 1

            # 在当前帧上画所有已有线条
            for fid, p1, p2 in lines:
                if fid <= frame_number:
                    cv2.line(frame, p1, p2, (0, 0, 255), 2)

            base_frame = frame.copy()
            current_frame = frame.copy()
            cv2.imshow("Video", frame)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('p'):  # 暂停/继续
            paused = not paused
            if paused:
                print("⏸ 视频暂停，可画线。")
                cv2.imshow("Video", current_frame)
            else:
                print("▶ 继续播放")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
