import os,sys,inspect,csv
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import variable_data as vd 



def get_emoji(code,table = None):
    if table is None:
        table = vd.EMOJI_TABLE 
    with open(table,'r',encoding="utf8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            if row['EscapedUnicode'] == code:
                return row
        fp.close()
    pass

print(get_emoji(r'\ud83d\ude00'))