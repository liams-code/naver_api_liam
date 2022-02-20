# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색

import os
import sys
import urllib.request
import pandas as pd
import json
import re

client_id = "WQ2aMcRNmsrSLswiiep4"
client_secret = "EpRI4HUUfY"

#코드 상에서 입력값을 넣어주는게 힘들어서 변수를 만들어서 입력하는 걸로 만듬
query = urllib.parse.quote(input("검색 입력란: "))

#검색값을 1000(최대값)을 받아올 수 있도록 함, display 100개 단위로 가져옴
index = 0
display = 100
start = 1
end = 1000

# 받아온 값을 print로 출력하는게 아니라 저장하는 함수 pandas에 이쁘게 저장(import 선언)
web_df = pd.DataFrame(columns=("Title", "Link", "Description"))

#for문 사용하여 1~1000,100개단위로 반복사용 , 탭사용하여 밑에 문장 for문 안으로 넣어줌.
for start_index in range(start, end, display):

  url = "https://openapi.naver.com/v1/search/blog?query=" + query \
        + "&display=" + str(display) \
        + "&start=" + str(start_index)

  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id",client_id)
  request.add_header("X-Naver-Client-Secret",client_secret)
  response = urllib.request.urlopen(request)
  rescode = response.getcode()
  #getcode사용해서 200 이면 응답을 받았다는 표시
  #파싱할려면 json 사용 - body가 자료를 딕셔너리 dict로 받아옴
  #우리가 필요한 자료는 items안에 key값 안에 있는 것을 반복적으로 다 받아와야 함.
  if(rescode==200):
      response_body = response.read()
      response_dict = json.loads(response_body.decode('utf-8'))
      items = response_dict['items']
      for item_index in range(0, len(items)):
        remove_tag = re.compile('<.*>?')
        title = re.sub(remove_tag, '', items[item_index]['title'])
        link = items[item_index]['link']
        description = re.sub(remove_tag, '', items[item_index]['description'])
        web_df.loc[index] = [title, link, description]
        index += 1
  else:
      print("Error Code:" + rescode)

web_df
