import re
import requests
from tsv_trimmer import trimmer

from bs4 import BeautifulSoup

"""리스트, 파일 초기화"""
urls_list = []
with open('result.tsv', 'w') as f:
    f.write("")

i = 1
while i <= 5:
    """url 접속"""
    url = f"https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt&relRadio=&orgFullName=%ED%95%9C%EA%B5%AD%ED%99%98%EA%B2%BD%EA%B3%B5%EB%8B%A8&orgFilter=%ED%95%9C%EA%B5%AD%ED%99%98%EA%B2%BD%EA%B3%B5%EB%8B%A8&org=%ED%95%9C%EA%B5%AD%ED%99%98%EA%B2%BD%EA%B3%B5%EB%8B%A8&orgSearch=&currentPage={i}&perPage=40&brm=&instt=&svcType=&kwrdArray=&extsn=&coreDataNmArray=&pblonsipScopeCode="
    res = requests.get(url)
    res.raise_for_status()

    """bs4 객체로 변환"""
    soup = BeautifulSoup(res.text, "lxml")

    """링크 스크랩"""
    results_list = soup.find_all("a", {"href": re.compile(r'/data/*')})
    for result in results_list:
        urls_list.append(f"https://www.data.go.kr{result['href']}")

    i += 1

progress = 1
p = re.compile("^한국환경공단_")
for url in urls_list:
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    titles_list = soup.find_all("p", attrs={"class": "tit"})
    content = soup.find("div", attrs={"class": "cont"}).get_text()

    content = re.sub("\.", ". ", content)
    content = content.strip()
    content = re.sub(",", ", ", content)
    content = re.sub(" {2,99}", " ", content)
    content = re.sub(" 입니다\.|입니다\.|이다|합니다\.", ".", content)
    content = re.sub("있습니다\.", "있음.", content)
    content = re.sub("말함", "말함.", content)
    content = re.sub("[ ]+\([ ]+", "(", content)
    content = re.sub("[ ]*_[ ]* ", "_", content)
    content = f"{content}."
    content = re.sub("\.{2,99}", ".", content)

    hyperlink = re.compile(r'([a-zA-Z0-9]+.) ([a-zA-Z0-9]+.) ([a-zA-Z0-9]+.) ([a-zA-Z0-9]+)')
    if hyperlink.search(content):
        content = re.sub(hyperlink,
                         f"{hyperlink.search(content).group(1)}{hyperlink.search(content).group(2)}{hyperlink.search(content).group(3)}{hyperlink.search(content).group(4)}",
                         content)

    for title in titles_list:
        if p.match(title.get_text()):
            title = title.get_text().lstrip("한국환경공단_")
            title = re.sub(" {2,99}", " ", title)

            print(f"title: {title}")
            print(f"content: {content}")

            with open("result.tsv", "a", encoding="utf8") as f:
                f.write(f"{title}\t{content}\n")

            print(f"Progress: {progress}/{len(urls_list)}\n")
            progress += 1

trimmer('result.tsv')
