import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

def summarize_news(news_article):
    prompt = f"다음 본문을 귀여운 말투로 한줄로 요약해봐. ~했어요! 하면서 이모티콘도 넣고 \n그리고 <b>나 <br>등의 태그는 절대 포함하면 안 돼. \n\n본문: {news_article}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150, #생성되는 텍스트의 최대 길이 지정
        n=1, #생성할 답변수
        stop=None,
        #top_p= #상위 몇%의 답을 할지 정하도록 유도
        temperature=0.5, #0~2사이로 설정. (낮으면 일관성 중시, 높으면 창의력 중시)
    )

    summary = response['choices'][0]['message']['content'].strip()
    return summary

def generate_insight(summary):
    prompt = f"이 요약을 보고 더 확장할 수 있는 생각과 사회적 현상을 뉴스 앵커가 전하는 것처럼 표현해 줘. 대신 귀엽게, 한줄로 알려줘! \n그리고 <b>나 <br>등의 태그는 절대 포함하면 안 돼.\n\n{summary}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    insight = response['choices'][0]['message']['content'].strip()

    # 중복된 내용 제거
    if summary in insight:
        insight = insight.replace(summary, '').strip()  # 중복된 부분 제거

    return insight
