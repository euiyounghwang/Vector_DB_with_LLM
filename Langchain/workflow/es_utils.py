
import re

''' ****** es util *******'''

def transform_trim_string(to_replace):
    """remove unnecessary characters"""
    if isinstance(to_replace, (str)):
        to_replace = to_replace.strip()
        to_replace = re.sub(r'(?<!\.)(\n|\r\n)', ' ', to_replace)
        to_replace = re.sub(r'\t|\\t', ' ', to_replace)
        to_replace = re.sub(r' +', ' ', to_replace)

    return to_replace
    

def json_value_to_transform_trim(raw_json):
    def get_recursive_nested_all(d):
        if isinstance(d, list):
            for i in d:
                get_recursive_nested_all(i)
        elif isinstance(d, dict):
            for k, v in d.items():
                if not isinstance(v, (list, dict)):
                    print("%%%%", k, v)
                    d[k] = transform_trim_string(v)
                else:
                    get_recursive_nested_all(v)
        return d

    return get_recursive_nested_all(raw_json)