import nltk
from nltk.corpus import wordnet as wn
from openai import OpenAI
from config import OPENAI_API_KEY
import re

# 필수 라이브러리 다운로드
nltk.download('punkt')
nltk.download('wordnet')

client = OpenAI(api_key=OPENAI_API_KEY)

# 금융 관련 용어를 사전으로 정의
FINANCE_TERMS = set([
    'stock', 'market', 'bond', 'equity', 'portfolio', 'investment', 
    'asset', 'liability', 'capital', 'fund', 'dividend', 'credit', 'debt', 
    'derivative', 'inflation', 'interest', 'liquidity', 'margin', 'yield',
    'option', 'futures', 'hedge', 'index', 'exchange', 'trading'
])

def split_text(text, max_tokens=3000):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        if sum(len(s.split()) for s in current_chunk) + len(sentence.split()) > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
        current_chunk.append(sentence)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def simplify_and_translate(text):
    prompts = split_text(text)
    simplified_texts = []
    for prompt in prompts:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that simplifies complex financial contents."},
                {"role": "user", "content": f"다음 내용을 금융 지식이 적은 사람도 이해할 수 있게 간단하게 설명해주세요:\n\n{prompt}\n\n설명은 쉬운 용어를 사용하고, 전문 용어는 풀어서 설명해주세요."}
            ]
        )
        simplified_texts.append(response.choices[0].message.content.strip())
    
    return ' '.join(simplified_texts)

def explain_term(term):
    """
    금융 용어를 설명합니다.
    """
    prompt = f"""
    다음 금융 용어의 뜻을 설명해주세요. 설명은 쉬운 용어를 사용하고, 전문 용어는 풀어서 설명해주세요:

    {term}
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that explains financial terms in simple language."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def extract_terms(text):
    """
    텍스트에서 주요 금융 용어를 추출합니다.
    """
    words = nltk.word_tokenize(text)
    terms = set()

    for word in words:
        synsets = wn.synsets(word)
        if synsets:
            synset = synsets[0]
            # Synset 정의가 금융 관련인지 확인
            if any(term in synset.lexname() for term in ['finance', 'commerce']):
                terms.add(word.lower())
            elif word.lower() in FINANCE_TERMS:
                terms.add(word.lower())

    return list(terms)

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes complex financial contents."},
            {"role": "user", "content": f"다음 텍스트를 요약해주세요:\n\n{text}"}
        ]
    )
    
    return response.choices[0].message.content.strip()
