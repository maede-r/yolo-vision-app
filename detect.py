import cv2
from ultralytics import YOLO
import pyttsx3

# مدل YOLOv8
model = YOLO("yolov8n.pt")

# تبدیل متن به صدا
engine = pyttsx3.init()

# باز کردن وب‌کم
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("✅ آماده‌ست! دکمه S = عکس و تشخیص | Q = خروج")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ تصویر دریافت نشد")
        break

    cv2.imshow("تصویر زنده (s برای عکس)", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        print("📸 عکس گرفته شد. در حال شناسایی...")

        results = model(frame)
        names = results[0].names
        boxes = results[0].boxes

        cls = boxes.cls.tolist()
        cords = boxes.xyxy.tolist()  # مختصات جعبه‌ها: xmin, ymin, xmax, ymax

        detected_labels = set()
        for i in range(len(cls)):
            label = names[int(cls[i])]
            detected_labels.add(label)

            # مختصات جعبه
            x1, y1, x2, y2 = map(int, cords[i])
            # رسم جعبه و برچسب روی تصویر
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # گفتن نام اشیاء
        for label in detected_labels:
            sentence = f"{label} detected"
            print("🔊", sentence)
            engine.say(sentence)
        engine.runAndWait()

        # ذخیره تصویر نهایی با جعبه‌ها
        cv2.imwrite("detected.jpg", frame)
        print("✅ تصویر با جعبه‌ها ذخیره شد (detected.jpg)")

        # نمایش تصویر نهایی
        cv2.imshow("تصویر شناسایی‌شده", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  # همه پنجره‌ها بسته می‌شوند

    elif key == ord('q'):
        print("👋 خروج از برنامه")
        break

cap.release()
cv2.destroyAllWindows()  # بستن تمام پنجره‌ها
