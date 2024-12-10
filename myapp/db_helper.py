import sqlite3
from flask import g
from datetime import datetime, timedelta


DATABASE = 'focusNews.db'

def get_db():
    """데이터베이스 연결을 가져오거나 생성합니다."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, timeout=5)  # 타임아웃 설정
        g.db.row_factory = sqlite3.Row  # 결과를 딕셔너리 형태로 변환
    return g.db

def init_db():
    """데이터베이스 초기화 및 테이블 생성."""
    conn = get_db()  # 현재 연결된 데이터베이스 가져오기
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS News (
        unique_link TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        content TEXT,
        summary TEXT,
        insight TEXT,
        image TEXT,  -- 이미지 경로
        upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 업로드 시간
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()

def insert_news(unique_link, title, description, content, summary, insight):
    """뉴스 항목을 데이터베이스에 삽입합니다."""
    conn = get_db()  # 현재 연결된 데이터베이스 가져오기
    cursor = conn.cursor()
    try:
        # 현재 시간을 UTC로 가져오고 KST로 변환
        current_time = datetime.utcnow() + timedelta(hours=9)  # KST로 변환
        created_at = current_time.strftime('%Y-%m-%d %H:%M:%S')  # 문자열 형식으로 변환

        cursor.execute('INSERT INTO News (unique_link, title, description, content, summary, insight, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                       (unique_link, title, description, content, summary, insight, created_at))
        conn.commit()
    except sqlite3.IntegrityError:
        # 이미 링크가 존재하는 경우 처리
        pass
    finally:
        cursor.close()  # 커서 닫기

def check_if_exists(unique_link):
    """unique_link가 데이터베이스에 존재하는지 확인합니다."""
    conn = get_db()  # 현재 연결된 데이터베이스 가져오기
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM News WHERE unique_link = ?', (unique_link,))
    exists = cursor.fetchone()[0] > 0  # 존재하면 True, 아니면 False
    cursor.close()  # 커서 닫기
    return exists

def close_db(exception):
    """데이터베이스 연결을 닫습니다."""
    db = g.pop('db', None)
    if db is not None:
        db.close()
