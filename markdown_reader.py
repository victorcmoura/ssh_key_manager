import requests
import json

def extract_dict(response_text):
    split_content = response_text.splitlines()

    result_dict = {}

    for each in split_content:
        if(each[0] == '#'):
            username = each[2:]
            result_dict[username] = ""
        else:
            result_dict[username] += each

    return result_dict
