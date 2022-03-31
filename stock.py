import requests
from bs4 import BeautifulSoup
import os
import time


class Paxnet:
    def __init__(self):
        pass
    
    @staticmethod
    def _isfile(filename):
        if os.path.isfile(filename):
            return True
        else:
            return False

    def get_themes(self):
        filename = 'paxnet_themes.txt'
        if not self._isfile(filename):
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
            }
            data = {
                "currentPageNo": "1",
                "preCurrentPageNo": "1",
                "schThemaCode": "",
                "schThemaName": ""
            }

            # url = 'https://finance.daum.net/api/themes/leading_stocks?page=2&perPage=30&fieldName=changeRate&order=desc&pagination=true'
            url = 'https://www.paxnet.co.kr/stock/infoStock/themaStock'
            r = requests.post(url, data=data, headers=headers)
            with open(filename, 'wt', encoding='utf-8') as f:
                f.write(r.text)
        else:
            f = open(filename, "rt", encoding='utf-8')
            r = f.read()
            bs = BeautifulSoup(r, 'html.parser')
            themes = bs.find('div', {'class': 'm-only-box'}).find('div', {'class': 'table-scroll'})

            themes_title = themes.find('thead').find('tr').findAll('th')
            themes_title_list = [v.text.strip() for v in themes_title]

            themes_title_essential = [value for i, value in enumerate(themes_title_list) if i in {0, 1, 3, 4}]

            themes_contents_row = themes.find('tbody').findAll('tr')
            themes_contents_list = [[v.text.strip().replace('상향', '') for v in row.findAll('td')] for row in themes_contents_row]
            themes_contents_essential = [[data for i, data in enumerate(rows) if i in {0, 1, 3, 4}] for rows in themes_contents_list]

            def print_all():
                for values in themes_contents_essential:
                    for key, value,  in zip(themes_title_essential, values):
                        print('{}: {}'.format(key, value))
            # print_all()
            def print_stock_v1(nested_list):
                r_str = ''
                for values in nested_list:
                    r_str += ' '.join(values) + '\n'
                return r_str

            print(print_stock_v1(themes_contents_essential))
            
            
                   
            
            # themes_index_title = themes_index.find('th', {'class': 'a-left'})
            # themes_index_contents = themes_index.find_all('td', {'class': 'ellipsis'})
            # print(themes_index_contents)
            # for v in themes_index_contents:
                # print(v.text)
            



class Stock:
    """Stock 관련 정보를 가져와서 보기 좋게 만들어서 뿌려준다.
    Themes 테마 관련주를 계속해서 뿌려줄 수 있도록 한다.
    테마 관련, 종목 관련, NoSQL MongoDB에 연동
    보기좋게 화면으로 뿌려준다. 오늘의 테마 및 테마 동향을 보고
    왜 그 주식이 좋은지 등 데이터를 이용하여서 보여줄 수 있도록 하자.
    데이터를 연결해야지만 좋은 결과를 낼 수 있다.

    매일 크롤링하는 모듈 하나
    유용한 정보를 return 하는 것 하나
    변경될 시 해당 값을 가져와서 저장하는 것 하나.

    크롤링이 필요함. DB에 계속 쌓는 과정이 필요함.
    DB 연결하는 부분도 추가

    Telegram 부분도 필요 에러가 났을 때 어떻게 대처해야하는지.

    각 모듈별로도 독립적으로 동작을 해야하며, Stock에서도 독립적으로 동작을 해야함.

    각 모듈의 관계에서도 DB를 사용할 수도 있지만.

    여러개를 엮어서 사용할 때는 Client 개념으로 DB, Crawling 등을 사용할 수 있지만,

    단독으로 사용할 때는 Module이라는 명칭을 사용하여서 독립적으로 사용가능하게 끔 만든다.

    User Scenario
    1. 매일 저녁 8시에 다음(daum) 증권에서 테마주 정보를 읽어서, DB(Mongo DB)에 저장을 한다. 그리고 그 정보를 읽어와서 보기 좋게(사용자/) 처리 후 json 형식으로 return 한다
     - 매일 저녁 8시에 실행
     - 다음 증권에서 테마주 정보를 읽어서: daum object를 만듦, request를 함. themes, all_stock 등 정보를 제공하는 class를 만듦
     - DB에 저장한다: MongoDB db에 값을 저장함.
     - db에서 정보를 읽어와서 보기좋게 처리(사용자/node.js): 보기좋게 처리 무슨객체임?


    """

    def __init__(self):
        pass

    def get_themes(self):
        headers = {
            "referer": "https://finance.daum.net/domestic/themes",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        }

        # url = 'https://finance.daum.net/api/themes/leading_stocks?page=2&perPage=30&fieldName=changeRate&order=desc&pagination=true'
        url = 'https://finance.daum.net/api/themes/leading_stocks?page=1&perPage=100&fieldName=changeRate&order=desc&pagination=true'
        r = requests.get(url, headers=headers)
        print(r.text)


if __name__ == '__main__':
    start = time.time()
    stock = Paxnet()
    stock.get_themes()
    end = time.time()
    print(f"{end - start:.5f} sec")


