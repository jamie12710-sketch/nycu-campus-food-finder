# NYCU Campus Food Finder
  午餐吃什麼?

### Python Data Processing · Debugging · REST API Engineering Portfolio

以陽明交通大學光復校區學生餐廳資料為題，使用 **Python、Pandas、Flask** 建立餐點資料查詢系統。

專案不只是餐廳搜尋介面，更著重於實際資料處理過程中的 **Data Cleaning、Data Validation、Exception Handling、Debugging 與 API Design**，將原始 CSV 資料轉換為可搜尋、篩選與排序的結構化資料。

> **Engineering Focus:** Python · Pandas · Flask · Data Cleaning · Data Validation · Debugging · REST API

![NYCU Campus Food Finder 主視覺](docs/food-finder-hero.webp)

---

## 🎯 Project Objective｜專案目標

餐廳原始資料可能存在文字格式不一致、空值、價格格式異常、CSV 編碼差異或額外欄位等問題。

本專案建立一套可重複執行的資料處理流程：

```text
Raw CSV Data
      │
      ▼
CSV Loading / Encoding Handling
      │
      ▼
Required Column Validation
      │
      ▼
Data Cleaning
      │
      ├── BOM / 空白字元處理
      ├── 缺失文字處理
      ├── 價格格式清理
      └── 無效資料排除
      │
      ▼
Data Type Conversion
      │
      ▼
Flask REST API
      │
      ├── Search
      ├── Filter
      ├── Budget Validation
      └── Sorting
      │
      ▼
Web Interface / API Response
```

目標是讓資料從原始 CSV 進入系統後，經過驗證與清理，再提供穩定的查詢結果。

---

## 🛠 Tech Stack｜使用技術

| Category        | Technology              |
| --------------- | ----------------------- |
| Programming     | Python                  |
| Data Processing | Pandas                  |
| Backend         | Flask                   |
| API             | REST API / JSON         |
| Data Source     | CSV                     |
| Version Control | Git / GitHub            |
| Frontend        | HTML / CSS / JavaScript |
| Deployment Demo | GitHub Pages            |

---

## 🔍 Problem → Debug → Solution

### 1. CSV 編碼與文字格式問題

**Problem**

CSV 可能包含 UTF-8 BOM、不間斷空白或多餘空白字元，造成欄位名稱或文字比對異常。

**Debug**

檢查 CSV 載入後的欄位名稱及文字內容，確認問題來自編碼與隱藏字元。

**Solution**

使用 Pandas 讀取資料，並對欄位名稱與文字資料進行標準化：

```text
UTF-8 / UTF-8-SIG
        ↓
Remove BOM
        ↓
Replace non-breaking spaces
        ↓
Strip whitespace
        ↓
Normalized Text Data
```

---

### 2. 價格欄位無法直接進行數值運算

**Problem**

價格資料可能含 `$`、`,` 或其他非數值格式，無法直接進行預算篩選與價格排序。

**Debug**

檢查價格欄位的資料型別及轉換失敗資料。

**Solution**

先移除價格格式字元，再透過 Pandas：

```python
pd.to_numeric(..., errors="coerce")
```

轉換為 numeric。

無法轉換的資料會成為 `NaN`，再從有效資料集中排除，最後轉換為整數。

---

### 3. CSV 欄位異常造成程式錯誤

**Problem**

如果 CSV 缺少必要欄位，後續資料處理可能直接失敗。

**Solution**

系統載入資料時先檢查必要欄位：

```text
餐廳區域
店家
餐點
價格
營業時間
```

若缺少必要欄位，系統會回報缺少的欄位，而不是繼續處理錯誤資料。

---

### 4. 空白餐點資料

**Problem**

缺失或空白的餐點名稱可能產生無意義的搜尋結果。

**Solution**

文字資料清理後，將空白餐點資料從有效 Dataset 排除，避免前端顯示空白項目。

---

### 5. 使用者輸入異常

**Problem**

最高預算若輸入非整數或負數，可能造成查詢邏輯錯誤。

**Solution**

後端加入輸入驗證。

有效輸入：

```text
100
150
200
```

異常輸入會回傳 HTTP `400` 與錯誤訊息，避免錯誤資料進入後續篩選流程。

---

### 6. API 輸出欄位不一致

**Problem**

CSV 若包含額外 index 欄位，直接輸出資料可能造成前端欄位錯位。

**Solution**

API 不直接輸出所有 DataFrame 欄位，而是明確指定：

```text
餐廳區域
店家
餐點
價格
營業時間
```

確保 API Response Schema 穩定。

---

## ⚙️ Engineering Skills Demonstrated

透過本專案實際練習與展示：

* **Python Programming**
* **Pandas Data Processing**
* **Data Cleaning**
* **Missing / Invalid Data Handling**
* **Data Type Validation**
* **Input Validation**
* **Exception Handling**
* **Debugging**
* **REST API Design**
* **JSON Data Processing**
* **Conditional Filtering**
* **Data Sorting**
* **API Health Check**
* **Git / GitHub Version Control**

這些能力可延伸至需要資料驗證、異常排查、測試資料處理及流程改善的工程工作。

---

## 🔎 Core Features｜核心功能

系統支援：

* 餐點關鍵字搜尋
* 店家搜尋
* 餐廳區域搜尋
* 餐廳區域與店家連動篩選
* 最高預算篩選
* 價格由低至高排序
* 價格由高至低排序
* API 錯誤回應
* API Health Check
* Desktop / Mobile Web Interface

---

## 🩺 API Health Check

系統提供：

```text
/api/health
```

用於確認 Flask API 是否正常運作。

正常狀態會回傳：

```json
{
  "status": "ok",
  "items": 57,
  "message": "NYCU Campus Food Finder API 正常"
}
```

透過 Health Check 可以快速確認服務狀態及目前載入的資料筆數。

---

## 📊 Dataset Summary｜資料摘要

| 指標   |        資料 |
| ---- | --------: |
| 餐廳區域 |         4 |
| 店家   |        13 |
| 餐點   |        57 |
| 價格範圍 | NT$30–229 |

> 本專案使用隨附 CSV 作為作品展示資料。餐點、價格與營業時間不代表即時狀態，正式使用前應重新確認資料來源與更新日期。

---

## 🏗 Project Architecture｜專案架構

```text
nycu-campus-food-finder/
│
├── .github/
│   └── workflows/
│
├── docs/
│   └── GitHub Pages static demo
│
├── static/
│   └── Flask static assets
│
├── templates/
│   └── index.html
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

---

## 🔄 Data Processing Flow

```text
restaurant_data.csv
        │
        ▼
     find_csv()
        │
        ▼
     load_data()
        │
        ├── Encoding Handling
        ├── Column Validation
        ├── Text Cleaning
        ├── Price Conversion
        └── Invalid Row Removal
        │
        ▼
   Pandas DataFrame
        │
        ▼
     Flask API
        │
   ┌────┼─────────────┐
   ▼    ▼             ▼
shops  search       health
 API    API           API
   │    │             │
   └────┴──────┬──────┘
               ▼
        Web Interface
```

---

## 🚀 How to Run｜本機執行

### 1. Clone Repository

```bash
git clone https://github.com/jamie12710-sketch/nycu-campus-food-finder.git
cd nycu-campus-food-finder
```

### 2. 建立 Python Virtual Environment

```bash
python -m venv .venv
```

### 3. Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

### 4. macOS / Linux

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

### 5. 開啟系統

```text
http://127.0.0.1:5000
```

Health Check：

```text
http://127.0.0.1:5000/api/health
```

---

## 💡 What I Learned｜專案學習成果

透過此專案，我實際將原始 CSV 資料轉換為可供系統使用的結構化資料，並處理資料格式、缺失值、型別轉換及異常輸入等問題。

相較於單純完成查詢功能，本專案更著重於：

```text
發現資料問題
      ↓
確認異常原因
      ↓
建立資料清理規則
      ↓
加入輸入與欄位驗證
      ↓
確認輸出結果
      ↓
建立可重複執行的處理流程
```

這個過程讓我進一步練習以工程化方式進行 **Problem Identification、Debugging、Data Validation 與 Process Improvement**。

---

## 🎯 Career Relevance｜工程職務能力連結

此作品主要展示以下可轉移工程能力：

**Test / Debug**

透過輸入驗證、異常資料排除與錯誤處理，練習定位問題並建立防呆機制。

**Data Analysis**

使用 Pandas 進行資料清理、型別轉換、條件篩選與統計。

**Automation**

將原始 CSV → 清理 → 驗證 → API Output 建立成可重複執行的 Python 處理流程。

**Problem Solving**

從資料格式與系統輸出問題出發，逐步確認原因並建立程式化解決方案。

> 專案為 Python / Data Processing 工程作品，不代表半導體製程、ICT/FCT、Yield 或硬體 Failure Analysis 的實務工作經驗。
> 重點在展示可轉移至 Test Engineering 的資料處理、Debugging 與問題分析能力。

---

## 👤 Author

**Jamie Hung**

Engineering Portfolio
Python · Pandas · Flask · Data Processing · Debugging

Repository:
`jamie12710-sketch/nycu-campus-food-finder`
