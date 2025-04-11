from flask import Blueprint, render_template_string

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Financial Info App</title>
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
                padding: 20px 0;
                text-align: center;
            }
            header h2 {
                margin: 0;
                font-size: 24px; /* Increase font size for better visibility */
                font-weight: bold;
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
            nav a:hover {
                color: #0066cc;
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
            <h1>Welcome to the Financial Info App</h1>
            <ul>
                <li><a href="/search">Search for Public Filings</a></li>
                <li><a href="/stock">Stock Exchange Decisions</a></li>
                <li><a href="/preferences">Set Your Preferences</a></li>
                <li><a href="/financial-indicators">View Financial Indicators</a></li>
                <li><a href="/financial-statements">View Financial Statements</a></li>
                <li><a href="/news">View Financial News</a></li>
            </ul>
        </div>
        <footer>
            <p>&copy; 2024 Financial Info App. All Rights Reserved.</p>
        </footer>
    </body>
    </html>

    '''
    return html_content