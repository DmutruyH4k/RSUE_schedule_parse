# To-Do:
#   Сделать поиск расписания по группе (Пример: ИБ-321 (Факультет: 3, Курс: 2, Группа: 7)
import requests
from bs4 import BeautifulSoup
from payload import url, data, headers


def download_page():
    response = requests.post(url=url, headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', id='content').find_all('div', class_='container')[1]
    return content


def parse_schedule(content):
    weeks = [i.text for i in content.find_all_next('h1', class_='ned')]
    weeks_schedules = content.find_all_next('div', class_='col-lg-2 col-md-2 col-sm-2')
    days = []
    for day in weeks_schedules:
        days.append([i for i in day.get_text().split('\n') if i != ''])
    start_week_index = 0
    for week in weeks:
        print('~' * 50, week, '~' * 50)
        for i in range(start_week_index, len(days)):
            day = days[i]
            print('#' * 50, day[0], '#' * 50)
            for j in range(1, len(day), 5):
                time = day[j][:day[j].find('П')]
                group = day[j][day[j].rfind(':')+2:] if day[j].find('П') != -1 else "обе"
                lesson_name = day[j + 1]
                tutor = day[j + 2]
                classroom = day[j + 3][day[j + 3].find('.') + 1:] if day[j + 3].count('д') == 1 else 'Дистанционно'
                lesson_type = day[j + 4]
                print(f'{time}\n'
                      f'\tДисциплина: {lesson_name}\n'
                      f'\tПодгруппа: {group}\n'
                      f'\tПреподаватель: {tutor}\n'
                      f'\tАудитория: {classroom}\n'
                      f'\tТип занятия: {lesson_type}')
            if day[0] == 'Суббота':
                start_week_index = i+1
                break


def main():
    schedule = download_page()
    parse_schedule(schedule)


if __name__ == '__main__':
    main()
