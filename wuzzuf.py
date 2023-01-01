#1st step install and import modules
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
job_title = []
company_name = []
location_name = []
skills = []
links = []
salary = []
responsibilities = []
date = []
#2nd step use requests to fetch the url
result = requests.get("https://wuzzuf.net/search/jobs/?q=graphic+designer&a=hpb")
#3rd step save page content/markup
src = result.content
#4th step create soup object to parse content
soup = BeautifulSoup(src , "lxml")
#5th step find the elements containing info we need
#-- job titles, job skills, company names, location names الحاجات اللى احنا عايزينها
job_titles = soup.find_all("h2" , {"class":"css-m604qf"} )
company_names = soup.find_all("a" , {"class":"css-17s97q8"} )
locations_names = soup.find_all("span" , {"class":"css-5wys0k"})
job_skills = soup.find_all("div" , {"class":"css-y4udm8"})
posted_new = soup.find_all("span" , {"class" : "css-do6t5g"})
posted_old = soup.find_all("span" , {"class" : "css-do9k5g"})
posted = [*posted_new, *posted_old]
#6th step loop over returned lists to extract needed info into other lists
for i in range(len(job_titles)):
    job_title.append(job_titles[i].text)
    links.append(job_titles[i].find("a").attrs['href'])
    company_name.append(company_names[i].text)
    location_name.append(locations_names[i].text)
    skills.append(job_skills[i].text)
    date_text = posted[i].text.replace("-" , "").strip()
    date.append(date_text)
    
for link in links:
    result = requests.get('https://wuzzuf.net' + link)
    src = result.text
    soup = BeautifulSoup(src , "lxml")
    salaries = soup.find("span" , {"class" : "css-4xky9y" })
    print(salaries)
    salary.append(salaries.text.strip())
    requirements = soup.find("span" , {"itemprop" : "responsibilities"}).ul
    respon_text = ""
    for text in requirements.find_all("li"):
        respon_text += text.text+"| "
        respon_text = respon_text[:-2]
    responsibilities.append(respon_text)
#7th step create csv file and fill it with values
file_list = [job_title , company_name , location_name , skills , links , salary , responsibilities , date]
exported = zip_longest(*file_list) #دي الفانكشن اللى بتجيب واحد من كل ليسته جنب بعض 
with open("E:\programming\web scraping\jobstutorial.csv" , "w" ) as myfile :
    wr = csv.writer(myfile)
    wr.writerow(["job title" , "company name" , "location" , "skills" , "links" , "salary" , "responsibilities" , "date"])
    wr.writerows(exported)




