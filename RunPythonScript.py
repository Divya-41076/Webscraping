import mysql.connector
import sys
import Internshala
import BigShyft
import TimesJobs
from db_config import db_config, database_name, table_name

global mydb

stats = {
    "Internshala": {"matched": 0, "unmatched": 0},
    "TimesJobs": {"matched": 0, "unmatched": 0},
    "BigShyft": {"matched": 0, "unmatched": 0},
}

def If_database_exist():
    global mydb

    def If_connection_established():
        try:
            global mydb 
            mydb = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"]
            )
            return mydb.is_connected()
        except mysql.connector.Error as err:
            print(f'❌ Unable to Establish Connection: {err}')
            return False
    
    def Initiate_values(cur, table_name):
        global stats, mydb
        cur, m, u = Internshala.insert_values(cur, table_name)
        stats["Internshala"]["matched"] += m
        stats["Internshala"]["unmatched"] += u
        mydb.commit()

        cur, m, u = TimesJobs.insert_values(cur, table_name)
        stats["TimesJobs"]["matched"] += m
        stats["TimesJobs"]["unmatched"] += u
        mydb.commit()

        cur, m, u = BigShyft.insert_values(cur, table_name)
        stats["BigShyft"]["matched"] += m
        stats["BigShyft"]["unmatched"] += u
        mydb.commit()
        return cur
    
    if If_connection_established():
        print("✅ Connection Established!")
        cur = mydb.cursor()
        cur.execute('SHOW DATABASES;')
        databases = [row[0] for row in cur.fetchall()]
        
        if database_name in databases:
            print(f"📂 Database '{database_name}' exists")
            cur.execute(f"USE {database_name}")
        else:
            print(f"🚀 Creating database '{database_name}'")
            cur.execute(f"CREATE DATABASE {database_name}")
            cur.execute(f"USE {database_name}")

        cur.execute("SHOW TABLES;")
        tables = [table[0] for table in cur.fetchall()]

        if table_name in tables:
            print(f"🗑 Table '{table_name}' exists. Truncating...")
            cur.execute(f"TRUNCATE {table_name};")
            mydb.commit()
        else:
            print(f"🆕 Creating table '{table_name}'...")
            cur.execute(f"""
                CREATE TABLE {table_name} (
                    JOB_TITLE VARCHAR(80),
                    COMPANY_NAME VARCHAR(70),
                    SKILLS VARCHAR(200) DEFAULT NULL,
                    EXPERIENCE VARCHAR(50) DEFAULT NULL,
                    SALARY VARCHAR(50),
                    LOCATION VARCHAR(200)
                );
            """)
            mydb.commit()

        print("⚡ Starting Web Scraping...")
        cur = Initiate_values(cur, table_name)
        return cur
    else:
        print("❌ Unable to connect. Check your db_config.py settings.")
        sys.exit(-1)


print("🔗 Establishing Connection...")
cur = If_database_exist()
mydb.commit()
mydb.close()

print("\n📊 Final Scraping Summary:")
total_matched = total_unmatched = 0
for site, result in stats.items():
    print(f" - {site}: Matched {result['matched']}, Unmatched {result['unmatched']}")
    total_matched += result["matched"]
    total_unmatched += result["unmatched"]

print(f"\n✅ Total Matched: {total_matched}, ⚠️ Total Unmatched: {total_unmatched}")
print("🎉 Work done!!")
