from bs4 import BeautifulSoup as bs
import requests
from db_config import search_query

def insert_values(cur, table_name):
    matched, unmatched = 0, 0
    for page in range(1, 3):
        source = requests.get(
            f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&postWeek=60&searchType=Home_Search&cboPresFuncArea=35&pDate=Y&sequence={page}&startPage=1"
        )
        soup = bs(source.content, 'lxml')
        jobs = soup.find('ul', class_="new-joblist").find_all('li', class_='clearfix job-bx wht-shd-bx')       

        for each_job in jobs:
            job_title = each_job.h2.text.strip()
            company_name = each_job.h3.text.strip().replace('\r\n','').split('  ')[0]
            exp = each_job.ul.find_all('li')[0].text.replace('card_travel','')

            salary = "not disclosed"
            if each_job.ul.find_all('li')[1].find('i', class_="material-icons rupee"):
                salary = each_job.ul.find_all('li')[1].text.replace("Rs ",'')
            
            location = each_job.ul.span.text
            skills = each_job.find('ul', class_='list-job-dtl clearfix').find_all('li')[1].span.text.strip()

            if search_query.lower() not in job_title.lower() and search_query.lower() not in skills.lower():
                unmatched += 1
                print(f"⚠️ Unmatched TimesJobs job: '{job_title}' (not containing '{search_query}')")
                continue

            matched += 1
            print(f"✅ Saving TimesJobs job {matched} ...")
            cur.execute(f"""
            INSERT INTO {table_name} VALUES
            ('{job_title[:80]}',
             '{company_name[:70]}',
             '{skills[:100]}',
             '{exp[:50]}',
             '{salary[:50]}',
             '{location[:100]}');""")

    print(f"TimesJobs: Matched {matched}, Unmatched {unmatched}")
    return cur, matched, unmatched
