import re
import os

def find_paths(directory:str,type_:str, prefix="", suffix="",pattern=None):

    assert(type_=="dir" or type_=="file")
    if pattern==None:
        pattern = re.compile(r'^' + prefix + r'.*' + suffix + r'$')
    
    matched_list = []

    for root, dirs, files in os.walk(directory):
        if type_=="file":
            for file in files:
                if pattern.match(file):
                    matched_list.append(os.path.join(root, file))
        elif type_=="dir":
            for dir in dirs:
                if pattern.match(dir):
                    matched_list.append(os.path.join(root, dir))
        else:
            raise RuntimeError("type should be dir or file")
    return matched_list