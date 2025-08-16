from bs4 import BeautifulSoup
import requests
from db_config import search_query

def insert_values(cur, table_name):
    matched, unmatched = 0, 0
    for each_page_no in range(1, 3):
        page_data = requests.get(f"https://internshala.com/jobs/page-{each_page_no}").content
        soup = BeautifulSoup(page_data, 'lxml')

        data = soup.find_all(
            'div',
            class_='container-fluid individual_internship view_detail_button visibilityTrackerItem'
        )
        
        for each_job in data:
            jobdetail_page_link = str(each_job.get("data-href"))
            job_title = each_job.h3.text.strip()
            company_name = each_job.p.text.strip()
            location = each_job.span.a.text.strip()
            experience = each_job.find('div', class_="item_body desktop-text").text
            salary = each_job.find('span', class_="mobile").text.strip()

            jobdetail_page = requests.get(f"https://internshala.com{jobdetail_page_link}")
            soup = BeautifulSoup(jobdetail_page.text, 'lxml')
            idetails = soup.find('div', id="content").find('div', class_="round_tabs_container")

            skills = ",".join([span_tag.text for span_tag in idetails.find_all('span', class_="round_tabs")])

            if search_query.lower() not in job_title.lower() and search_query.lower() not in skills.lower():
                unmatched += 1
                print(f"⚠️ Unmatched Internshala job: '{job_title}' (not containing '{search_query}')")
                continue

            matched += 1
            print(f"✅ Saving Internshala job {matched} ...")
            cur.execute(f"""
            INSERT INTO {table_name} VALUES
            ('{job_title[:80]}',
             '{company_name[:70]}',
             '{skills[:100]}',
             '{experience[:50]}',
             '{salary[:50]}',
             '{location[:100]}');""")

    print(f"Internshala: Matched {matched}, Unmatched {unmatched}")
    return cur, matched, unmatched
