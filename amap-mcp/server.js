#!/usr/bin/env node

/**
 * 高德地图 MCP Server
 * API Key: YOUR_AMAP_KEY
 */

const http = require('http');
const https = require('https');

const AMAP_KEY = 'YOUR_AMAP_KEY';

function amapRequest(path, params) {
  return new Promise((resolve, reject) => {
    const query = new URLSearchParams({ key: AMAP_KEY, ...params }).toString();
    const url = `https://restapi.amap.com/v3${path}?${query}`;
    
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch(e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

const tools = {
  weather: {
    description: "获取指定城市的天气信息",
    inputSchema: {
      type: "object",
      properties: {
        city: { type: "string", description: "城市名称，如北京、上海" }
      },
      required: ["city"]
    }
  },
  geocode: {
    description: "地理编码 - 将地址转换为坐标",
    inputSchema: {
      type: "object",
      properties: {
        address: { type: "string", description: "地址，如北京市朝阳区" }
      },
      required: ["address"]
    }
  },
  reverse_geocode: {
    description: "逆地理编码 - 将坐标转换为地址",
    inputSchema: {
      type: "object",
      properties: {
        longitude: { type: "string", description: "经度" },
        latitude: { type: "string", description: "纬度" }
      },
      required: ["longitude", "latitude"]
    }
  },
  direction_driving: {
    description: "驾车路线规划",
    inputSchema: {
      type: "object",
      properties: {
        origin: { type: "string", description: "起点经纬度，如116.481028,39.989643" },
        destination: { type: "string", description: "终点经纬度，如116.434446,39.90816" }
      },
      required: ["origin", "destination"]
    }
  },
  ip_location: {
    description: "IP定位 - 根据IP地址获取位置",
    inputSchema: {
      type: "object",
      properties: {
        ip: { type: "string", description: "IP地址，默认本机IP" }
      }
    }
  },
  district: {
    description: "行政区划查询",
    inputSchema: {
      type: "object",
      properties: {
        keywords: { type: "string", description: "关键词" },
        subdistrict: { type: "integer", description: "返回下级行政区层级，0-3" }
      },
      required: ["keywords"]
    }
  }
};

async function handleTool(name, args) {
  switch(name) {
    case 'weather':
      return await amapRequest('/weather/weatherInfo', { city: args.city });
    case 'geocode':
      return await amapRequest('/geocode/geo', { address: args.address, output: 'JSON' });
    case 'reverse_geocode':
      return await amapRequest('/geocode/regeo', { location: `${args.longitude},${args.latitude}` });
    case 'direction_driving':
      return await amapRequest('/direction/driving', { origin: args.origin, destination: args.destination });
    case 'ip_location':
      return await amapRequest('/ip', { ip: args.ip || '' });
    case 'district':
      return await amapRequest('/config/district', { keywords: args.keywords, subdistrict: args.subdistrict || 1 });
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

// MCP Protocol
const stdin = process.stdin;
const stdout = process.stdout;

let buffer = '';

stdin.setEncoding('utf8');
stdin.on('data', (chunk) => {
  buffer += chunk;
  let newline;
  while ((newline = buffer.indexOf('\n')) !== -1) {
    const line = buffer.slice(0, newline);
    buffer = buffer.slice(newline + 1);
    try {
      const msg = JSON.parse(line);
      handleMessage(msg);
    } catch(e) {
      // ignore
    }
  }
});

async function handleMessage(msg) {
  if (msg.method === 'initialize') {
    send({ jsonrpc: '2.0', id: msg.id, result: { protocolVersion: '2024-11-05', capabilities: { tools: {} }, serverInfo: { name: 'amap-mcp', version: '1.0.0' } } });
  } else if (msg.method === 'tools/list') {
    send({ jsonrpc: '2.0', id: msg.id, result: { tools: Object.entries(tools).map(([name, def]) => ({ name, ...def })) } });
  } else if (msg.method === 'tools/call') {
    try {
      const result = await handleTool(msg.params.name, msg.params.arguments || {});
      send({ jsonrpc: '2.0', id: msg.id, result: { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] } });
    } catch(e) {
      send({ jsonrpc: '2.0', id: msg.id, error: { code: -32603, message: e.message } });
    }
  } else if (msg.method === 'initialized') {
    // ok
  }
}

function send(msg) {
  stdout.write(JSON.stringify(msg) + '\n');
}
