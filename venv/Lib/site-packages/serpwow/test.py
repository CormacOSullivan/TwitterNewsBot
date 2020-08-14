# -*- coding: utf-8 -*-

from google_search_results import GoogleSearchResults
import json

# create the serpwow object, passing in our API key
serpwow = GoogleSearchResults("E47P2562")

params = {
  'name': '2020-04-17/LP_Contacts_1_test', 
  'enabled': True, 
  'schedule_type': 'manual', 
  'notification_email': 
  'kiruthika.easwari@preqin.com', 
  'notification_as_csv': True, 
  'notification_as_json': True, 
  'api_key': '561B51D7E5FF488FA59B37F59B09D978'
}
# retrieve the search results as JSON
result = serpwow.create_batch(params)

# pretty-print the result
print(json.dumps(result, indent=2, sort_keys=True))