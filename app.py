from flask import Flask, render_template, request, jsonify
import os
import pandas as pd

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIRED = ["餐廳區域", "店家", "餐點", "價格", "營業時間"]


def find_csv():
    # 優先使用標準檔名；若使用者下載成 restaurant_data(3).csv 也能自動找到。
    candidates = [
        os.path.join(BASE_DIR, "restaurant_data.csv"),
        os.path.join(BASE_DIR, "restaurant_data(3).csv"),
        os.path.join(BASE_DIR, "restaurant_data(2).csv"),
        os.path.join(BASE_DIR, "restaurant_data(1).csv"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("找不到 restaurant_data.csv（或 restaurant_data(3).csv）")


def clean_text(series):
    return (series.fillna("").astype(str)
            .str.replace("\ufeff", "", regex=False)
            .str.replace("\xa0", " ", regex=False)
            .str.strip())


def load_data():
    csv_file = find_csv()
    try:
        data = pd.read_csv(csv_file, encoding="utf-8-sig")
    except UnicodeDecodeError:
        data = pd.read_csv(csv_file, encoding="utf-8")

    data.columns = (data.columns.astype(str)
                    .str.replace("\ufeff", "", regex=False)
                    .str.strip())

    # 舊版 CSV 可能有 index 欄，新版沒有；不影響餐點資料。
    missing = [c for c in REQUIRED if c not in data.columns]
    if missing:
        raise ValueError("CSV 缺少欄位：" + ", ".join(missing))

    for c in ["餐廳區域", "店家", "餐點", "營業時間"]:
        data[c] = clean_text(data[c])

    data["價格"] = (data["價格"].astype(str)
                     .str.replace("$", "", regex=False)
                     .str.replace(",", "", regex=False)
                     .str.strip())
    data["價格"] = pd.to_numeric(data["價格"], errors="coerce")
    data = data.dropna(subset=["價格"]).copy()
    data["價格"] = data["價格"].astype(int)

    # 餐點為空的資料不應顯示成空白餐點列。
    data = data[data["餐點"] != ""].copy()
    return data.reset_index(drop=True)


df = load_data()


def stats_dict(data):
    if data.empty:
        return {"restaurants": 0, "shops": 0, "items": 0, "avg": 0, "min": 0, "max": 0}
    return {
        "restaurants": int(data["餐廳區域"].nunique()),
        "shops": int(data["店家"].nunique()),
        "items": int(len(data)),
        "avg": round(float(data["價格"].mean()), 2),
        "min": int(data["價格"].min()),
        "max": int(data["價格"].max()),
    }


def to_records(data):
    # 明確指定欄位，避免 CSV 額外 index 欄造成前端顯示錯位。
    return [{
        "餐廳區域": str(row["餐廳區域"]),
        "店家": str(row["店家"]),
        "餐點": str(row["餐點"]),
        "價格": int(row["價格"]),
        "營業時間": str(row["營業時間"]),
    } for _, row in data.iterrows()]


@app.route("/")
def index():
    return render_template(
        "index.html",
        restaurants=sorted(df["餐廳區域"].unique().tolist()),
        shops=sorted(df["店家"].unique().tolist()),
        stats=stats_dict(df),
    )


@app.route("/api/shops")
def shops():
    restaurant = request.args.get("restaurant", "").strip()
    data = df if not restaurant or restaurant == "全部" else df[df["餐廳區域"] == restaurant]
    return jsonify(sorted(data["店家"].drop_duplicates().tolist()))


@app.route("/api/search")
def search():
    data = df.copy()
    restaurant = request.args.get("restaurant", "").strip()
    shop = request.args.get("shop", "").strip()
    keyword = request.args.get("keyword", "").strip()
    budget = request.args.get("budget", "").strip()
    sort_order = request.args.get("sort", "default").strip()

    if restaurant and restaurant != "全部":
        data = data[data["餐廳區域"] == restaurant]
    if shop and shop != "全部":
        data = data[data["店家"] == shop]

    if keyword:
        # 關鍵字可搜尋餐點、店家、餐廳區域。
        mask = (
            data["餐點"].str.contains(keyword, case=False, na=False, regex=False) |
            data["店家"].str.contains(keyword, case=False, na=False, regex=False) |
            data["餐廳區域"].str.contains(keyword, case=False, na=False, regex=False)
        )
        data = data[mask]

    if budget:
        try:
            limit = int(budget)
            if limit < 0:
                raise ValueError
        except ValueError:
            return jsonify({"error": "最高預算請輸入 0 以上的整數。"}), 400
        data = data[data["價格"] <= limit]

    if sort_order == "price_asc":
        data = data.sort_values(["價格", "餐點"], ascending=[True, True])
    elif sort_order == "price_desc":
        data = data.sort_values(["價格", "餐點"], ascending=[False, True])

    return jsonify({"count": int(len(data)), "data": to_records(data)})


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "items": int(len(df)), "message": "NYCU Campus Food Finder API 正常"})


@app.route("/favicon.ico")
def favicon():
    from flask import send_from_directory
    return send_from_directory(os.path.join(BASE_DIR, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
