# NYCU Campus Food Finder

陽明交通大學光復校區學生餐廳查詢系統。專案把餐廳 CSV 資料整理成可依區域、店家、關鍵字、預算與價格排序的查詢工具，並提供適合面試展示的靜態作品頁。

!\[NYCU Campus Food Finder 主視覺](docs/food-finder-hero.webp)

## 

## 專案摘要

|指標|資料|
|-|-:|
|餐廳區域|4|
|店家|13|
|餐點|57|
|價格範圍|NT$30–229|

## 

## 核心功能

* 搜尋餐點、店家與餐廳區域
* 餐廳區域與店家連動篩選
* 最高預算篩選
* 依價格由低到高或由高到低排序
* API 健康檢查與錯誤回應
* 手機與桌面版介面

## 

## 工程處理重點

1. **CSV 相容性**：自動處理 UTF-8 BOM、不間斷空白與舊檔名。
2. **資料型別**：移除價格中的 `$` 與千分位，再轉為整數。
3. **欄位穩定性**：API 固定輸出五個欄位，避免額外 index 欄造成顯示錯位。
4. **輸入安全**：搜尋使用純文字比對，前端輸出進行 HTML escape。
5. **可觀測性**：`/api/health` 回報服務狀態與餐點筆數。

## 

## 專案結構



```text
.
├── app.py                    # Flask API 與資料處理
├── restaurant\_data.csv       # 餐點資料
├── requirements.txt
├── templates/index.html      # Flask 版介面
├── static/                   # Flask 版樣式與圖示
└── docs/                     # GitHub Pages 靜態展示版
```

## 

## 本機執行 Flask 版本



```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

macOS / Linux：

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

開啟 `http://127.0.0.1:5000`。健康檢查位於 `http://127.0.0.1:5000/api/health`。

## 

## 啟用 GitHub Pages 展示

1. 將本資料夾內容推送到 GitHub Repository。
2. 進入 Repository 的 **Settings → Pages**。
3. 在 **Build and deployment** 選擇 **Deploy from a branch**。
4. 選擇主要分支與 `/docs` 資料夾後儲存。

GitHub Pages 版本會直接讀取 `docs/restaurant\_data.csv`，不需要執行 Python 伺服器。

## 

## 資料說明

本專案使用隨附 CSV 作為展示資料。餐點、價格與營業時間不代表即時狀態；正式使用前應重新確認來源與更新日期。

## 

## 作者

Jamie Hung  
Engineering Portfolio · Python / Flask / Pandas

