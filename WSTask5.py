from WSTask import *     
import requests        
from bs4 import BeautifulSoup as s  
from pprint import pprint
import json

def get_movie_list_details(movies):
    main=[]
    for i in movies[:10]:
        link=i["movie_link"]
        di=scrape_movie_details(link)
        main.append(di)
    return main
def scrape_movie_details(link):
    page=requests.get(link) 
    soup=s(page.text,"html.parser")
    d={}         
    body_of_web=soup.find("body")
    d['Name']=body_of_web.find("h1").text[:-8] 
    d['Year']=int(body_of_web.h1.span.a.text)

    d['director']=body_of_web.find('div',class_="plot_summary").find('div',class_='credit_summary_item').a.text

    # director = body_of_web.find("div",class_="credit_summary_item") 
    # director_list=director.findAll('a')
    # d['director']=[i.text.strip() for i in director_list] 

    d['bio'] = body_of_web.find("div",class_="summary_text").text.strip()    
    d['gerne']=body_of_web.find_all("div",class_="see-more inline canwrap")[-1].a.text   
    
    d['country']=body_of_web.find_all('div',class_="txt-block")[5].text.strip().split('\n')[1]
    d['language']=body_of_web.find_all('div',class_="txt-block")[6].text.strip().split('\n')[1]

    # country=body_of_web.find("div",attrs={"class":'article','id':'titleDetails'})
    # more=country.findAll("div")
    # for i in more:
    #     tag=i.findAll("h4")
    #     for text in tag:
    #         if 'Language:' in text:
    #             tag2=i.findAll('a')
    #             d['language']=[language.text for language in tag2] 
    #         elif "Country:" in text:
    #             tag2=i.findAll('a')
    #             d['country']=[''.join(country.text) for country in tag2]  
    
    d['img link']='https://www.imdb.com/'+(body_of_web.find_all("div",class_="poster")[0].a['href'])

    sub = body_of_web.find('div', class_ = 'subtext').time.text.strip() 
    time_m = int(sub[0])*60
    ep=sub.split(' ')
    fl=ep[1].split('min')[-2] 
    d['rune time'] = time_m + int(fl)

    # time=body_of_web.find("div",class_='subtext').time.text.strip()
    # time2=int(time[0])*60
    # if 'min' in time:
    #     b=time.strip('min').split('h')
    #     d['run time']=str(time2+int(b[1]))+' minutes'

    return d
get_movie_list_details(scrape_top_list())