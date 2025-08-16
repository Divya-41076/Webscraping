
# 🛠 JobScraper – Multi-Portal Job Scraping with MySQL

A Python-based job scraper that extracts job opportunities from **Internshala, TimesJobs, and BigShyft** using **BeautifulSoup** and stores the results in a **MySQL database**.  
The tool helps filter relevant jobs by keyword (e.g., *Python, Data Scientist*) and provides a clear summary of matched vs. unmatched job postings.

---

## 🚀 Features
- 🔍 Scrapes jobs from three major job portals
- 📂 Extracts **Job Title, Company, Skills, Experience, Salary, Location**
- ⚡ Filters jobs based on a search keyword (`search_query` in config)
- 💾 Saves matched jobs into **MySQL**
- 📊 Logs real-time progress with ✅ *Matched* / ⚠️ *Unmatched* indicators
- 📈 Provides a final scraping summary
- 🔒 Secure credential management with `.gitignore` for sensitive files

---

## 📂 Project Structure

```
JobScraper/
│── scrapers/
│   ├── internshala.py
│   ├── timesjobs.py
│   ├── bigshyft.py
│── db/
│   ├── db_config_example.py   <- Template for DB credentials
│   ├── db_config.py           <- User’s private DB credentials (gitignored)
│── main.py                    <- Entry point to run scraper
│── requirements.txt           <- Python dependencies
│── README.md                  <- Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```
git clone https://github.com/yourusername/JobScraper.git
cd JobScraper
```

### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 3️⃣ Configure Database Credentials
`db_config.py`:

```
# db_config.py
MYSQL_HOST = "localhost"
MYSQL_USER = "your_username"
MYSQL_PASSWORD = "your_password"
MYSQL_DATABASE = "jobscraper"
```
---

## ▶️ How to Run

Run the script:

```
python main.py
```

The script will:

1. Connect to MySQL using credentials in `db_config.py`
2. Create database & table (if not already existing)
3. Scrape jobs from **Internshala, TimesJobs, and BigShyft**
4. Insert matched jobs into MySQL
5. Print a final summary

---

## 📊 Example Output

```
[Internshala]  ✅ Matched: Python Developer at XYZ Ltd
[TimesJobs]   ⚠️ Unmatched: Java Developer at ABC Corp
[BigShyft]    ✅ Matched: Data Scientist at PQR Tech

✅ Total Matched Jobs: 7
⚠️ Total Unmatched Jobs: 5
```

---

## 📂 Viewing Results in MySQL

After running the script, log into MySQL:

```
USE jobscraper;
SELECT * FROM job_listings;
```

---

## 🔮 Future Improvements
- ✅ Add support for more job portals (**LinkedIn, Indeed, Naukri**)
- ✅ Export results to **CSV/Excel**
- ✅ Add job auto-scheduling with **cron / Task Scheduler**
- ✅ Web dashboard with **Flask/Django**

---
👨‍💻 Developed with ❤️ using Python, BeautifulSoup, and MySQL
