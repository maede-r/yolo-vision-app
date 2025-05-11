// تابع برای فعال کردن وب‌کم و گرفتن تصویر
function startCamera() {
    const videoElement = document.getElementById("videoElement");

    // درخواست دسترسی به وب‌کم
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            videoElement.srcObject = stream;
        })
        .catch(function (error) {
            console.error("Error accessing webcam: ", error);
        });
}

// تابع برای گرفتن عکس از وب‌کم و ارسال آن به سرور
function captureAndSendImage() {
    const videoElement = document.getElementById("videoElement");
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    // تنظیم اندازه کانواس به اندازه تصویر وب‌کم
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    // رسم تصویر وب‌کم روی کانواس
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // تبدیل تصویر به فرمت Base64
    const imageData = canvas.toDataURL("image/jpeg");

    // ارسال تصویر به سرور
    fetch("/detect", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        // نمایش تصویر شناسایی‌شده در صفحه
        const resultImage = document.getElementById("resultImage");
        resultImage.src = `data:image/jpeg;base64,${data.image}`;

        // نمایش برچسب‌های شناسایی‌شده
        const labelsElement = document.getElementById("labels");
        labelsElement.textContent = "Objects detected: " + data.labels.join(", ");

        // پخش صدا
        const speech = data.speech;
        const utterance = new SpeechSynthesisUtterance(speech);
        speechSynthesis.speak(utterance);
    })
    .catch(error => {
        console.error("Error sending image to server: ", error);
    });
}

// فعال‌سازی وب‌کم و شروع کار
document.addEventListener("DOMContentLoaded", function() {
    startCamera();

    // وقتی کاربر دکمه "Capture" را می‌زند، تصویر گرفته می‌شود و به سرور ارسال می‌شود
    const captureButton = document.getElementById("captureButton");
    captureButton.addEventListener("click", captureAndSendImage);
});
