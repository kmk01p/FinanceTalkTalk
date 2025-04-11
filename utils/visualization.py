import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64

def plot_financial_data(financial_data):
    df = pd.DataFrame(financial_data, columns=['지표명', '지표값', '회사'])
    df['지표값'] = pd.to_numeric(df['지표값'], errors='coerce')
    df = df.dropna()

    plt.figure(figsize=(14, 8))

    unique_metrics = df['지표명'].unique()
    bar_width = 0.2
    index = np.arange(len(unique_metrics))

    for i, company in enumerate(df['회사'].unique()):
        company_data = df[df['회사'] == company]
        plt.bar(index + i * bar_width, company_data['지표값'], bar_width, label=company)

    plt.ylabel('지표값')
    plt.xlabel('지표명')
    plt.title('다중 회사 재무 지표 시각화')
    plt.xticks(index + bar_width, unique_metrics)
    plt.legend()
    plt.grid(axis='y')

    # 이미지 저장
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    
    # Base64 인코딩
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return img_base64