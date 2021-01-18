import mysql.connector
import datetime

class DbdConnector(object):
    def __init__(self):
        print('init db')
        self.db = mysql.connector.connect(
                user='root',
                password='opencloud1',
                host='localhost',
                database='Companies',
                )
        
    def insertCompanyInfo(self, sqls, company_id):
        row_count = 0
        try:
            cur = self.db.cursor()
            print(sqls)
            cur.execute(sqls)
            self.db.commit()
        except Exception as e:
            row_count = 0
            print(e)
            print(f'fail to update transaction about company{company_id}, rollback now')
            self.db.rollback()
        finally:
            print(row_count, f"record(s) affected in {company_id}")
            cur.close()