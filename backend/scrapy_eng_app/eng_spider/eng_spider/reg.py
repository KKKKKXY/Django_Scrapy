import re

def business_type_separater(s):
    #this method separate the type code and type detail
    s = s.strip('"')
    bussiness_type_code = ''
    bussiness_type      = ''
    if s == '-':
        bussiness_type_code = '-'
        bussiness_type      = '-'
    else:
        try:
            matchObject = re.match('([0-9]*)(.*)', s)
            bussiness_type_code = matchObject.group(1).strip()
            bussiness_type      = matchObject.group(2).strip()
        except:
            print('Convert business type faild')

    return (bussiness_type_code, bussiness_type)


def directors_convert(directors):
        directors_text      = ''
        count = 0

        for line in directors:
            if 'ลงหุ้นด้วย' in line or 'Stocking with' in line:
                directors_text  = directors_text
            else:
                if '/' in line:
                    line = line[:-1]
                directors_text  = directors_text + str(count+1)+'. '+ line+'\n'
                count += 1
        directors_text      = directors_text.rstrip()

        return directors_text