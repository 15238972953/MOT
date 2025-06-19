# 在视频中拖动鼠标左键划线，右键点击线段可删除已有划线

import cv2
import math

# 全局变量
drawing = False
point1 = None
point2 = None
lines = []  # 每条线为 (frame_number, pt1, pt2)
frame_number = 0
current_frame = None
temp_line = None
min_drag_dist = 5  # 最小拖动像素距离
delete_thresh = 10  # 点击删除线的像素阈值

def point_to_line_distance(pt, line_start, line_end):
    """计算点 pt 到线段的最小距离"""
    x0, y0 = pt
    x1, y1 = line_start
    x2, y2 = line_end

    A = x0 - x1
    B = y0 - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D
    param = dot / len_sq if len_sq != 0 else -1

    if param < 0:
        xx, yy = x1, y1
    elif param > 1:
        xx, yy = x2, y2
    else:
        xx = x1 + param * C
        yy = y1 + param * D

    dx = x0 - xx
    dy = y0 - yy
    return math.hypot(dx, dy)

def draw_line(event, x, y, flags, param):
    global point1, point2, drawing, temp_line, lines

    if event == cv2.EVENT_LBUTTONDOWN:
        point1 = (x, y)
        drawing = True
        temp_line = None

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        temp_line = (point1, (x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        point2 = (x, y)
        drawing = False
        if point1 and point2:
            dx = abs(point2[0] - point1[0])
            dy = abs(point2[1] - point1[1])
            if dx >= min_drag_dist or dy >= min_drag_dist:
                lines.append((frame_number, point1, point2))
            temp_line = None

    elif event == cv2.EVENT_RBUTTONDOWN:
        # 右键点击尝试删除最近的线
        click_point = (x, y)
        for i, (fid, p1, p2) in enumerate(lines):
            dist = point_to_line_distance(click_point, p1, p2)
            if dist < delete_thresh:
                print(f"🗑 删除线段：帧{fid}, {p1}->{p2} (点击点距离: {dist:.1f})")
                lines.pop(i)
                break  # 删除一条后退出

def main():
    global frame_number, current_frame

    cap = cv2.VideoCapture("inference\\input\\1.mp4")  # 改为0使用摄像头

    if not cap.isOpened():
        print("❌ 无法打开视频")
        return

    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", draw_line)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_number += 1
        current_frame = frame.copy()

        # 绘制已有线条
        for fid, p1, p2 in lines:
            if fid <= frame_number:
                cv2.line(current_frame, p1, p2, (0, 0, 255), 2)

        # 正在绘制的线条
        if drawing and temp_line:
            cv2.line(current_frame, temp_line[0], temp_line[1], (0, 255, 0), 2)

        cv2.imshow("Video", current_frame)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
