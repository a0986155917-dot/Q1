import cv2
import numpy as np

cap = cv2.VideoCapture('coin.mp4') 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # 1. 轉灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. 稍微模糊，消除鍵盤上的文字雜訊
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 3. 強制二值化 (調整 100 這個數字：越低會抓到越多東西，越高越嚴格)
    # 因為硬幣比背景亮，所以我們用 cv2.THRESH_BINARY
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

    # 4. 尋找輪廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # 5. 降低面積門檻 (從 1000 改成 200)，避免漏掉較小的硬幣
        if 2000 < area < 50000: 
            x, y, w, h = cv2.boundingRect(cnt)
            # 畫框與文字
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"({x},{y})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    # 顯示「黑白圖」幫你除錯 (看到這個你就知道電腦有沒有抓到圓形)
    cv2.imshow('Binary View (Thresh)', thresh)
    cv2.imshow('Result', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()