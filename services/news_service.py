from threading import Thread
import time
from api.news_api import fetch_financial_news
from utils.data_processing import simplify_and_translate, explain_term, extract_terms, summarize_text
from bs4 import BeautifulSoup
import requests

articles_data = []

def get_full_article(url):
    """
    기사의 전체 내용을 가져옵니다.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 기사 본문을 추출합니다.
    article_body = soup.find_all('p')
    full_text = '\n'.join([p.get_text() for p in article_body])
    return full_text

def update_articles():
    global articles_data
    retry_count = 0
    while True:
        try:
            news_data = fetch_financial_news('finance OR stock OR market')
            articles = news_data.get('articles', [])

            new_articles_data = []
            for article in articles[:5]:  # 처리할 기사 수를 5개로 제한
                title = article['title']
                url = article['url']

                # 기사 전체 내용 가져오기
                full_content = get_full_article(url)

                # 기사 요약
                summary = summarize_text(full_content)

                # 주요 금융 용어 추출
                terms = extract_terms(full_content)
                term_explanations = {term: explain_term(term) for term in terms}

                # 제목과 내용을 단순화하고 번역
                simplified_and_translated = simplify_and_translate(full_content)
                
                # 용어 설명 추가
                explained_content = f"{summary}\n\n{simplified_and_translated}\n\n용어 설명:\n" + "\n".join(f"{term}: {explanation}" for term, explanation in term_explanations.items())

                new_articles_data.append({
                    'title': title,
                    'url': url,
                    'content': explained_content
                })

                print(f"처리 중인 기사: {title}")
                print("단순화 및 번역된 내용:")
                print(explained_content)
                print("-" * 50)

            articles_data = new_articles_data
            retry_count = 0  # 성공적으로 업데이트가 되면 카운트 초기화
            print("기사 업데이트 완료")
            print("1시간 대기 중...")
            time.sleep(3600)  # 1시간마다 업데이트

        except Exception as e:
            retry_count += 1
            print(f"오류 발생: {e}")
            if retry_count >= 3:  # 3번 이상 실패 시
                print("재시도 횟수 초과, 관리자에게 알림을 전송합니다.")
                # 알림 전송 코드 추가
            print("5분 후 재시도...")
            time.sleep(300)

def start_news_update_thread():
    update_thread = Thread(target=update_articles)
    update_thread.start()
