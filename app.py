from flask import Flask, request, render_template
import requests

app = Flask(__name__)


# =========================
# 中韓 / 中日翻譯題庫
# =========================

zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요": "你好",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}

zh_ja_dict = {
    "你好": "こんにちは",
    "안녕하세요": "こんにちは",
    "謝謝": "ありがとうございます",
    "對不起": "すみません",
    "早安": "おはようございます",
    "晚安": "おやすみなさい",
    "老師": "先生",
    "學生": "学生",
    "朋友": "友達",
    "家人": "家族",
    "愛": "愛"
}


# =========================
# 首頁
# =========================

@app.route('/')
def index():
    return render_template('index.html')


# =========================
# 競賽經驗
# =========================

@app.route('/competition')
def competition():
    return render_template('competition.html')


# =========================
# 中韓字典
# =========================

@app.route('/ask', methods=['GET', 'POST'])
def ask():

    if request.method == 'POST':

        question1 = request.form.get('question', '').strip()
        # 取得表單傳送的目標語言 (預設 ko)
        target_lang = request.form.get('target_lang', 'ko')

        if target_lang == 'ja':
            dictionary = zh_ja_dict
            lang_name = "日文"
        else:
            dictionary = zh_ko_dict
            lang_name = "韓文"

        # 查詢題庫
        answer1 = dictionary.get(
            question1,
            f"抱歉，我目前沒有這個詞的{lang_name}對應。"
        )

        return render_template(
            'ask.html',
            question=question1,
            answer=answer1,
            target_lang=target_lang
        )

    return render_template(
        'ask.html',
        question="",
        answer="",
        target_lang="ko"
    )


# =========================
# 課外活動
# =========================

@app.route('/activities', methods=['GET', 'POST'])
def activities():

    if request.method == 'POST':

        question = request.form.get(
            'question',
            ''
        ).strip()

        target_lang = request.form.get('target_lang', 'ko')

        if target_lang == 'ja':
            dictionary = zh_ja_dict
            lang_name = "日文"
        else:
            dictionary = zh_ko_dict
            lang_name = "韓文"

        answer1 = dictionary.get(
            question,
            f"抱歉，我目前沒有這個詞的{lang_name}對應。"
        )

        return render_template(
            'activities.html',
            question=question,
            answer=answer1,
            target_lang=target_lang
        )

    return render_template(
        'activities.html',
        question="",
        answer="",
        target_lang="ko"
    )


# =========================
# 股票查詢
# =========================

@app.route('/stock', methods=['GET', 'POST'])
def stock():

    if request.method == 'POST':

        # 取得使用者輸入的股票代號
        stock_no = request.form.get(
            'question',
            ''
        ).strip()

        # 防止使用者沒有輸入股票代號
        if not stock_no:

            return render_template(
                'stock.html',
                question="",
                answer="請輸入股票代號，例如：2330"
            )

        try:

            # 台灣證券交易所 API
            url = (
                "https://www.twse.com.tw/"
                "exchangeReport/STOCK_DAY"
                f"?response=json&stockNo={stock_no}"
            )

            # 發送請求
            res = requests.get(
                url,
                timeout=10
            )

            data = res.json()

            # 判斷 API 是否成功
            if data.get("stat") == "OK" and data.get("data"):

                # 最新一筆資料
                latest_data = data["data"][-1]

                # 收盤價通常位於第 7 欄
                answer = latest_data[6]

            else:

                answer = (
                    "查無資料，請確認股票代號是否正確。"
                )

        except Exception as e:

            answer = (
                "查詢股票時發生錯誤，"
                "請稍後再試。"
            )

        return render_template(
            'stock.html',
            question=stock_no,
            answer=answer
        )

    # GET
    return render_template(
        'stock.html',
        question="",
        answer=""
    )


# =========================
# 幹部經驗
# =========================

@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


# =========================
# 社團經驗
# =========================

@app.route('/club')
def club():
    return render_template('club.html')


# =========================
# 多元選修
# =========================

@app.route('/electives')
def electives():
    return render_template('electives.html')


# =========================
# AI 應用
# =========================

@app.route('/ai')
def ai():
    return render_template('ai.html')


# =========================
# 🌍 世界計畫
# =========================

@app.route('/world-project')
def world_project():

    return render_template(
        'world-project.html'
    )


# =========================
# 啟動 Flask
# =========================

if __name__ == '__main__':
    app.run(debug=True)
