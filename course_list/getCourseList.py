'""Get HKU CS course list.""'
from bs4 import BeautifulSoup
import requests
import json
from pprint import pprint

course_list = []  # Structure: [course1, course2, ...]
url = 'http://www.cs.hku.hk/programme/courses-offered.jsp'
data = requests.get(url).text.encode('utf-8').decode('ascii', 'ignore')
soup = BeautifulSoup(data, 'html.parser')
table = soup.find_all(name='table', border='1', width='99%', class_='table')[1]
for tr in table.findAll('tr'):
    td_list = tr.findAll('td')
    if len(td_list) == 4:
        course_code = td_list[0].string
        course_title = td_list[1].string
        term = td_list[2].string.strip()
        staff = td_list[3].findAll(text=True)[0]
        course_list.append({
            'course_code': course_code,
            'course_title': course_title,
            'term': term,
            'staff': staff
        })

pprint(course_list[1:len(course_list)])
with open('course_list.txt', 'w') as outfile:
    json.dump(course_list, outfile)
