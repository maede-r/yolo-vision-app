import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


if not cap.isOpened():
    print("❌ وب‌کم باز نشد")
else:
    print("✅ وب‌کم باز شد، منتظر تصویر...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ دریافت تصویر انجام نشد")
        break

    cv2.imshow("تست وب‌کم - خروج با Q", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
