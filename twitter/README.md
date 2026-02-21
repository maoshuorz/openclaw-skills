# Twitter/X 自动发帖

Twitter Developer API 封装，支持发帖、搜索、带图发帖等操作。

## 功能

- 📝 Post: 发布推文
- 🖼️ Post with Image: 发布带图片的推文
- 👤 User: 获取用户信息

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

# 发文字
result = client.post('Hello World!')

# 发图片
result = client.post('Check this out!', '/path/to/image.png')
```

## 命令行

```bash
# 发文字
python twitter.py post "Hello World"

# 发图片
python twitter.py post "Check this!" /path/to/image.png

# 获取用户信息
python twitter.py me
```

## 获取 API Keys

1. 访问 https://developer.twitter.com/en/portal/dashboard
2. 创建 App 并获取 Keys
3. 生成 Access Token (需要 OAuth 1.0a)
4. 确保 App 权限开启 Read and Write

## License

MIT
