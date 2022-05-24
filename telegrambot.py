# 파이썬 라이브러리 불러오기
from telegram.ext import Updater, MessageHandler, Filters
import telegram
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

# 내 토큰 설정
my_token = '#################################'
print('start telegram chat bot')

# 링크 저장할 리스트
old_links = []
new_links = []
links = []

# 봇이 나에게 메시지 보내는 함수
def get_message(update, context):
    word = update.message.text
    keyword = "".join(word.split())
    update.message.reply_text("{}가 포함된 가장 최신 기사를 가져옵니다.".format(keyword))
    url = f"https://m.search.naver.com/search.naver?where=m_news&query={keyword}&sm=mtb_tnw&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall"
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select_one('#news_result_list')
    news_list = search_result.select('.bx > .news_wrap > a')
        
    for news in news_list[:5]:
        link = news['href']
        links.append(link)

    for link in links:
        if link not in old_links:
            new_links.append(link)
    for news in new_links:
        update.message.reply_text(link)

updater = Updater(my_token, use_context=True)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()
