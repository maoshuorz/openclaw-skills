# 高德地图 MCP Server

基于 mcporter 的高德地图 MCP 服务，提供天气、地理编码、路线规划等功能。

## 功能

- �Weather: 获取城市天气信息
- 📍 Geocode: 地址转坐标
- 🔄 Reverse Geocode: 坐标转地址
- 🚗 Direction: 驾车路线规划
- 🌐 IP Location: IP 定位
- 🗺️ District: 行政区划查询

## 安装

```bash
# 1. 安装 mcporter
npm install -g mcporter

# 2. 添加配置
mcporter config add amap --stdio "node /path/to/amap-mcp/server.js"
```

## 使用

```bash
# 查询天气
mcporter call amap.weather city=上海

# 地址转坐标
mcporter call amap.geocode address=北京市朝阳区

# 驾车路线
mcporter call amap.direction_driving origin=116.481028,39.989643 destination=116.434446,39.90816

# IP 定位
mcporter call amap.ip_location
```

## API Key

需要高德地图 Web API Key，免费申请：https://console.amap.com/

在 `server.js` 中替换：
```javascript
const AMAP_KEY = '你的API Key';
```

## License

MIT
