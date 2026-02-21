#!/usr/bin/env python3
"""
Twitter/X 自动发帖 - 支持图片
"""

import sys
import os
import json
import requests
from requests_oauthlib import OAuth1

class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.auth = OAuth1(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret
        )
    
    def upload_media(self, image_path):
        """上传图片"""
        with open(image_path, 'rb') as f:
            img_data = f.read()
        
        resp = requests.post(
            'https://upload.twitter.com/1.1/media/upload.json',
            auth=self.auth,
            files={'media': (os.path.basename(image_path), img_data, 'image/png')}
        )
        
        if resp.status_code == 200:
            return resp.json().get('media_id_string')
        else:
            raise Exception(f'Media upload failed: {resp.text}')
    
    def post(self, text, image_path=None):
        """发帖，可选带图片"""
        media_ids = []
        if image_path:
            media_id = self.upload_media(image_path)
            media_ids.append(media_id)
        
        body = {"text": text}
        if media_ids:
            body["media"] = {"media_ids": media_ids}
        
        resp = requests.post(
            'https://api.twitter.com/2/tweets',
            auth=self.auth,
            json=body
        )
        
        return resp.json()
    
    def get_me(self):
        resp = requests.get('https://api.twitter.com/2/users/me', auth=self.auth)
        return resp.json()

if __name__ == '__main__':
    # 凭证
    consumer_key = os.environ.get('TWITTER_CONSUMER_KEY', 'YOUR_CONSUMER_KEY')
    consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET', 'YOUR_CONSUMER_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN', 'YOUR_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_SECRET', 'YOUR_ACCESS_TOKEN_SECRET')
    
    client = Twitter(consumer_key, consumer_secret, access_token, access_token_secret)
    
    args = sys.argv[1:]
    if not args:
        print("Usage:")
        print("  python twitter.py post <text> [image]")
        print("  python twitter.py me")
        sys.exit(1)
    
    cmd = args[0]
    
    if cmd == 'post':
        text = args[1]
        image = args[2] if len(args) > 2 else None
        result = client.post(text, image)
    elif cmd == 'me':
        result = client.get_me()
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result, indent=2))
