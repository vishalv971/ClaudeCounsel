import requests

brave_endpoint = "https://api.search.brave.com/res/v1/web/search"


def fetchDiscussionPosts(prompt, brave_api_key=''):
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
