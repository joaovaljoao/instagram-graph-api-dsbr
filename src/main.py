#!/usr/bin/python3
from instagram_feed import InstagramGraphApi
import json

# download instagram data
username = 'cnpq_oficial', 'fapergs', 'finepinova', 'capes_oficial', 'agenciafapesp', 'fapesb'

# bd = InstagramGraphApi().business_discovery(i, pages=1)
top_media = InstagramGraphApi().top_media('ufob', pages=1)
filter = InstagramGraphApi().filter_caption('PROCESSO SELETIVO', top_media)

#write json

with open('top_media.json', 'w') as outfile:
    json.dump(filter, outfile, indent=4)
