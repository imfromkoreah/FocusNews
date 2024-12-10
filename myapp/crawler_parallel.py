import urllib.request
import requests
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from lxml import html

from myapp.openai_helper import summarize_news, generate_insight  # OpenAI 관련 함수
from myapp.db_helper import init_db, insert_news, get_db, close_db  # 데이터베이스 관련 함수

import os  # os 모듈을 가져옵니다.
from dotenv import load_dotenv  # dotenv를 가져옵니다.

# .env 파일 로드
load_dotenv()

# 네이버 클라이언트
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# 클라이언트 ID와 Secret 검증
if not client_id or not client_secret:
    raise ValueError("NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET가 설정되지 않았습니다.")


# 크롤링 정보들
newsTitle = '/html/body/div/div[2]/div/div[1]/div[1]/div[1]/div[2]/h2/span/text()'
newsContent = '/html/body/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/article//text()'

rankingTitle = '/html/body/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/h2/text()'
rankingContent = '/html/body/div/div[2]/div/div[1]/div/div[1]/div/div[2]/article/div[1]'

newsRanking = ({
    'category' : '인기뉴스',
    'url' : 'https://news.naver.com/main/ranking/popularDay.naver',
    'xpath' : '/html/body/div/div[4]/div[2]/div/div/ul/li[1]/div/a/@href',
    'title' : newsTitle,
    'content' : newsContent
}, {
    'category' : '연예',
    'url' : 'https://entertain.naver.com/ranking',
    'xpath' : '/html/body/div/div[2]/div/div/div[2]/div[2]/div/div[2]/ul/li/a/@href',
    'title' : rankingTitle,
    'content' : rankingContent
})

def process_article(item):
    title = item['title']
    link = item['link']
    description = item['description']

    # "/article/" 이후 unique_link 추출
    if "naver.com/" not in link:
        return None  # 조건에 맞지 않는 경우 None 반환
    unique_link = link.split('/article/')[-1].split('?')[0]

    # 뉴스 본문 크롤링 및 요약/느낀점 처리
    try:
        article_request = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        article_response = urllib.request.urlopen(article_request)
        article_soup = BeautifulSoup(article_response, 'html.parser')
        article_body = article_soup.find('article', {'id': 'dic_area'})
        full_text = article_body.get_text(strip=True) if article_body else "본문을 찾을 수 없습니다."
    except Exception as e:
        full_text = f"본문을 가져오는 중 오류 발생: {str(e)}"

    # 뉴스 요약 및 느낀점 생성
    summary = summarize_news(description)
    insight = generate_insight(summary)
    # image = generate_card_image(unique_link, summary)

    return unique_link, title, description, full_text, summary, insight #, image

def crawl_news_parallel(keyword):
    news_items = []  # 크롤링 결과를 저장할 리스트
    db = get_db()  # DB 연결을 가져옴
    encText = urllib.parse.quote(keyword)
    url = f"https://openapi.naver.com/v1/search/news?query={encText}&sort=sim"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            data = json.loads(response_body.decode('utf-8'))

            # 뉴스 항목을 가져옴
            news_items_to_process = data['items']

            # 병렬 처리로 뉴스 기사 크롤링 및 분석
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(process_article, item): item for item in news_items_to_process}

                # 유효한 결과만 news_items에 추가하고 5개가 되면 종료
                for future in as_completed(futures):
                    result = future.result()
                    if result:  # 유효한 결과만 추가
                        unique_link, title, description, full_text, summary, insight = result #, image
                        if len(news_items) < 5:
                            # if not image:
                            #     image = str(len(news_items))+".png"
                            insert_news(unique_link, title, description, full_text, summary, insight)
                            news_items.append({
                                'unique_link': unique_link,
                                'title': title,
                                'description': description,
                                'full_text': full_text,
                                'summary': summary,
                                'insight': insight # ,
                                # 'image': image
                            })
                        else:  # 유효한 뉴스 항목이 5개가 되면 종료
                            break
    except Exception as e:
        print(f"크롤링 중 오류 발생: {str(e)}")

    close_db(None)  # DB 연결 닫기
    print([(item['unique_link'], item['title']) for item in news_items])
    return news_items  # 크롤링된 뉴스 데이터 반환

#===================================================================================================


# 크롤링 프로세스
def process_link(unique_link, titleXpath = newsTitle, contentXpath = newsContent):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }   # 브라우저로 접속하는 것처럼 헤더 설정
    try:
        url = 'https://n.news.naver.com/article/' + unique_link
        print(url)

        # 뉴스 링크 처리
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        response_body = response.read().decode('utf-8')  # UTF-8로 디코딩
        tree = html.fromstring(response_body)

        # 뉴스 데이터 수집
        title = tree.xpath(titleXpath)[0]
        print(title)
        content = tree.xpath(contentXpath)
        full_text = ''.join(content).strip()
        description = full_text[:50] + '...'

        # 뉴스 요약 및 느낀점 생성
        summary = summarize_news(description)
        insight = generate_insight(summary)

        return {
            'unique_link': unique_link,
            'title': title,
            'description': description,
            'full_text': full_text,
            'summary': summary,
            'insight': insight
        }
    except Exception as e:
        print(f"링크 처리 중 오류 발생: {str(e)}")
        return None

# 카테고리 뉴스 크롤링
def category_crawl(category_number):
    base_url = f"https://news.naver.com/section/{category_number}"
    news_items = []
    unique_links = []
    db = get_db()  # DB 연결 생성

    try:
        # 카테고리 페이지 요청 및 파싱
        response = urllib.request.urlopen(base_url)
        response_body = response.read().decode('utf-8')  # UTF-8로 디코딩
        tree = html.fromstring(response_body)
        links = tree.xpath('/html/body/div/div[2]/div[2]/div[2]/div[1]/div[1]/ul/li/div/div/div[2]/a/@href')

        # 링크 5개만 남기기
        for link in links :
            # unique_link 추출
            unique_link = link.split('/article/')[-1].split('?')[0]
            if len(unique_link) == 14:  # len("241/0003393341")
                print("unique_link = " + unique_link)
                unique_links.append(unique_link)
                if len(unique_links) >= 5:
                    break
            else:
                continue

        # 병렬 크롤링 수행
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_link, link) for link in unique_links]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    # DB에서 이미 존재하는지 확인
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM News WHERE unique_link = ?", (result['unique_link'],))
                    existing_record = cursor.fetchone()

                    if existing_record:
                        # 이미 존재하는 경우 DB의 내용을 사용
                        columns = ['unique_link', 'title', 'description', 'content', 'summary', 'insight', 'image', 'upload']
                        news_item = dict(zip(columns, existing_record))
                    else:
                        # 새로운 데이터를 DB에 삽입
                        insert_news(
                            result['unique_link'],
                            result['title'],
                            result['description'],
                            result['full_text'],
                            result['summary'],
                            result['insight']
                        )
                        news_item = result
                    news_items.append(news_item)
    except Exception as e:
        print(f"크롤링 중 오류 발생: {str(e)}")
    finally:
        close_db(db)  # DB 연결 닫기

    return news_items


# 랭킹 크롤링
def ranking_crawl(message):
    # message가 포함된 딕셔너리를 찾고, 해당 딕셔너리 값을 변수로 설정
    select = next((item for item in newsRanking if item['category'] == message), None)

    if select:
        # 각각의 값을 변수에 저장
        category = select['category']
        base_url = select['url']
        xpath = select['xpath']
        title = select['title']
        content = select['content']
        
        print(f"Category: {category}")
        print(f"URL: {base_url}")
        print(f"XPath: {xpath}")
        print(f"Title: {title}")
        print(f"Content: {content}")
    else:
        print(f"{message}는 newsRanking 내에 존재하지 않습니다.")
        return
    news_items = []
    unique_links = []
    db = get_db()  # DB 연결 생성

    try:
        # 랭킹 페이지 요청 및 파싱
        response = urllib.request.urlopen(base_url)
        response_body = response.read()
        tree = html.fromstring(response_body)
        links = tree.xpath(xpath)[:12]

        # 링크 5개만 남기기
        for link in links :
            # unique_link 추출
            unique_link = link.split('/article/')[-1].split('?')[0]
            if len(unique_link) == 14:
                print("unique_link = " + unique_link)
                unique_links.append(unique_link)
                if len(unique_links) >= 5:
                    break
            else:
                continue
        
        # 뉴스 기사 처리
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_link, link, title, content) for link in unique_links]
            for future in futures:
                result = future.result()
                if result:
                    # DB에서 이미 존재하는지 확인
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM News WHERE unique_link = ?", (result['unique_link'],))
                    existing_record = cursor.fetchone()

                    if existing_record:
                        # 이미 존재하는 경우 DB의 내용을 사용
                        columns = ['unique_link', 'title', 'description', 'content', 'summary', 'insight', 'image', 'upload']
                        news_item = dict(zip(columns, existing_record))
                    else:
                        # 새로운 데이터를 DB에 삽입
                        insert_news(
                            result['unique_link'],
                            result['title'],
                            result['description'],
                            result['full_text'],
                            result['summary'],
                            result['insight']
                        )
                        news_item = result
                    news_items.append(news_item)

                if len(news_items) >= 5:
                    break

    except Exception as e:
        print(f"크롤링 중 오류 발생: {str(e)}")

    return news_items

if __name__ == "__main__":
    keyword = input("검색할 단어를 입력하세요: ")
    news_data = crawl_news_parallel(keyword)
    for news in news_data:
        print(news)
