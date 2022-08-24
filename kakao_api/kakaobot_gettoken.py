import requests

rest_api_key = 'bd64ff1830b58542a2c2be786ab2bab1'
redirect_uri = 'https://example.com/oauth'
url_token = 'https://kauth.kakao.com/oauth/token'
authorize_code = 'wNY8q_xF1n6E3NvqhLKoHyXemaAewz66acfjqa8uUpnjN04eKGmDfOP1q9HxEBM_ikfLjwo9dGgAAAGBf0oTyQ'

# 신규 발급
param = {
    'grant_type': 'authorization_code',
    'client_id': rest_api_key,
    'redirect_uri': redirect_uri,
    'code': authorize_code,  # 한번 발급되면 authorize_code는 무효화됩니다.
}

response = requests.post('https://kauth.kakao.com/oauth/token', data=param)
# token 발급 api로 발급된 정보들을 kakao_token.json 파일에 저장합니다.
tokens = response.json()
