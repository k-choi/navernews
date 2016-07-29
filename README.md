# Naver News Library

A simple Python library to scrape naver news with multi-threaded downloading.

# Dependencies
* requests
* lxml

# Usage

~~~{.python}
import navernews

l_article = []

from datetime import datetime
str_sid1 = '101'
#start from 2016/4/14 and go back to 2016/4/14
dt_org = datetime(2016,4,15)
dt_end = datetime(2016,4,14)
def mongo_callback(article, article_id):
    l_article.append((article_id,article))
navernews.download_naver_news_date_range(str_sid1, dt_org, dt_end, mongo_callback)
~~~

Output:
> 2016-04-14<br/>
324/324 100.00%<br/>
2016-04-13<br/>
247/247 100.00%

~~~{.python}
article_id, article = l_article[0]
print article['textv1']
~~~

Output:
> 20대 국회의원 선거 결과 유력 정치인들의 희비가 엇갈리면서 14일 관련 테마주도 요동을 쳤다. 예상을 뛰어넘는 성과를 거둔 더불어민주당과 국민의당 관련주는 급등했고, 참패한 새누리당 관련주는 급락했다.<br/>
이날 가장 눈에 띈 종목은 안철수 테마주였다. 국민의당 안철수 공동대표가 설립한 안랩의 주가는 장이 시작하자마자 21% 이상 치솟았다. 이후 차익 물량이 상승분을 반납해 전날보다 1.71%만 오른 채 마감했다. 역시 안철수 테마주로 꼽히는 써니전자와 다믈멀티미디어도 장 초반 각각 17%, 15% 올랐다. 그러나 갈수록 주가가 빠져 각각 0.74%, -6.18%의 등락률로 장을 마쳤다.<br/>
더민주의 ‘문재인 테마주’는 대부분 큰 폭으로 상승했다. 우리들휴브레인 주가가 15%나 올랐고 우리들제약, 에이엔피 등도 2∼5% 상승했다.<br/>
반면 새누리당 김무성 대표의 부친이 설립한 전방의 주가는 18.65%나 빠졌다. 엔케이(-20.4%), 디지틀조선(-18.59%), 조일알미늄(-17.09%) 등 다른 김무성 테마주들도 급락세를 빚었다.<br/>
한편 이날 코스피는 중국발 훈풍에 급반등해 2010선을 돌파했다. 코스피는 전날보다 34.61포인트(1.75%) 오른 2015.93으로 장을 마쳤다. 연중 최고치이자 지난해 12월1일(2023.93) 이후 가장 높은 수치다. 김정현 IBK투자증권 연구원은 “중국 수출 지표의 호조세, 유가 반등세 등으로 위험자산 선호 심리가 강화됐고, 외국인 매수세가 지수를 끌어올렸다”고 분석했다.<br/>
이진경 기자 ljin@segye.com<br/>
ⓒ 세상을 보는 눈, 글로벌 미디어

# Installation
Run the following command to install this library.

~~~
sudo python setup.py install
~~~
