#!/usr/bin/python3
from instagram_feed import InstagramGraphApi
import json

# download instagram data
username = 'ufoboficial' #, 'cnpq_oficial', 'fapergs', 'finepinova', 'capes_oficial', 'agenciafapesp', 'fapesb'

insta = InstagramGraphApi()
busines = insta.business_discovery(username=username,
                         pages=1)


with open('top_media.json', 'w') as outfile:
    json.dump(busines, outfile, indent=4)
