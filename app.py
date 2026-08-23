from flask import Flask, render_template, request, jsonify
import os
import pandas as pd

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'restaurant_data.csv')
REQUIRED = ['餐廳區域','店家','餐點','價格','營業時間']

def load_data():
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
    df.columns = df.columns.astype(str).str.strip()
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError('CSV 缺少欄位：' + ', '.join(missing))
    df['價格'] = pd.to_numeric(df['價格'].astype(str).str.replace('$','',regex=False).str.replace(',','',regex=False).str.strip(), errors='coerce')
    df = df.dropna(subset=['價格']).copy()
    df['價格'] = df['價格'].astype(int)
    for c in ['餐廳區域','店家','餐點','營業時間']:
        df[c] = df[c].fillna('').astype(str).str.strip()
    return df

df = load_data()

@app.route('/')
def index():
    stats = dict(restaurants=int(df['餐廳區域'].nunique()), shops=int(df['店家'].nunique()), items=len(df), avg=round(float(df['價格'].mean()),2), min=int(df['價格'].min()), max=int(df['價格'].max()))
    return render_template('index.html', restaurants=sorted(df['餐廳區域'].unique()), shops=sorted(df['店家'].unique()), stats=stats)

@app.route('/api/shops')
def shops():
    r = request.args.get('restaurant','').strip()
    x = df if not r or r == '全部' else df[df['餐廳區域'] == r]
    return jsonify(sorted(x['店家'].unique().tolist()))

@app.route('/api/search')
def search():
    x = df.copy()
    r = request.args.get('restaurant','').strip(); s = request.args.get('shop','').strip()
    k = request.args.get('keyword','').strip(); b = request.args.get('budget','').strip(); order = request.args.get('sort','default')
    if r and r != '全部': x = x[x['餐廳區域'] == r]
    if s and s != '全部': x = x[x['店家'] == s]
    if k:
        mask = x['餐點'].str.contains(k, case=False, na=False, regex=False) | x['店家'].str.contains(k, case=False, na=False, regex=False) | x['餐廳區域'].str.contains(k, case=False, na=False, regex=False)
        x = x[mask]
    if b:
        try:
            n = int(b)
            if n < 0: raise ValueError
            x = x[x['價格'] <= n]
        except ValueError:
            return jsonify(error='最高預算請輸入 0 以上的整數。'), 400
    if order == 'price_asc': x = x.sort_values('價格')
    elif order == 'price_desc': x = x.sort_values('價格', ascending=False)
    return jsonify(count=len(x), data=[{'餐廳區域':r['餐廳區域'],'店家':r['店家'],'餐點':r['餐點'],'價格':int(r['價格']),'營業時間':r['營業時間']} for _,r in x.iterrows()])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
