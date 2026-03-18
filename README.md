# Q1

# 硬幣偵測與影像處理專案 (Coin Detection Project)

 目標是透過 **Python (OpenCV)** 與 **MATLAB** ，對影片中硬幣的即時偵測、定位與標註。

---

##  開發環境與技術棧
* **語言**: Python , MATLAB 
* **開發工具**: VS Code, MATLAB Online

---

##  演算法邏輯 (Algorithm Workflow)
不論是 Python 或 MATLAB 版本，核心邏輯均遵循以下影像處理管線：

1. **影像預處理**: 將原始 RGB 幀轉為**灰階 (Grayscale)**，並使用**高斯模糊 (Gaussian Blur)** 去除環境雜訊。
2. **二值化處理 (Binarization)**: 
   - 設定亮度門檻（門檻值約 0.45 - 0.5 之間）將硬幣與背景分離。
   - 針對反光問題調整門檻，確保暗處硬幣也能被正確切割。
3. **連通域分析與特徵提取**:
   - 偵測閉合輪廓。
   - **面積過濾 (Area Filtering)**：設定門檻（如 > 10,000 像素）排除鍵盤按鍵或細小雜訊。
4. **即時標註**: 提取目標物的中心點 (Centroid) 與邊界框 (Bounding Box)，並即時繪製紅框與座標。

---

##  實作成果展示

### 1. Python 成果
```
* **實作檔案**: ```pythonimport cv2
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
* **預覽**: 

### 2. MATLAB 實作成果
* **實作檔案**: `detect_coins.m`
* **說明**: 透過 `regionprops` 進行精準的幾何矩分析。針對 MATLAB Online 網頁環境進行優化，使用 `insertShape` 直接操作影像矩陣以提升穩定性。
* **預覽**: `output_matlab.avi`

---

##  參數調整心得
在實作過程中，針對環境光線進行了多次參數優化：
* **門檻值 (Threshold)**: 從初始的 0.7 降至 **0.45**，成功解決了硬幣亮度不足導致漏偵測的問題。
* **面積過濾**: 將下限提升至 **10,000**，有效過濾掉背景中亮度較高的鍵盤字母干擾。

---
