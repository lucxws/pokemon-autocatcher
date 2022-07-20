import re

def extract_name_from_title(title):
    title = re.sub(r'(\d+|#|-|)', '', title) 
    return re.sub(r'^\s+', '', title)   

def extract_id(title):
    return re.findall(r'#(\d+)', title)[0]

def get_names(text, title: str):
    
    languages = ['🇰🇷', '🇨🇳', '🇫🇷', '🇩🇪', '🇪🇸', '🇮🇹']
    names = {}
    
    base_name = extract_name_from_title(title)
    jp_name = re.findall(r'🇯🇵 (.*?)\n', text)
    if jp_name:
        if jp_name[0].find('/'):
            jp_name = jp_name.split('/')[1]
    if not jp_name:
        jp_name = base_name

    names['🇺🇸'] = base_name
    names['🇯🇵'] = [jp_name][0]
    
    for lang in languages:
        if lang in text:
            names[lang] = re.findall(r'{} (.*?)\n'.format(lang), text)[0]        
        if not lang in text:
            names[lang] = [base_name][0]
        
    return names
