from django.conf import settings
from bs4 import BeautifulSoup
from .models import HackerNews
from django.db import transaction
import requests
import traceback


class HackerNewsParser:

    user_agent = settings.USER_AGENT
    url = settings.BASE_URL

    def __init__(self):
        self.headers = {
            'user-agent': self.user_agent
        }
        self.html_responses = []

    def parse(self):
        try:
            self.parse_html()
        except:
            print(traceback.format_exc())

    def parse_html(self):
        html = self.get_html(self.url)
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr', {'class': 'athing'})
        rows_for_ins = []
        with transaction.atomic():
            for tr in trs:
                row_ins = {}
                a_tag = tr.find('a', {'class': 'storylink'})
                row_ins['title'] = a_tag.text.strip()
                row_ins['url'] = a_tag['href'].replace("%20", ' ')
                HackerNews.objects.filter(url=row_ins['url']).delete()
                h = HackerNews(title=row_ins['title'], url=row_ins['url'])
                rows_for_ins.append(h)

            HackerNews.objects.bulk_create(rows_for_ins)

    def get_html(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 404:
                return
            if response.status_code != 200:
                raise ValueError('Request to {} responded with status {}'.format(url, response.status_code))
            else:
                html = response.text
                return html
        except Exception:
            raise Exception('Error in getting html\n'+str(traceback.format_exc()))
