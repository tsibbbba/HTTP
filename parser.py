from bs4 import BeautifulSoup
import requests
import argparse
import sys
import matplotlib.pyplot as plt

def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('surname', nargs=3, type=str, help='teacher surname')
    parser.add_argument('date', nargs=3, help='date: year, month, number. for example 2023 3 13 -> 13 Marсh 2023')
    return parser


if __name__ == '__main__':
    args = parsing().parse_args(sys.argv[1:])
    print(args.surname)
    print(args.date)
    url = 'https://ruz.spbstu.ru/search/teacher?q=' + args.surname[0] + '%20' + args.surname[1] + '%20' + args.surname[2]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    surnames = soup.find_all("a", class_="search-result__link")
    for surname in surnames:
        continue_url = surname['href']

    new_url = 'https://login.dnevnik.ru/login'
    print(new_url)
    page = requests.get(new_url)
    soup = BeautifulSoup(page.text, "html.parser")

    quotes = soup.find_all('span', class_='lesson__time')
    subjects = soup.find_all('li', class_='lesson')
    results = soup.find_all(lambda tag: tag.name == 'li' and
                            tag.get('class') == ['lesson__time']
                            or tag.get('class') == ['lesson__subject']
                            or tag.get('class') == ['lesson__places']
                            or tag.get('class') == ['schedule__date']
                            or tag.get('class') == ['page__h3']
                            or tag.get('class') == ['lesson__teachers'])

    all_timetable = []
    for result in results:
        all_timetable.append(result.text)
        print(result.text)


    tmp1 = soup.find_all('li', class_='schedule__day')
    day_of_week = []
    count_of_pair = []

    for t in tmp1:
        day_of_week.append(t.find('div', class_="schedule__date").text)
        count_of_pair.append(len(t.find_all('li', class_='lesson')))

    plt.bar(day_of_week, count_of_pair)
    plt.xlabel('День недели')
    plt.ylabel('Кол-во пар')
    plt.title('График зависимости кол-ва пар от дня недели')
    plt.show()


