import requests
from bs4 import BeautifulSoup
import csv
import re
import time

start_time = time.time()
url = 'https://mydramalist.com/people/top'
response = requests.get(url)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')
    total_records=soup.find('p',{'class':'m-b-sm pull-right'}).text
    
    total_rec=int(int(re.findall("(\d+)",total_records)[0])/20)+1
    
    counter=1
    while counter<101:
        
        url="https://mydramalist.com/people/top?page="+str(counter)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        
        

    
    
    
        links=soup.find_all('h6',{'class':'text-primary title'})
        

        with open('drama_list_soup.csv', 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
        
            
            
            for link in links:
                data=[]
                link=link.find('a')['href']
                link="https://mydramalist.com"+link
                
                page=requests.get(link)
                soup = BeautifulSoup(page.text, 'html.parser')
                
                table=soup.find('table',{'class':'table film-list'})
                trs=table.find_all('tr')[1]
                tds=trs.find_all('td')
                for td in tds:
                    value=td.text.split('\n')
                    for val in value:
                        data.append(val)
                csv_writer.writerow(data)
                
                
                print(counter, link)

        
                counter=counter+1

    end_time = time.time()

    print("Runtime BeautifulSoup", end_time - start_time)

 

else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
