import cv2
from ultralytics import YOLO

# 加载模型
model = YOLO(model="D:/pyProject/pythonProject/SmartPicker/servers/cv_server/my_detect/models/building_block.pt")

# 摄像头编号
camera_nu = "D:/pyProject/pythonProject/SmartPicker/servers/cv_server/my_detect/test_video/mp4/1.mp4"

# 打开摄像头
cap = cv2.VideoCapture(camera_nu)

class_list = list()
while cap.isOpened():
    # 获取图像
    res, frame = cap.read()
    # 如果读取成功
    if res:
        # 正向推理
        results = model(frame)
        c = results[0].boxes.cls
        for i in results[0].boxes.xywhn.cpu().numpy():
            if i[1] > 0.5 and i[1] < 0.9:
                for i in c:
                    class_list.append(int(i))
            else:
                #进行检测
                if len(class_list) >10:
                    classA = max(class_list,key=class_list.count)
                    class_list = list()
                    check = True
                    print(classA)
                else:
                    class_list = list()



        # print(class_list)
        # person_num = len(results[0])

        # 绘制结果
        annotated_frame = results[0].plot()
        # 显示图像
        cv2.imshow(winname="YOLOV8", mat=annotated_frame)

        # 按ESC退出
        if cv2.waitKey(1) == 27:
            break
# 释放连接
cap.release()
cv2.destroyAllWindows()
