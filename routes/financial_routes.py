from flask import Blueprint, request, render_template
from api.dart_api import call_open_dart_api_json, get_corp_code, get_financial_statement, get_financial_data
from utils.data_processing import simplify_and_translate
from utils.visualization import plot_financial_data
from config import DART_API_KEY

bp = Blueprint('financial', __name__)

@bp.route('/search')
def search():
    result = call_open_dart_api_json(
        sort='date',
        sort_mth='desc',
        page_no='1',
        page_count='10'
    )
    simplified_items = []
    if result:
        items = result.get('list', [])
        for item in items:
            detailed_info = f"""
            공시 제목: {item.get('title')}
            공시 날짜: {item.get('rcept_dt')}
            공시 유형: {item.get('pblntf_ty')}
            공시 상세 유형: {item.get('pblntf_detail_ty')}
            회사명: {item.get('corp_name')}
            """
            simplified_text = simplify_and_translate(detailed_info)
            simplified_items.append(simplified_text)

    html_content = '''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Public Filings</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            header {
                background-color: #333;
                color: white;
                padding: 10px 0;
                text-align: center;
            }
            nav {
                margin: 10px;
                text-align: center;
            }
            nav a {
                margin: 0 15px;
                text-decoration: none;
                color: #333;
                font-weight: bold;
            }
            footer {
                background-color: #333;
                color: white;
                text-align: center;
                padding: 10px 0;
                position: fixed;
                bottom: 0;
                width: 100%;
            }
            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            li a {
                text-decoration: none;
                color: #0066cc;
            }
            li a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <header>
            <h2>FinanceTalkTalk</h2>
        </header>
        <nav>
            <a href="/">Home</a>
            <a href="/search">Public Filings</a>
            <a href="/stock">Stock Exchange Decisions</a>
            <a href="/preferences">Preferences</a>
            <a href="/financial-indicators">Financial Indicators</a>
            <a href="/financial-statements">Financial Statements</a>
            <a href="/news">News</a>
        </nav>
        <div class="container">
            <h1>Public Filings</h1>'''
    
    if simplified_items:
        html_content += '<ul>'
        for item in simplified_items:
            html_content += f'<li>{item}</li>'
        html_content += '</ul>'
    else:
        html_content += '<p>No data found or error occurred.</p>'
    
    html_content += '''
        </div>
        <footer>
            <p>&copy; 2024 Financial Info App. All Rights Reserved.</p>
        </footer>
    </body>
    </html>
    '''
    
    return html_content

@bp.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        corp_name = request.form['corp_name']
        corp_code = get_corp_code(corp_name)
        if corp_code:
            bgn_de = request.form['bgn_de']
            end_de = request.form['end_de']
            result = call_open_dart_api_json(corp_code, bgn_de, end_de)
            simplified_items = []
            if result:
                list_items = result.get('list', [])
                for item in list_items:
                    detailed_info = f"""
                    회사명: {item.get('corp_name')}
                    결정일: {item.get('bddd')}
                    평가 기간: {item.get('exevl_pd')}
                    주식 교환 비율: {item.get('extr_rt')}
                    비율 기준: {item.get('extr_rt_bs')}
                    평가 의견: {item.get('exevl_op')}
                    주식 교환 이유: {item.get('extr_pp')}
                    """
                    simplified_text = simplify_and_translate(detailed_info)
                    simplified_items.append(simplified_text)
            
            html_content = f'''
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Stock Exchange Decisions</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    header {{
                        background-color: #333;
                        color: white;
                        padding: 10px 0;
                        text-align: center;
                    }}
                    nav {{
                        margin: 10px;
                        text-align: center;
                    }}
                    nav a {{
                        margin: 0 15px;
                        text-decoration: none;
                        color: #333;
                        font-weight: bold;
                    }}
                    footer {{
                        background-color: #333;
                        color: white;
                        text-align: center;
                        padding: 10px 0;
                        position: fixed;
                        bottom: 0;
                        width: 100%;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 20px auto;
                        padding: 20px;
                        background-color: white;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #333;
                        text-align: center;
                    }}
                    ul {{
                        list-style-type: none;
                        padding: 0;
                    }}
                    li {{
                        margin: 10px 0;
                    }}
                    li a {{
                        text-decoration: none;
                        color: #0066cc;
                    }}
                    li a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <header>
                    <h2>FinanceTalkTalk</h2>
                </header>
                <nav>
                    <a href="/">Home</a>
                    <a href="/search">Public Filings</a>
                    <a href="/stock">Stock Exchange Decisions</a>
                    <a href="/preferences">Preferences</a>
                    <a href="/financial-indicators">Financial Indicators</a>
                    <a href="/financial-statements">Financial Statements</a>
                    <a href="/news">News</a>
                </nav>
                <div class="container">
                    <h1>Stock Exchange Decisions for {corp_name}</h1>'''
            
            if simplified_items:
                html_content += '<ul>'
                for item in simplified_items:
                    html_content += f'<li>{item}</li>'
                html_content += '</ul>'
            else:
                html_content += '<p>No data found or error occurred.</p>'
            html_content += '''
                </div>
                <footer>
                    <p>&copy; 2024 Financial Info App. All Rights Reserved.</p>
                </footer>
            </body>
            </html>
            '''
            return html_content
        else:
            return f"<h1>Company name '{corp_name}' not found.</h1>", 404

    html_content = '''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Stock Exchange Decisions</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            header {
                background-color: #333;
                color: white;
                padding: 10px 0;
                text-align: center;
            }
            nav {
                margin: 10px;
                text-align: center;
            }
            nav a {
                margin: 0 15px;
                text-decoration: none;
                color: #333;
                font-weight: bold;
            }
            footer {
                background-color: #333;
                color: white;
                text-align: center;
                padding: 10px 0;
                position: fixed;
                bottom: 0;
                width: 100%;
            }
            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            li a {
                text-decoration: none;
                color: #0066cc;
            }
            li a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <header>
            <h2>FinanceTalkTalk</h2>
        </header>
        <nav>
            <a href="/">Home</a>
            <a href="/search">Public Filings</a>
            <a href="/stock">Stock Exchange Decisions</a>
            <a href="/preferences">Preferences</a>
            <a href="/financial-indicators">Financial Indicators</a>
            <a href="/financial-statements">Financial Statements</a>
            <a href="/news">News</a>
        </nav>
        <div class="container">
            <h1>Stock Exchange Decisions</h1>
            <form method="POST">
                <label for="corp_name">Enter Company Name:</label><br><br>
                <input type="text" id="corp_name" name="corp_name" required><br><br>
                <label for="bgn_de">Start Date (YYYYMMDD):</label><br><br>
                <input type="text" id="bgn_de" name="bgn_de" required><br><br>
                <label for="end_de">End Date (YYYYMMDD):</label><br><br>
                <input type="text" id="end_de" name="end_de" required><br><br><br>
                <input type="submit" value="Submit">
            </form>
        </div>
        <footer>
            <p>&copy; 2024 Financial Info App. All Rights Reserved.</p>
        </footer>
    </body>
    </html>
    '''
    return html_content

@bp.route('/financial-indicators', methods=['GET', 'POST'])
def financial_indicators():
    if request.method == 'POST':
        corp_names = request.form.get('corp_names').split(', ')
        bsns_year = request.form.get('bsns_year')
        report_option = request.form.get('report_option')
        idx_option = request.form.get('idx_option')

        report_code = {
            '1': '11013',
            '2': '11012',
            '3': '11014',
            '4': '11011'
        }.get(report_option)

        idx_code = {
            '1': 'M210000',
            '2': 'M220000',
            '3': 'M230000',
            '4': 'M240000'
        }.get(idx_option)

        if not report_code or not idx_code:
            return "잘못된 입력입니다."

        financial_data = []
        for name in corp_names:
            corp_code = get_corp_code(name)
            if corp_code:
                company_data = get_financial_data(corp_code, bsns_year, report_code, idx_code)
                for item in company_data:
                    financial_data.append((item[0], item[1], name))
            else:
                return f"{name}의 고유번호를 찾을 수 없습니다."

        img_base64 = plot_financial_data(financial_data)
        return render_template('index.html', img_base64=img_base64)

    return render_template('index.html')

def chunk_text(text, max_tokens=1500):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield ' '.join(words[i:i + max_tokens])

@bp.route('/financial-statements', methods=['GET', 'POST'])
def financial_statements():
    if request.method == 'POST':
        corp_name = request.form['corp_name']
        bsns_year = request.form['bsns_year']
        reprt_choice = request.form['reprt_choice']
        fs_choice = request.form['fs_choice']

        reprt_codes = {
            '1': '11013',
            '2': '11012',
            '3': '11014',
            '4': '11011'
        }
        fs_divisions = {
            '1': 'OFS',
            '2': 'CFS'
        }
        reprt_code = reprt_codes.get(reprt_choice, '11011')
        fs_div = fs_divisions.get(fs_choice, 'OFS')

        corp_code = get_corp_code(corp_name)
        if not corp_code:
            return f"<h1>Company name '{corp_name}' not found.</h1>", 404

        financial_data = get_financial_statement(DART_API_KEY, corp_code, bsns_year, reprt_code, fs_div)
        if financial_data:
            html_content = f'<h1>Financial Statements for {corp_name} ({bsns_year})</h1>'
            simplified_data = ""
            
            for chunk in chunk_text(str(financial_data)):
                simplified_chunk = simplify_and_translate(chunk)
                simplified_data += simplified_chunk
            
            html_content += '<pre>' + simplified_data + '</pre>'
            return html_content
        else:
            return '<h1>No financial data found or error occurred.</h1>', 404

    # HTML content for GET request...
    html_content = '''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Financial Statements</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            header {
                background-color: #333;
                color: white;
                padding: 10px 0;
                text-align: center;
            }
            nav {
                margin: 10px;
                text-align: center;
            }
            nav a {
                margin: 0 15px;
                text-decoration: none;
                color: #333;
                font-weight: bold;
            }
            footer {
                background-color: #333;
                color: white;
                text-align: center;
                padding: 10px 0;
                position: fixed;
                bottom: 0;
                width: 100%;
            }
            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background-color: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <header>
            <h2>FinanceTalkTalk</h2>
        </header>
        <nav>
            <a href="/">Home</a>
            <a href="/search">Public Filings</a>
            <a href="/stock">Stock Exchange Decisions</a>
            <a href="/preferences">Preferences</a>
            <a href="/financial-indicators">Financial Indicators</a>
            <a href="/financial-statements">Financial Statements</a>
            <a href="/news">News</a>
        </nav>
        <div class="container">
            <h1>View Financial Statements</h1>
            <form method="post">
                <label for="corp_name">Company Name:</label>
                <input type="text" id="corp_name" name="corp_name" required>
                <br><br>
                <label for="bsns_year">Business Year (YYYY):</label>
                <input type="text" id="bsns_year" name="bsns_year" required>
                <br><br>
                <label for="reprt_choice">Report Type:</label>
                <select id="reprt_choice" name="reprt_choice" required>
                    <option value="1">1분기보고서</option>
                    <option value="2">반기보고서</option>
                    <option value="3">3분기보고서</option>
                    <option value="4">사업보고서</option>
                </select>
                <br><br>
                <label for="fs_choice">Financial Statement Type:</label>
                <select id="fs_choice" name="fs_choice" required>
                    <option value="1">개별재무제표 (OFS)</option>
                    <option value="2">연결재무제표 (CFS)</option>
                </select>
                <br><br>
                <input type="submit" value="Submit">
            </form>
        </div>
        <footer>
            <p>&copy; 2024 Financial Info App. All Rights Reserved.</p>
        </footer>
    </body>
    </html>
    '''
    return html_content