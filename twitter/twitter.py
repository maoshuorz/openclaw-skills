#!/usr/bin/env python3
"""
Twitter/X 自动发帖
"""

import sys
import json
import time
import random
import hashlib
import base64
import urllib.parse
import hmac
import requests

class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
    
    def _create_oauth_header(self, url, method, body=None):
        oauth_params = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': base64.urlsafe_b64encode(str(random.random()).encode()).decode()[:32],
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_token': self.access_token,
            'oauth_version': '1.0'
        }
        
        all_params = dict(oauth_params)
        if body:
            all_params.update(body)
        
        params_str = '&'.join([f'{urllib.parse.quote(k, safe="")}={urllib.parse.quote(str(v), safe="")}' 
                              for k, v in sorted(all_params.items())])
        
        signature_base = f'{method}&{urllib.parse.quote(url, safe="")}&{urllib.parse.quote(params_str, safe="")}'
        signing_key = f'{urllib.parse.quote(self.consumer_secret, safe="")}&{urllib.parse.quote(self.access_token_secret, safe="")}'
        
        signature = base64.b64encode(hmac.new(signing_key.encode(), signature_base.encode(), hashlib.sha1).digest()).decode()
        oauth_params['oauth_signature'] = signature
        
        return 'OAuth ' + ', '.join([f'{k}="{urllib.parse.quote(v, safe="")}"' for k, v in oauth_params.items()])
    
    def post(self, text):
        """发布推文"""
        url = "https://api.twitter.com/2/tweets"
        method = "POST"
        body = json.dumps({"text": text})
        
        auth_header = self._create_oauth_header(url, method, {"text": text})
        
        resp = requests.post(url, 
            headers={'Authorization': auth_header, 'Content-Type': 'application/json'},
            data=body)
        
        return resp.json()
    
    def search(self, query, limit=10):
        """搜索推文"""
        # 需要 Bearer Token
        return {"error": "Search requires Bearer Token"}
    
    def get_me(self):
        """获取当前用户信息"""
        url = "https://api.twitter.com/2/users/me"
        method = "GET"
        
        auth_header = self._create_oauth_header(url, method)
        
        resp = requests.get(url, headers={'Authorization': auth_header})
        return resp.json()

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("Usage: python twitter.py <ck> <cs> <at> <as> <command> [args]")
        print("Commands: post <text> | me")
        sys.exit(1)
    
    ck = sys.argv[1]
    cs = sys.argv[2]
    at = sys.argv[3]
    as_ = sys.argv[4]
    cmd = sys.argv[5]
    
    client = Twitter(ck, cs, at, as_)
    
    if cmd == 'post':
        text = ' '.join(sys.argv[6:])
        result = client.post(text)
    elif cmd == 'me':
        result = client.get_me()
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result, indent=2))
