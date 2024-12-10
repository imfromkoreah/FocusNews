from flask import Flask, render_template, request, jsonify, session
from myapp.crawler_parallel import crawl_news_parallel, category_crawl, ranking_crawl#, special_crawl
from myapp.db_helper import get_db, close_db, init_db
# import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# 전역 변수 선언
newsCategory = ("정치", "경제", "사회", "생활/문화", "IT/과학", "세계")
categoryNum = (100, 101, 102, 103, 105, 104)
newsRanking = ("연예", "인기뉴스")


# 앱 시작 시 데이터베이스 초기화
with app.app_context():
    init_db()

# 요청 완료 후 DB 연결 닫기
@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# 기본 경로('/')로 접속 시 HTML 파일 렌더링
@app.route('/')
def home():
    session.clear() # 새로운 크롤링이 들어오면 세션 초기화
    return render_template('index.html')

# '/slider' 경로로 접속 시 slider.html 파일 렌더링
@app.route('/slider')
def slider():
    # 세션에서 'news_items' 값을 가져옵니다. (없으면 빈 리스트로 반환)
    news_items = session.get('news_items', [])
    print(f"세션에 저장된 unique_links: {news_items}")  # 디버깅용 출력

    # news_items를 템플릿에 전달
    return render_template('slider.html', news_items=news_items)


# 세션을 사용하여 news_items 리스트 관리
@app.route('/crawl_news', methods=['POST'])
def crawl_news_route():
    print("크롤링 페이지 접속")
    try:
        print('트라이 시작')
        data = request.get_json()
        user_message = data.get('message')

        if not user_message:
            return jsonify({'status': 'error', 'message': '키워드가 제공되지 않았습니다.'}), 400
        
        # 크롤링 요청 메시지 로그 출력
        print(f"크롤링 요청 메시지: {user_message}")  
        
        # `user_message`가 `newsRanking`에 포함되어 있는지 확인
        if user_message in newsRanking:
            news_items = ranking_crawl(user_message)
        # `user_message`가 `newsCategory`에 포함되어 있는지 확인
        elif user_message in newsCategory:
            news_items = category_crawl(categoryNum[newsCategory.index(user_message)])  # `user_message`가 카테고리인 경우
            if news_items == None:
                # ValueError 예외를 강제로 발생시킴
                raise ValueError("크롤링 오류")
        else:
            # 크롤링 함수 호출
            news_items = crawl_news_parallel(user_message)  # 크롤링 수행
            if news_items == None:
                # ValueError 예외를 강제로 발생시킴
                raise ValueError("크롤링 오류")

        
        # news_items에서 unique_link만 추출하여 세션에 저장
        unique_links = [item['unique_link'] for item in news_items]
        session['news_items'] = unique_links
        
        # 크롤링 후 저장된 unique_links 출력
        print(f"크롤링 후 세션에 저장된 unique_link: {session['news_items']}")

        return jsonify({
            'status': 'success',
            'message': '뉴스 크롤링이 완료되었습니다. 이제 /get_news로 데이터를 확인할 수 있습니다.',
            'news_items': unique_links
        })
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 뉴스 목록 조회 엔드포인트


# 뉴스 타이틀 정보 조회 엔드포인트
@app.route('/get_newstitle', methods=['GET'])
def get_newstitle():
    try:
        unique_link = request.args.get('unique_link')

        # DB에서 해당 unique_link의 summary 가져오기
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM News WHERE unique_link = ?', (unique_link,))
        title = cursor.fetchone()

        if title:
            # 세션에서 모든 unique_link 삭제
            session.pop('news_items', None)  # 세션에 저장된 모든 뉴스 항목 제거

            return jsonify({'status': 'success', 'summary': title[0]})
        else:
            return jsonify({'status': 'error', 'message': '해당 링크에 대한 타이틀 정보를 찾을 수 없습니다.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 뉴스 상세 요약 정보 조회 엔드포인트
@app.route('/get_summary', methods=['GET'])
def get_summary():
    try:
        unique_link = request.args.get('unique_link')

        # DB에서 해당 unique_link의 summary 가져오기
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT summary FROM News WHERE unique_link = ?', (unique_link,))
        summary = cursor.fetchone()

        if summary:
            # 세션에서 모든 unique_link 삭제
            session.pop('news_items', None)  # 세션에 저장된 모든 뉴스 항목 제거

            return jsonify({'status': 'success', 'summary': summary[0]})
        else:
            return jsonify({'status': 'error', 'message': '해당 링크에 대한 요약 정보를 찾을 수 없습니다.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 뉴스 상세 통찰력 정보 조회 엔드포인트
@app.route('/get_insight', methods=['GET'])
def get_insight():
    try:
        unique_link = request.args.get('unique_link')

        # DB에서 해당 unique_link의 insight 가져오기
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT insight FROM News WHERE unique_link = ?', (unique_link,))
        insight = cursor.fetchone()

        if insight:
            # 세션에서 모든 unique_link 삭제
            session.pop('news_items', None)  # 세션에 저장된 모든 뉴스 항목 제거

            return jsonify({'status': 'success', 'insight': insight[0]})
        else:
            return jsonify({'status': 'error', 'message': '해당 링크에 대한 통찰력 정보를 찾을 수 없습니다.'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
