import matplotlib
matplotlib.use('Agg')
from flask import Flask
from routes import main_routes, financial_routes, news_routes
from services.news_service import start_news_update_thread
import config
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt

rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)

# 라우트 등록
app.register_blueprint(main_routes.bp)
app.register_blueprint(financial_routes.bp)
app.register_blueprint(news_routes.bp)

if __name__ == '__main__':
    #start_news_update_thread()
    app.run(debug=True)