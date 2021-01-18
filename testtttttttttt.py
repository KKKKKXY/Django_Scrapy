# import mysql.connector
# import datetime

# class DbdConnector(object):
#     def __init__(self):
#         print('init db')
#         self.db = mysql.connector.connect(
#                 host='dbd_db', 
#                 user='root', 
#                 passwd='opencloud1',
#                 #passwd='opencloud1',
#                 database='dbd',
#                 )
        
#     def insert(self, sql, values):
#         try:
#             cur = self.db.cursor()
#             cur.execute(sql, values)
#             self.db.commit()
#             print('insert succeed',end=' :')
#             if len(values)>5:
#                 print(values[1])#if insert success, It print value
#             else:
#                 print(values)
#         except Exception as e:
#             if e.errno == 1062:#the code when the data already in database
#                 print('duplicate')
#             else:
#                 print(e)
#                 print('fail to insert into dbdcompany, rollback now')
#             self.db.rollback()
#         finally:
#             cur.close()


#     def insertTransaction(self, sqls, values):
#         row_count = 0
#         try:
#             cur = self.db.cursor()
#             for index, item in enumerate(sqls):
#                 cur.execute(item, values[index])
#                 row_count += cur.rowcount
#             self.db.commit()
#             for index, item in enumerate(sqls):
#                 print('insert succeed',end=' :')
#                 if len(values[index])>5:
#                     print(values[index][1])#if insert success, It print value
#                 else:
#                     print(values[index])
#         except Exception as e:
#             row_count = 0
#             if e.errno == 1062:#the code when the data already in database
#                 print('duplicate')
#             else:
#                 print(e)
#                 print('fail to insert transaction, rollback now')
#             self.db.rollback()
#         finally:
#             print(row_count, "record(s) affected")
#             cur.close()


#     def updateCompanyTransaction(self, sqls, values, company_id):
#         row_count = 0
#         try:
#             cur = self.db.cursor()
#             for index, item in enumerate(sqls):
#                 if values[index]:
#                     #print(item % values[index])
#                     cur.execute(item, values[index])
#                 else:
#                     cur.execute(item)
#                 row_count += cur.rowcount
#             self.db.commit()
#         except Exception as e:
#             row_count = 0
#             print(e)
#             print(f'fail to update transaction about company{company_id}, rollback now')
#             self.db.rollback()
#         finally:
#             print(row_count, f"record(s) affected in {company_id}")
#             cur.close()


#     def readIds(self, sql):
#         try:
#             cur = self.db.cursor()
#             cur.execute(sql)
#             ids = cur.fetchall()
#         except Exception as e:
#             print(e)
#             print('fail to get new company ids')
#         finally:
#             cur.close()
#         return ids

#     def read(self, sql):
#         try:
#             cur = self.db.cursor(buffered=True)
#             cur.execute(sql)
#             result = cur.fetchone()
#             #print(f'read result is: {result}')
#         except Exception as e:
#             print(e)
#             print('fail to get information')
#         finally:
#             cur.close()
#             #print('read cur closed')
#         return result

#     def clearmdbd(self):
#         try:
#             sql = 'TRUNCATE TABLE mdbd'
#             cur = self.db.cursor()
#             cur.execute(sql)
#             print('finish empty mdbd')
#         except Exception as e:
#             print(e)
#             print('fail to empty mdbd')
#         finally:
#             cur.close()

#     def clearNewQuery(self):
#         try:
#             sql = 'TRUNCATE TABLE dbd_new_query'
#             cur = self.db.cursor()
#             cur.execute(sql)
#             print('finish empty dbd_new_query')
#         except Exception as e:
#             print(e)
#             print('fail to empty dbd_new_query')
#         finally:
#             cur.close()

#     #####################################
#     def read_exclude_new_company(self):
#         try:
#             sql = '''select t1.DBD_COMPANY_ID from dbd_new_query as t1 
#                      left join mdbd as t2 on t1.DBD_COMPANY_ID = t2.regisid 
#                      where t2.id is null;'''
#             cur = self.db.cursor()
#             cur.execute(sql)
#             exclude_company_id = cur.fetchall()
#         except Exception as e:
#             print(e)
#             print('fail to find id that exclude in mdbd')
#         return exclude_company_id

#     def read_include_new_company(self):
#         try:
#             sql = '''select t1.DBD_COMPANY_ID, t2.id from dbd_new_query as t1
#                      inner join mdbd as t2 on t1.DBD_COMPANY_ID = t2.regisid;'''
#             cur = self.db.cursor()
#             cur.execute(sql)
#             include_company_ids = cur.fetchall()
#         except Exception as e:
#             print(e)
#             print('fail to find id that include in mdbd')
#         return include_company_ids

#     #####################################
#     def read_exclude_all_company(self):
#         try:
#             sql = '''select t1.DBD_ID from dbdcompany as t1 
#                      left join mdbd as t2 on t1.DBD_ID = t2.regisid 
#                      where t2.id is null;'''
#             cur = self.db.cursor()
#             cur.execute(sql)
#             exclude_company_id = cur.fetchall()
#         except Exception as e:
#             print(e)
#             print('fail to find id that exclude in mdbd')
#         return exclude_company_id

#     def read_include_all_company(self):
#         try:
#             sql = '''select t1.DBD_ID, t2.id from dbdcompany as t1 
#                      inner join mdbd as t2 on t1.DBD_ID = t2.regisid where t2.id'''
#             cur = self.db.cursor()
#             cur.execute(sql)
#             include_company_ids = cur.fetchall()
#         except Exception as e:
#             print(e)
#             print('fail to find id that include in mdbd')
#         return include_company_ids
#     #####################################



#     def read_company_info_old(self, company_id):
#         try:
#             sql = f'''select 
#             DBD_ID, DBD_TYPE, DBD_REGISTRATION_DATE, DBD_STATUS, DBD_REGISTRATION_MONEY, DBD_STREET, DBD_SUBDISTRICT, DBD_DISTRICT, DBD_PROVINCE, DBD_ZIPCODE, DBD_BUSINESS_TYPE_CODE, DBD_BUSINESS_TYPE, DBD_OBJECTIVE, DBD_NAME_TH
#             from dbdcompany where DBD_ID = '{company_id}';'''
#             cur = self.db.cursor()
#             cur.execute(sql)
#             company_info = cur.fetchone()
#         except Exception as e:
#             print(e)
#             print('fail to find company info')
#         return company_info

#     def read_company_info(self, company_ids):
#         try:
#             id_str = ''
#             for company_id in company_ids:
#                 id_str += '"' + str(company_id[0]) + '",'
#             id_str = id_str.rstrip(',')
#             #print(id_str)

#             sql = f'''select 
#             DBD_ID, DBD_TYPE, DBD_REGISTRATION_DATE, DBD_STATUS, DBD_REGISTRATION_MONEY, DBD_STREET, DBD_SUBDISTRICT, DBD_DISTRICT, DBD_PROVINCE, DBD_ZIPCODE, DBD_BUSINESS_TYPE_CODE, DBD_BUSINESS_TYPE, DBD_OBJECTIVE, DBD_NAME_TH
#             from dbdcompany where DBD_ID in ({id_str});'''
#             #print(sql)
#             cur = self.db.cursor()
#             cur.execute(sql)
#             company_info = cur.fetchall()
#             #print(company_info)
#         except Exception as e:
#             print(e)
#             print('fail to find company info')
#         return company_info

#     def find_biggest_id(self, num):
#         try:
#             sql = f'SELECT * FROM mdbd WHERE id < {num} ORDER BY id DESC LIMIT 1'
#             cur = self.db.cursor()
#             cur.execute(sql)
#             biggest = cur.fetchone()
#         except Exception as e:
#             print(e)
#             print('fail to find biggest id')
#         return biggest


#     def clear_status_before_annually(self, start, end):
#         try:
#             sql = 'update dbd_query set DBD_STATUS = null'
#             cur = self.db.cursor()
#             cur.execute(sql)
#             print('finish set dbd_query.status to null')
#         except Exception as e:
#             print(e)
#             print('fail to set dbd_query status')
#         finally:
#             cur.close()


#     def dbClose(self):
#         self.db.close()
#         print("database closed")


# if __name__ == '__main__':
#     db = DbdConnector()
#     for i in db.read_include_new_company():
#         print(db.read_company_info(i[0]))

        
