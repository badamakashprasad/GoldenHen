import re
import json
import os



def unicode_process(m):
    '''process(m) -> Unicode code point

    m is a regular expression match object that has groups below:
     1: high Unicode surrogate 4-digit hex code d800-dbff
     2: low  Unicode surrogate 4-digit hex code dc00-dfff
     3: None
    OR
     1: None
     2: None
     3: Unicode 4-digit hex code 0000-d700,e000-ffff
    '''
    if m.group(3) is None:
        # Construct code point from UTF-16 surrogates
        hi = int(m.group(1),16) & 0x3FF
        lo = int(m.group(2),16) & 0x3FF
        cp = 0x10000 | hi << 10 | lo
    else:
        cp = int(m.group(3),16)
    return chr(cp)


def get_emoji(code,indepth = False):
    code = re.sub(r'\\u(d[89ab][0-9a-f]{2})\\u(d[cdef][0-9a-f]{2})|\\u([0-9a-f]{4})',unicode_process,code) 
    code_blk = re.findall(r'\\U[0-9a-f]{8}',str(code.encode('unicode-escape').decode('utf-8')))
    ret = []
    for c in code_blk:
        with open(os.path.join(os.path.dirname(__file__),'emoji_json.json'),mode='r',encoding='utf-8') as fp:
            data = json.load(fp)
            for i in data:
                #print(i['character'].encode('unicode-escape'))
                if i['character'].encode('unicode-escape') == c.encode('utf-8'):
                    if indepth is False:
                        if i['unicodeName'][0] != 'E':
                            ret.append(
                                {
                                    "Name" : i['unicodeName'],
                                    "group" : i['group'],
                                    "subgroup" : i['subGroup']
                                })
                    else:
                        ret.append(i)
    return ret 





def explain_text(text):
    text = text.decode('unicode-escape')
    links = re.findall("http\\S+",text)
    ref_names = re.findall("@\\w+",text)
    hash_tags = re.findall("#\\w+",text)

    emoji_code = ''
    filtered_text = []

    for i in text.split(' '):
        try:
            i.encode('utf-8')
            if i not in links + hash_tags and i != 'RT':
                for ref in ref_names:
                    if ref+':' != i:
                        filtered_text.append(i)
        except UnicodeEncodeError:
            emoji_code += i

    emoji_code = r'{}'.format(emoji_code.encode('unicode-escape').decode('utf-8'))
    emoji_details = get_emoji(emoji_code)
    filtered_text = ' '.join(filtered_text).strip()
    ret = {
        "link" : links ,
        "reference_names" : ref_names ,
        "hash_tags" : hash_tags ,
        "emoji_details" : emoji_details ,
        "filtered_text" : filtered_text
    }

    return ret

text = b"RT @spanishbarbzz: put a net in the car so my dog wouldn\u2019t distract me while driving \ud83e\udd26\ud83c\udffb\u200d\u2640\ufe0f\ud83d\ude02 https://t.co/DB5B8HeKez"
print(explain_text(text))
