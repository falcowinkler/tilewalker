import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import csv
import re


def save_config(current_num):
    with open("config", 'w') as config_file:
        config_file.write(str(current_num))


def get_current_number():
    try:
        with open("config") as config_file:
            current_number = int(config_file.readlines()[0])
    except FileNotFoundError:
        current_number = 1
        save_config(current_number)
    return current_number


def scrape(current_number):
    url = "http://www.nmaps.net/" + str(current_number)
    try:
        content = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return None, None

    soup = BeautifulSoup(content, 'html.parser')

    data = soup.find("textarea", attrs={'rows': '1'})
    if data is not None:
        data = data.contents[0]
    else:
        return None, None

    tr_s = soup.find("table", attrs={'class': 'formtable'}).find_all("tr")
    tags = []

    for x in tr_s[1].td.find_all("a"):
        if len(x.contents) > 0:
            tags.append(x.contents[0])

    rating = None
    for i in range(1, 6):
        rating = soup.find("div", attrs={'class': 'rated' + str(i)})
        if rating is not None:
            rating = rating.contents[0]
            break

    if rating is not None:
        tags.append("rating:" + str(rating))

    tags.append("id:" + str(current_number))
    return data, tags


def persist(data, labels, csvfile):
    spamwriter = csv.writer(csvfile, delimiter=';')
    spamwriter.writerow((data, ",".join(labels)))


def data_in_expected_format(data):
    try:
        match = re.match(".*#.*#.*#([0-9A-Q@;:y=?<>]{713})|", data).group(1)
        return match is not None
    except:
        return False


if __name__ == '__main__':
    current_no = get_current_number()
    with open("numa_archive.csv", "a", newline="") as csvfile:
        while current_no < 300000:
            data, labels = scrape(current_no)
            if data is not None:
                data = data.replace('\n', ' ').replace('\r', '')
                if data_in_expected_format(data):
                    print("Crawled map " + str(current_no))
                    persist(data, labels, csvfile)
            current_no += 1
            save_config(current_no)
