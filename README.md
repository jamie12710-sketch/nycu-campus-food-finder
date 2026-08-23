# NYCU Campus Food Finder v3.1

陽明交通大學光復校區學生餐廳查詢 Web App。

## 功能
- 餐廳、店家、餐點關鍵字搜尋
- 最高預算篩選
- 價格低到高 / 高到低
- 統計餐廳、店家、餐點與價格
- 響應式手機 / 平板 / 電腦介面
- NYCU 校園餐廳 favicon

## 本機執行
```powershell
python -m pip install -r requirements.txt
python app.py
```
瀏覽器開啟 `http://127.0.0.1:5000`

## GitHub 展示
本專案是 Flask + Pandas Web App。GitHub 可以用來展示原始碼與 README；GitHub Pages 本身是靜態網站服務，不能直接執行本專案的 Flask Python 後端。若要線上操作，請把 GitHub 作為原始碼庫，再部署到支援 Python/Flask 的雲端服務。

## 專案結構
```text
nycu_restaurant_webapp_v3.1/
├─ app.py
├─ restaurant_data.csv
├─ requirements.txt
├─ README.md
├─ .gitignore
├─ templates/index.html
└─ static/
   ├─ style.css
   ├─ favicon.ico
   └─ favicon.svg
```
