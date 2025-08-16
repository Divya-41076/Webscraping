from bs4 import BeautifulSoup as bs
import requests

def insert_values(cur,table_name):
    count=0
    for page in range(1,3):
        source=requests.get(f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&postWeek=60&searchType=Home_Search&cboPresFuncArea=35&pDate=Y&sequence={page}&startPage=1")
        soup=bs(source.content, 'lxml')
        main_content=soup.find('ul', class_="new-joblist").find_all('li',class_='clearfix job-bx wht-shd-bx')       
        for each_job in main_content:
            job_title=each_job.h2.text.strip()
            company_name=each_job.h3.text.strip().replace('\r\n','').split('  ')[0]
            experience=each_job.ul.find_all('li')
            exp=experience[0].text.replace('card_travel','')
            if experience[1].find('i',class_="material-icons rupee"):
                salary=experience[1].text.replace("Rs ",'')
            else:
                salary="not disclosed"
            location=each_job.ul.span.text
            skills=each_job.find('ul',class_='list-job-dtl clearfix').find_all('li')[1].span.text.strip()
            print()

            count+=1
            print(f'Inserting TimesJobs- job {count} ',end="...")
            cur.execute(f"""
            INSERT INTO {table_name} VALUES
            ('{job_title[:80]}',
             '{company_name[:70]}',
             '{skills[:100]}',
             '{exp[:50]}',
             '{salary[:50]}',
             '{location[:100]}');""")
            
            print(f"job {count} inserted")
           
    return cur