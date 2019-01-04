#!/usr/bin/env python
# coding: utf-8

# [non-conforming-features](https://www.w3.org/TR/html/obsolete.html)

import requests
from bs4 import BeautifulSoup
import json
page_url = 'https://www.w3.org/TR/html/obsolete.html'
response = requests.get(page_url)
print(response)
page_contents = response.content

# Manually stripped out the style information from the html.
# Locally copied the items. TODO: Clean up the html so we can fit the soup in the bowl so to speak... :)
# soup = BeautifulSoup(open('obsolete.html', "r").read())

# This turns out to be pretty heavy for some reason. The page is 3.4M
print('soup load start')
soup = BeautifulSoup(page_contents, features="html.parser")
print('soup load end')
# tags notes:
purge = False
obsolete_tag_list = []
obsolete_attrs_list = {}
cur_tags = []
cur_attr = ''
token_on = ' on '
# dl indexes
# 0- Elements in the following list are entirely obsolete, and must not be used by authors:
# 1- The following attributes are obsolete (though the elements are still part of the language), and must not be used by authors:
print('Parsing W3 obsolete page')
for dl_idx, el in enumerate(soup.find_all(['dl'])):
    if dl_idx == 0:
        print(
            dl_idx,
            'Elements in the following list are entirely obsolete, and must not be used by authors:',
            el.name)
        for i, ch in enumerate(el.contents):
            if ch.name:
                purge = (ch.name == 'dd')
                if (purge):
                    obsolete_tag_list.append({
                        'tags':
                        cur_tags,
                        'alternative':
                        ch.text.strip().replace('\n', '')
                    })
                    cur_tags = []
                else:
                    cur_tags.append(ch.text.strip())

    elif dl_idx == 1:
        print(
            dl_idx,
            'The following attributes are obsolete (though the elements are still part of the language), and must not be used by authors:',
            el.name)

        for i, ch in enumerate(el.contents):
            if ch.name:
                #                 The attr should be the same each time. Index into the dict that has the collection of elements.
                if ch.name == 'dt' and ch.text.find(token_on) > 0:
                    cur_attr = ch.text.split(token_on)[0]
                    cur_element = ch.text.split(
                        token_on)[1].split()[0].replace(',', '')

                    if not cur_attr in obsolete_attrs_list.keys():
                        obsolete_attrs_list[cur_attr] = {'tags': []}

                    obsolete_attrs_list[cur_attr]['tags'].append(cur_element)
                    cur_tags.append(cur_element)
                else:
                    purge = (ch.name == 'dd')
                    if (purge):
                        obsolete_attrs_list[
                            cur_attr]['alternative'] = ch.text.strip().replace(
                                '\n', '').replace(',', '')
                        cur_tags = []

    else:
        print(
            '*' * 10,
            'dl > 1 TODO, I think we have what we need.',
            '*' * 10,
        )


print('Writting obsolete_tag_list.json')
with open('obsolete_tag_list.json',
          'w') as obs_json:  # Use file to refer to the file object
    json.dump(obsolete_tag_list, obs_json)

print('Writting obsolete_attrs_list.json')
with open('obsolete_attrs_list.json',
          'w') as obs_json:  # Use file to refer to the file object
    json.dump(obsolete_attrs_list, obs_json)
