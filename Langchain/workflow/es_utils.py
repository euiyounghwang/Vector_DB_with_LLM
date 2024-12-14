
import re
import json

''' ****** es util *******'''

class bcolors:
    HEADER    = '\033[95m'
    MARGENTA  = '\033[35m'
    BLUE      = '\033[34m'
    YELLOW    = '\033[33m'
    GREEN     = '\033[32m'
    RED       = '\033[31m'
    CYAN      = '\033[36m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

    ''' 
    if __name__ == '__main__':
        print('\n')
        print("==========================================================")
        print(bcolors().BOLD + bcolors().YELLOW + " start : %s " % ('lib_create') + bcolors().ENDC)
        print("==========================================================")
    '''


class util:
    ''' utils class with statismethod decorator for the pure function like util (when it's not update to the state of instance)'''
    ''' instance method with __init__(self, argument) vs static method (don't need to 'self' argument)'''
    
    SUSPECT_SUBSTRINGS = ["/", "\\", "\"", "*", ":", "AND", "OR", "NOT", "?", "+", "-", "~", "(", ")", "{", "}", "$", ";", "[", "]", "!", "#", "%", "^"]

    @classmethod
    def print_class_name(cls):
        print(cls.name)


    @staticmethod
    def json_read_config(path):
            ''' read config file with option'''
            with open(path, "r") as read_file:
                data = json.load(read_file)
            return data

    @staticmethod
    def has_suspect_characters(query_string):
        ''' es query string'''
        for suspect in util.SUSPECT_SUBSTRINGS:
            if suspect in query_string:
                return True
        return False


    @staticmethod
    def transform_trim_string(to_replace): 
        """remove unnecessary characters"""
        if isinstance(to_replace, (str)):
            to_replace = to_replace.strip()
            to_replace = re.sub(r'(?<!\.)(\n|\r\n)', ' ', to_replace)
            to_replace = re.sub(r'\t|\\t', ' ', to_replace)
            to_replace = re.sub(r' +', ' ', to_replace)

        return to_replace
        

    @staticmethod
    def json_value_to_transform_trim(raw_json):
        ''' update value in the form of json format'''
        def get_recursive_nested_all(d):
            if isinstance(d, list):
                for i in d:
                    get_recursive_nested_all(i)
            elif isinstance(d, dict):
                for k, v in d.items():
                    if not isinstance(v, (list, dict)):
                        print("%%%%", k, v)
                        d[k] = util.transform_trim_string(v)
                    else:
                        get_recursive_nested_all(v)
            return d

        return get_recursive_nested_all(raw_json)


    @staticmethod
    def sanitize_and_trim_text(text):
            # remove punctuation
            regex = r'[\$\{\}\[\]\\\|\)\(<>\+\./%\"\',\-\&\?\!=;\*#:@`~^_]|[0-9]'
            text = re.sub(regex, '', text)

            # remove newlines
            regex = r'\n'
            text = re.sub(regex, ' ', text)

            # remove duplicate spaces
            regex = r' +'
            text = re.sub(regex, ' ', text)

            return text[:2000]