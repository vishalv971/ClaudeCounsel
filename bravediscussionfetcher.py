import requests
import os
from dotenv import load_dotenv

brave_endpoint = "https://api.search.brave.com/res/v1/web/search"

load_dotenv()
brave_api_key = os.getenv('BRAVE_API_KEY')

def fetchDiscussionPosts(prompt):
    PARAMS = {'q':prompt, 'result_filter':'discussions'}
    headers = {'X-Subscription-Token':brave_api_key}
    r = requests.get(url = brave_endpoint, params = PARAMS, headers=headers)
    data = r.json()
    discussionResponse = []
    if 'discussions' in data:
        if len(data['discussions']) > 0:
            
            for result in data['discussions']['results']:
                individualResult = {}
                individualResult['url'] = result['url']
                individualResult['title'] = result['title']
                individualResult['favicon'] = result['meta_url']['favicon']
                discussionResponse.append(individualResult)
            return discussionResponse
