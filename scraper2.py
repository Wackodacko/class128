from typing import final
from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import csv
import requests

START_URL="https://exoplanets.nasa.gov/exoplanet-catalog"
broswer=webdriver.Chrome("C:/Users/anaeo/Downloads/chromedriver")
broswer.get(START_URL)
time.sleep(10)
headers=["name","light_years_from_earth","planet_mars","stellar_magnitude","discovery_data","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]
planet_data=[]
new_planet_data=[]

def scrape():

    for i in range(0,489):
        soup=BeautifulSoup(broswer.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tag=ul_tag.find_all("li")
            temp_list=[]
            for index,li_tag in enumerate(li_tag):
                if index==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag=li_tag[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            planet_data.append(temp_list)
        #going to the next page
        broswer.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    # with open("scraper2.csv","w") as f:
    #     csvwriter=csv.writer(f)
    #     csvwriter.writerow(headers)
    #     csvwriter.writerows(planet_data)

def scrape_more_data(hyperlink):
    page=requests.get(hyperlink)
    soup=BeautifulSoup(page.content,"html.parser")
    for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
        td_tags=tr_tag.find_all("td")
        temp_list=[]
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
        new_planet_data.append(temp_list)


scrape()

for data in planet_data:
    scrape_more_data(data[5])

final_planet_data=[]
for index, data in enumerate(planet_data):
    final_planet_data.append(data+final_planet_data[index])
with open("scraper2.csv","w") as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)