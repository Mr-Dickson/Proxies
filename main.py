import requests as req
from bs4 import BeautifulSoup
import csv


html_text = req.get("https://free-proxy-list.net/").text

#function to extract text from tags
def extract(tag: BeautifulSoup):
  return tag.text


#Parse html with beautiful soup
soup = BeautifulSoup(html_text, "lxml")
table = soup.find("tbody")
table_rows = table.find_all("tr")

for row in table_rows:
  row_data = row.findAll('td')
  if row_data[5].text and row_data[6].text == "yes":
    row_data = list(map(extract, row_data))
    ip = row_data[0]
    port = row_data[1]
    proxy_server = {
      "https" : "{}:{}".format(ip, port)
    }

    #Save good proxies to a working.csv file
    try:
      if req.get("https://www.google.com/", proxies=proxy_server, timeout= 3).status_code == 200:
        with open("./working.csv" , 'a') as wf:
          writer = csv.writer(wf)
          writer.writerow([f"{ip}", f"{port}"])
      elif req.get("https://www.google.com/", proxies=proxy_server ).status_code == 429:
        pass
    except Exception:
      pass
  else:
    continue