#Q1
* Coin Detection
  * 以下是程式碼

```pythonimport cv2
import numpy as np

# 1. 讀取影片
cap = cv2.VideoCapture('coin.mp4')

# --- 準備影片寫入器 (這段是存檔關鍵) ---
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
# 定義編碼並建立 VideoWriter 物件
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # 2. 影像處理
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)

    # 3. 找輪廓並標註
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 2000 < area < 50000: 
            x, y, w, h = cv2.boundingRect(cnt)
            # 畫框與文字
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"({x},{y})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    # 4. 顯示與存檔
    cv2.imshow('Result', frame)
    out.write(frame) # 將這一幀畫面寫入影片檔案

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. 釋放資源 (這步沒做，影片會毀損打不開)
cap.release()
out.release()
cv2.destroyAllWindows()
print("偵測完成！影片已存為 output.mp4")
```
