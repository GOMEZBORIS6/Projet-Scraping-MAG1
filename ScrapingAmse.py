#----------------------------------------------------------------------------------------------------------
# Gomez Boris Jean-Baptiste 
# Student of the University of Aix Marseille 
# First year of Magistere engineer Economist
# Scrpaing Project
#--------------------------------------------------------------------------------------------------------------------------------
import requests as rq
from bs4 import BeautifulSoup
from dataclasses import dataclass
import dateparser
import csv
import pandas as pd
import os
from datetime import datetime, timedelta
import time


###For test my code directly

titlelist = []
pointlist = []
authorlist = []
hourlist = []
listhoursfinale = []
numberOfCommentslist = []


labels = ["names", "points", "author", "date_published", "number_of_comments"]


@dataclass
class Post:
    # names: str
    # points: str
    # author: str
    # date_published: str
    # number_of_comments: str
    def recuperation_htmlpage(self, myurl):
        htmlcode = rq.get(url=myurl).text
        page = BeautifulSoup(htmlcode, "html.parser")
        return page

    def extraire_donnees(self, elements):
        resultat = []

        for element in elements:
            resultat.append(element.string)
        return resultat

    def converterhoursTodate(self, listhours1):
        listhours2 = []
        for datestring in listhours1:
            dt = dateparser.parse(datestring)
            listhours2.append(dt.strftime("%d-%m-%Y"))
        return listhours2


# for j in range(30):
#     Boris = Post(names=listdico[j]["names"],points=listdico[j]["points"],author=listdico[j]["author"],date_published=listdico[j]["date_published"],
#                  number_of_comments=listdico[j]["number_of_comments"])
#     #print(Boris.__dict__)

Boris = Post()

scrap_url = ["https://news.ycombinator.com/"]

fileName = r"scrapingAmse.csv"
reponse = os.path.exists(fileName)

if reponse == True:
    os.remove(fileName)  # remove the file is exists
#   print("tata")

for i in range(5):

    soup = Boris.recuperation_htmlpage(
        scrap_url[i]
    )  # scrap_url is a list of all url page for len of the range above

    url_links = [a["href"] for a in soup.find_all("a", class_="morelink", href=True)]

    scrap_url.append(scrap_url[0] + url_links[0])

    url_links = []

    ## Print all the title on the homepage (30 names) with BeautifulSoup

    # AllTitle = soup.find_all("a", class_="titlelink")
    # for Title in AllTitle:
    #     print(Title.get_text())

    divs = soup.find_all("tr", class_="athing")

    # to recover the name or title
    for div in divs:
        tb = div.find_all("a", class_="titlelink")
        titlelist.append(Boris.extraire_donnees(tb)[0])

    tds = soup.find_all("td", class_="subtext")

    # to recover the points and the authors
    for row in tds:
        points = row.find_all("span", class_="score")
        authors = row.find_all("a", class_="hnuser")
        if len(points):
            pointlist.append(Boris.extraire_donnees(points)[0])

        else:
            points = ["None"]  # put None if there is no such information
            pointlist.append(points[0])
        if len(authors):
            authorlist.append(Boris.extraire_donnees(authors)[0])

        else:
            authors = ["None"]  # put None if there is no such information
            authorlist.append(authors[0])

    link = []

    # to recover the number of comments
    for raw in tds:

        for line in raw.find_all("a"):
            hrefa = line.get("href")
            classe = line.get("class")
            if classe is None and (
                "item?" in hrefa
            ):  # we have noticed that the comment number tag (balise) does not have a class
                link.append(
                    line.get_text()
                    .replace("\xa0", " ")
                    .encode("utf-8")
                    .decode()  # we encode in utf8 and we remove the b of binary byte using decode
                )
        if len(link) != 2:
            link.append("None")  # put None if there is no such information

        numberOfCommentslist.append(link[1])
        link = []

    date_publish = soup.find_all("span", class_="age")

    for hours in date_publish:
        hrs = hours.find_all("a")
        hourlist.append(Boris.extraire_donnees(hrs)[0])

    listhoursfinale = Boris.converterhoursTodate(hourlist)

    listarticles = []

    for j in range(30):
        dico = {}
        dico["names"] = titlelist[j]
        dico["points"] = pointlist[j]
        dico["author"] = authorlist[j]
        dico["date_published"] = listhoursfinale[j]
        dico["number_of_comments"] = numberOfCommentslist[j]
        listarticles.append(dico)
    # print(listarticles)

    # listarticles is a list of dictionnary of each article

    ## Write data in CSV
    try:
        with open("scrapingAmse.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=labels)
            writer.writeheader()
            for article in listarticles:
                writer.writerow(article)

    except IOError:
        print("I/O error")
    print(f"I finish the creation of csvfile for page {i}")


# Visualization of data in CSV

data = pd.read_csv("scrapingAmse.csv", encoding="latin1")
print(data)


###For turn the code each hours

# while 1:
#     # print('Run something..')
# #######    [Put my code here for turning each hours] ########
#     dt = datetime.now() + timedelta(hours = 1)

#     while datetime.now() < dt:
#         time.sleep(1)


# -------------------------------------------------- end of code
