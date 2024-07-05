from bs4 import BeautifulSoup as bs
import requests
import mysql.connector




for page in range(1,6):


    source=requests.get(f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&postWeek=60&searchType=Home_Search&cboPresFuncArea=35&pDate=Y&sequence={page}&startPage=1")

    soup=bs(source.content, 'lxml')

    main_content=soup.find('ul', class_="new-joblist").find_all('li',class_='clearfix job-bx wht-shd-bx')
    print(len(main_content))

    for each_job in main_content:
    # print(each_job)
        job_title=each_job.h2.text.strip()
        company_name=each_job.h3.text.strip().split('  ')[0]

        experience=each_job.ul.find_all('li')
        exp=experience[0].text.replace('card_travel','')
        salary=experience[1].text.replace('Rs ','')

        loc=each_job.ul.span.text
        skills=each_job.find('ul',class_='list-job-dtl clearfix').find_all('li')[1].span.text.strip()
 
        print(f"Job_title:{job_title.rjust(10)}   Company_name:{company_name}Experience:{exp.rjust(10)}   Skills:{skills[:len(skills)-1].rjust(10)}   Salary:{salary.rjust(10)}   Location:{loc}")
        print('---------------------------------------------------------------------------')


