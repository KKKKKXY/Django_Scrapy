import re
import datetime
def address_separater(s):
    #this method separater the address which from datawarehouse to small part
    if s:
        s = s.replace('\'', '')
    else:
        result = ['','','','','']
        return result

    province_b    = 'กรุงเทพมหานคร'
    province      = 'จ\\.'

    district_b    = 'เขต'
    district      = 'อ\\.|อำเภอ'

    subdistrict_b = 'แขวง'
    subdistrict   = 'ต\\.|ตำบล'



    if province_b in s:
        #if the address is a bangkok address
        pattern = f'(.*){subdistrict_b}(.*){district_b}(.*){province_b}'
        matchObject = re.match(pattern, s)
        company_province    = province_b

        if matchObject:
            #if match pattern success, the address is correct format
            company_street      = matchObject.group(1).strip() 
            company_subdistrict = matchObject.group(2).strip() 
            company_district    = matchObject.group(3).strip() 
        else:
            #if the format is wrong
            matchObject         = re.search(f'{district_b}(.*){province_b}',s)
            company_district    = matchObject.group(1).strip() if matchObject else ''

            if company_district:
                matchObject         = re.search(f'{subdistrict_b}(.*){district_b}',s)
                company_subdistrict = matchObject.group(1).strip() if matchObject else ''
            else:
                #if the district is lost in address, find subdistrict between subdistrict and province
                matchObject         = re.search(f'{subdistrict_b}(.*){province_b}',s)
                company_subdistrict = matchObject.group(1).strip() if matchObject else ''

            if company_subdistrict:
                matchObject         = re.search(f'(.*){subdistrict_b}',s)
                company_street      = matchObject.group(1).strip() if matchObject else ''
            elif company_district:
                #if subdistrict not exist but district exit, find street
                matchObject         = re.search(f'(.*){district_b}',s)
                company_street      = matchObject.group(1).strip() if matchObject else ''
            else:
                matchObject         = re.search(f'(.*){province_b}',s)
                company_street      = matchObject.group(1).strip() if matchObject else ''

    else:
        #if the address is not bangkok address
        pattern = f'(.*)({subdistrict})(.*)({district})(.*){province}(.*)'
        matchObject = re.match(pattern, s)

        if matchObject:
            #if the format is correct
            company_street      = matchObject.group(1).strip() 
            company_subdistrict = matchObject.group(3).strip() 
            company_district    = matchObject.group(5).strip() 
            company_province    = matchObject.group(6).strip() 
        else:
            #if the format is wrong
            matchObject = re.search(f'({province})(.*)',s)
            company_province = matchObject.group(2).strip() if matchObject else ''# find the province 

            matchObject         = re.search(f'({district})(.*)({province})',s)
            company_district    = matchObject.group(2).strip() if matchObject else ''# find the district

            if company_district:
                matchObject         = re.search(f'({subdistrict})(.*)({district})',s)
                company_subdistrict = matchObject.group(2).strip() if matchObject else ''
            else:
                #if the district is lost in address, find subdistrict between subdistrict and province
                matchObject         = re.search(f'({subdistrict})(.*)({province})',s)
                company_subdistrict = matchObject.group(2).strip() if matchObject else ''


            if company_subdistrict:
                #if subdistrict  is exist
                matchObject         = re.search(f'(.*)({subdistrict})',s)
                company_street      = matchObject.group(1).strip() if matchObject else ''
            elif company_district:
                #if subdistrict not exist but district exit
                matchObject         = re.search(f'(.*)({district})',s)
                company_street      = matchObject.group(1).strip() if matchObject else ''
            else:
                #if subdistrict and district both lost
                matchObject         = re.search(f'(.*)({province})',s)
                company_street      = matchObject.group(1).strip() if matchObject else ''


        
    # if can not find anything, return raw address in company_street
    if not company_street and not company_subdistrict and not company_district and not company_province:        
        company_street = s

    company_address = company_street + ' ' + company_subdistrict

    result = [company_street, company_subdistrict, company_district, company_province, company_address]

    #remove some special sign ex: '
    for i in range(4):
        if result[i]:
            result[i] = result[i].replace('\'', '')

    return result

def address_clear(subdistrict, district, province):
    #this method clear the prefix of the address from excel file
    province_b            = 'กรุงเทพมหานคร'
    province_pattern      = 'จ'

    district_pattern_b    = 'เขต'
    district_pattern      = 'อ|อำเภอ'

    subdistrict_pattern_b = 'แขวง'
    subdistrict_pattern   = 'ต|ตำบล'

    #print(subdistrict)

    if province == province_b:
        if district_pattern_b in district:
            district = district[3:]
        if subdistrict_pattern_b in subdistrict:
            subdistrict = subdistrict[4:]
        #district = district.lstrip(district_pattern_b)
        #subdistrict = subdistrict.lstrip(subdistrict_pattern_b)
    else:
        province = province.lstrip(province_pattern).lstrip('.')
        district = district.lstrip(district_pattern).lstrip('.')
        subdistrict = subdistrict.lstrip(subdistrict_pattern).lstrip('.')

    #print(subdistrict)
    
    return subdistrict, district, province


def business_type_separater(s):
    #this method separate the type code and type detail
    s = s.strip('"')
    bussiness_type_code = ''
    bussiness_type      = ''
    try:
        matchObject = re.match('([0-9]*)(.*)', s)
        bussiness_type_code = matchObject.group(1).strip()
        bussiness_type      = matchObject.group(2).strip()
    except:
        print('error')

    return (bussiness_type_code, bussiness_type)

def date_convert(time):
    if isinstance(time,str):
        temptime = datetime.datetime.strptime(time, '%d/%m/%Y').date()
        temptime = temptime.replace(year = temptime.year-543)
        res = datetime.datetime.strftime(temptime , '%Y-%m-%d')
    elif isinstance(time, datetime.datetime):
        time = time.replace(year = time.year-543)
        res = datetime.datetime.strftime(time, '%Y-%m-%d')
    return res

def directors_convert(directors):
        directors_text      = ''

        count = 0

        for line in directors:
            if 'ลงหุ้นด้วย' in line:
                directors_text  = directors_text + line+'\n'
            else:
                directors_text  = directors_text + str(count+1)+'. '+ line+'\n'
                count += 1
        directors_text      = directors_text.rstrip()

        return directors_text





if __name__ == "__main__":
    strings = ['857 ซอยเพชรเกษม94 แขวงบางแคเหนือ เขตบางแค กรุงเทพมหานคร', '39 หมู่ที่ 5 ต.นิคมพัฒนา อ.นิคมพัฒนา จ.ระยอง', '122/2หมู่ที่12 ตำบลสันกำแพงอำเภอสันกำแพงจ.เชียงใหม่']

    for string in strings:
        address = address_separater(string)
        print(f'raw address:{address}')
        print(f'address with header:{address_decorator(address)}')
