# Twitter/X 自动发帖

Twitter Developer API 封装，支持发帖、搜索、转推等操作。

## 功能

- 📝 Post: 发布推文
- 🔍 Search: 搜索推文
- 👤 User: 获取用户信息
- 🔄 Retweet: 转推

## 安装

```bash
pip3 install requests requests-oauthlib
```

## 使用

```python
from twitter import Twitter

client = Twitter(
    consumer_key='你的Consumer Key',
    consumer_secret='你的Consumer Secret',
    access_token='你的Access Token',
    access_token_secret='你的Access Token Secret'
)

# 发帖
result = client.post('Hello from Twitter API!')
print(result)

# 搜索
results = client.search('AI', limit=10)
print(results)
```

## 获取 API Keys

1. 访问 https://developer.twitter.com/en/portal/dashboard
2. 创建 App 并获取 Keys
3. 确保 App 权限开启 Read and Write

## License

MIT
