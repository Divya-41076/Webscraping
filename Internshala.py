from bs4 import BeautifulSoup
import lxml
import requests

def insert_values(cur,table_name):
    count=0
    # Loop for each page numbers
    for each_page_no in range(1,3):

        # Getting the listed jobs on each page
        each_page_request_data=requests.get(f"https://internshala.com/jobs/page-{each_page_no}").content
        soup=BeautifulSoup(each_page_request_data,'lxml')
        soup.prettify()

        data=soup.find_all('div',class_='container-fluid individual_internship view_detail_button visibilityTrackerItem')
        
        for each_job in data:
            jobdetail_page_link=str(each_job.get("data-href")) #to get the link of the each job details page
            job_title=each_job.h3.text.strip() #jobtitle
            company_name=each_job.p.text.strip() #jobcompany
            location=each_job.span.a.text.strip() #joblocation
            experience=each_job.find('div',class_="item_body desktop-text").text #jobexperience
            salary=each_job.find('span',class_="mobile").text.strip() #jobsalary

            jobdetail_page=requests.get(f"https://internshala.com{jobdetail_page_link}")
            soup=BeautifulSoup(jobdetail_page.text,'lxml')

            content=soup.find('div',id="content")
            idetails=content.find('div',class_="round_tabs_container")

            list_of_skills=[]
            for span_tag in idetails.find_all('span',class_="round_tabs"):
                list_of_skills.append(span_tag.text)
            skills=",".join(list_of_skills)  #jobskills
            print()
            count+=1
            print(f"Inserting Internshala: job {count} ",end="...")
            cur.execute(f"""
            INSERT INTO {table_name} VALUES
            ('{job_title[:80]}',
             '{company_name[:70]}',
             '{skills[:100]}',
             '{experience[:50]}',
             '{salary[:50]}',
             '{location[:100]}');""")
            
            print(f"job {count} inserted")
    return cur