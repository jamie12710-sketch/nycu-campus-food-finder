# NYCU Campus Food Finder｜午餐吃什麼？

### Python Data Processing · Debugging · REST API Engineering Portfolio

以陽明交通大學光復校區學生餐廳資料為題，使用 **Python、Pandas、Flask、JavaScript** 
建立可互動的餐點資料查詢系統。

此專案重點不只是完成搜尋介面，而是將原始 CSV 資料經過 **Data Cleaning、Data Validation、Exception Handling 與 Debugging**，建立可搜尋、篩選、排序及驗證的資料處理流程。

> **Engineering Focus:** Python · Pandas · Flask · Data Cleaning ·
> Data Validation · Debugging · REST API

![NYCU Campus Food Finder 主視覺](docs/food-finder-hero.webp)

---

# 1. Overview｜專案概述

本專案包含兩種不同用途的實作：

### 🌐 Interactive Demo — GitHub Pages

**Interactive Demo:** GitHub Pages 靜態展示版，
以 JavaScript 載入 CSV 並執行搜尋、篩選與排序。

用途：

* 提供面試官直接操作
* 不需安裝 Python
* 可立即測試搜尋、篩選、預算與排序功能

### ⚙️ Backend Implementation — Flask

**Backend Implementation:** Repository 同時包含 Python / Flask / Pandas 版本，
實作 REST API、資料驗證、錯誤處理與 Health Check。

用途：

* CSV Data Cleaning
* Required Column Validation
* Data Type Conversion
* Input Validation
* REST API
* Exception Handling
* API Health Check

> **Architecture Note**
>
> GitHub Pages Demo 與 Flask Backend 為兩種不同執行方式。
>
> GitHub Pages 使用 **JavaScript 直接載入 CSV** 完成互動查詢；
> Flask 版本則使用 **Python + Pandas 處理資料並透過 REST API 提供結果**。
>
> 因此 GitHub Pages Demo 不會直接執行 Flask Backend。

---

# 2. Live Demo｜互動展示

GitHub Pages 版本設計為免安裝的互動展示環境。

使用者可以直接操作：

* 🔍 餐點關鍵字搜尋
* 📍 餐廳區域篩選
* 🏪 店家篩選
* 💰 最高預算篩選
* ↕️ 價格排序
* 🔄 清除搜尋條件
* 📱 Desktop / Mobile Interface

### Demo Data Flow

```text
GitHub Pages
      │
      ▼
HTML / CSS / JavaScript
      │
      ▼
restaurant_data.csv
      │
      ▼
Parse / Normalize
      │
      ▼
Search / Filter / Sort
      │
      ▼
Interactive Results
```

### Backend Data Flow

```text
restaurant_data.csv
        │
        ▼
     Python
        │
        ▼
     Pandas
        │
        ├── Data Cleaning
        ├── Data Validation
        ├── Type Conversion
        └── Invalid Data Handling
        │
        ▼
      Flask
        │
        ▼
     REST API
   ┌────┼─────┐
   ▼    ▼     ▼
 Search Shops Health
   │    │     │
   └────┴─────┘
        │
        ▼
    JSON Response
```

---

# 3. Architecture｜系統架構

```text
nycu-campus-food-finder/
│
├── docs/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── restaurant_data.csv
│
│   GitHub Pages Interactive Demo
│
├── templates/
│   └── index.html
│
├── static/
│   └── Flask static assets
│
├── app.py
│   ├── CSV Loading
│   ├── Data Cleaning
│   ├── Data Validation
│   ├── Search / Filter
│   ├── REST API
│   └── Health Check
│
├── restaurant_data.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Tech Stack

| Category         | Technology              |
| ---------------- | ----------------------- |
| Programming      | Python                  |
| Data Processing  | Pandas                  |
| Backend          | Flask                   |
| Frontend         | HTML / CSS / JavaScript |
| API              | REST API / JSON         |
| Data Source      | CSV                     |
| Version Control  | Git / GitHub            |
| Interactive Demo | GitHub Pages            |

---

# 4. Problem → Debug → Solution

本專案著重於將資料問題轉換成可驗證、可重複執行的程式處理流程。

## Case 1 — CSV 編碼與文字格式

### Problem

CSV 可能包含 UTF-8 BOM、不間斷空白或多餘空白字元，造成欄位名稱與搜尋比對異常。

### Debug

檢查 CSV 載入後的欄位名稱及文字內容，確認是否存在編碼或隱藏字元問題。

### Solution

```text
UTF-8 / UTF-8-SIG
        ↓
Remove BOM
        ↓
Replace Non-breaking Spaces
        ↓
Strip Whitespace
        ↓
Normalized Data
```

透過 Pandas 對欄位名稱及文字資料進行標準化，降低格式差異造成的資料處理問題。

---

## Case 2 — 價格資料型別異常

### Problem

價格欄位可能含 `$`、`,` 或非數值內容，無法直接執行預算篩選及價格排序。

### Debug

檢查價格欄位的資料型別與轉換失敗資料。

### Solution

先移除價格格式字元，再使用：

```python
pd.to_numeric(..., errors="coerce")
```

將價格轉換為 numeric。

無法轉換的資料會成為 `NaN`，再從有效資料集中排除，避免錯誤資料進入後續流程。

---

## Case 3 — CSV 必要欄位缺失

### Problem

CSV 若缺少必要欄位，後續資料處理可能失敗。

### Solution

資料載入階段先驗證：

```text
餐廳區域
店家
餐點
價格
營業時間
```

若必要欄位不存在，系統直接回報缺少欄位，而不是繼續處理不完整資料。

---

## Case 4 — 空白或無效資料

### Problem

空白餐點名稱可能產生沒有意義的搜尋結果。

### Solution

完成文字標準化後，將空白餐點從有效 Dataset 排除。

```text
Raw Data
   ↓
Normalize
   ↓
Validate
   ↓
Remove Invalid Rows
   ↓
Valid Dataset
```

---

## Case 5 — 使用者輸入異常

### Problem

最高預算若輸入非整數或負數，可能造成錯誤的查詢結果。

### Solution

Flask Backend 加入 Input Validation。

正常輸入：

```text
100
150
200
```

異常輸入則回傳：

```text
HTTP 400
```

避免不合法輸入進入後續資料篩選流程。

---

## Case 6 — API Response Schema

### Problem

CSV 若包含額外 index 欄位，直接輸出 DataFrame 可能造成 API 欄位不一致。

### Solution

REST API 明確指定輸出欄位：

```text
餐廳區域
店家
餐點
價格
營業時間
```

確保 API Response Schema 維持一致。

---

# 5. Features｜功能與工程能力

## Interactive Features

* Keyword Search
* Restaurant Area Filter
* Shop Filter
* Budget Filter
* Price Sorting
* Clear Filters
* Responsive Web Interface

## Backend Features

* CSV Loading
* Data Cleaning
* Required Column Validation
* Missing / Invalid Data Handling
* Data Type Conversion
* Input Validation
* REST API
* JSON Response
* Exception Handling
* API Health Check

## Test Engineer Relevant Skills

本專案主要展示以下可轉移至 **Test Engineering / Test Automation** 的工程能力：

| Engineering Skill | Project Evidence                                |
| ----------------- | ----------------------------------------------- |
| Debugging         | 針對資料格式、型別與輸入異常進行問題定位                            |
| Data Validation   | 驗證 CSV 必要欄位與輸入資料                                |
| Error Handling    | 處理無效價格、空白資料與錯誤輸入                                |
| Test Thinking     | 將正常／異常輸入分開處理並確認預期結果                             |
| Data Processing   | 使用 Pandas 清理、轉換、篩選資料                            |
| Automation        | 將 CSV → Cleaning → Validation → Output 建立為可重複流程 |
| API Validation    | 使用 HTTP Status 與固定 Response Schema 驗證輸出         |
| Observability     | `/api/health` 提供服務狀態與資料筆數確認                     |

### Engineering Positioning

```text
TEST
Debugging
Validation
Error Handling

DATA QUALITY
Data Cleaning
Data Validation
Problem Investigation

AUTOMATION
Python
Pandas
REST API
```

> 本專案為 **Python / Data Processing / Web API 工程作品**。
>
> 本專案重點是展示可轉移至 Test Engineering 的 **Debugging、Data Validation、Error Handling、Test Thinking 與 Automation** 能力，不將此軟體專案描述為半導體製程、ICT/FCT、Yield 或硬體 Failure Analysis 的實務經驗。

---

# 6. Testing｜驗證方式

目前系統可透過正常輸入、邊界條件與異常輸入確認資料處理結果。

| Test Scenario   | Expected Result       |
| --------------- | --------------------- |
| CSV 正常載入        | 成功建立 Dataset          |
| CSV 缺少必要欄位      | 回報缺少欄位                |
| 價格為有效數字         | 成功轉換 numeric          |
| 價格格式含 `$` / `,` | 清理後進行轉換               |
| 價格無法轉換          | 排除無效資料                |
| 餐點名稱空白          | 排除該筆資料                |
| Keyword Search  | 回傳符合條件資料              |
| Budget Filter   | 僅回傳預算內餐點              |
| 非整數 Budget      | HTTP 400              |
| 負數 Budget       | HTTP 400              |
| Health Check    | HTTP 200 + API Status |

## API Health Check

Flask Backend 提供：

```text
/api/health
```

正常狀態：

```json
{
  "status": "ok",
  "items": 57,
  "message": "NYCU Campus Food Finder API 正常"
}
```

Health Check 用於快速確認：

```text
Application Running
        +
Dataset Loaded
        +
Current Item Count
```

> **Testing Scope**
>
> 上述內容描述目前程式的資料驗證與可測試情境。
> Automated Unit Test / pytest 可作為後續擴充，使測試流程進一步自動化。

---

# 7. Run Locally｜本機執行

## Clone Repository

```bash
git clone https://github.com/jamie12710-sketch/nycu-campus-food-finder.git
cd nycu-campus-food-finder
```

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

### macOS / Linux

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

開啟：

```text
http://127.0.0.1:5000
```

Health Check：

```text
http://127.0.0.1:5000/api/health
```

---

## Engineering Takeaway

這個專案的核心流程：

```text
Identify Problem
      ↓
Inspect Data
      ↓
Clean / Normalize
      ↓
Validate Input
      ↓
Handle Exceptions
      ↓
Verify Output
      ↓
Repeatable Process
```

透過這個流程，實際練習使用 **Python / Pandas / Flask** 將資料問題轉換成可驗證、可重複執行的程式處理流程。

---

## Author

**Jamie Hung**

Engineering Portfolio
Python · Pandas · Flask · Data Processing · Debugging · Test Automation

Repository: `jamie12710-sketch/nycu-campus-food-finder`
