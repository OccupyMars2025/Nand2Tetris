import re

def is_integer(s):
    pattern = r'^\d+$'
    return bool(re.match(pattern, s))