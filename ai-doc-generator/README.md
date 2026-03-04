# AI 智能文档生成器

基于 AI 的合同与单据自动填充、批量生成工具。

## 功能

| 功能 | 说明 |
|------|------|
| **模板解析** | 从 `.docx` 模板中自动提取 `{{字段名}}` 占位符 |
| **AI 智能填充** | 用户提供模糊描述，AI 自动推断字段值并填充模板 |
| **批量生成** | 基于模板 + 模糊描述，一次生成多份不同数据的文档 |
| **AI 自由生成** | 无需模板，根据描述直接生成完整、美观的合同/单据 |
| **批量自由生成** | 无需模板，批量生成多份不同内容的文档 |

## 安装依赖

```bash
pip install python-docx openai
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | API 密钥（必需） |
| `OPENAI_BASE_URL` | API 地址（可选，兼容 DeepSeek / 通义千问 等） |
| `OPENAI_MODEL` | 模型名称（可选，默认 `gpt-4o`） |

## 使用方式

### 1. 模板解析 — 查看模板中有哪些字段

```bash
python ai_doc_generator.py parse 合同模板.docx
```

输出示例:
```json
{
  "fields": ["甲方", "乙方", "金额", "日期", "合同编号"],
  "field_count": 5
}
```

### 2. 手动填充 — 用 JSON 数据填充模板

```bash
python ai_doc_generator.py fill 合同模板.docx data.json 输出合同.docx
```

`data.json` 格式:
```json
{
  "甲方": "北京某某科技有限公司",
  "乙方": "上海某某贸易有限公司",
  "金额": "100,000.00",
  "日期": "2026年3月4日"
}
```

### 3. AI 智能填充 — 模糊描述自动填充

```bash
python ai_doc_generator.py smart 合同模板.docx "甲方是北京的一家科技公司，乙方是上海的贸易公司，合同金额大概10万" 输出.docx
```

AI 会自动推断所有字段值并填充。

### 4. 批量生成 — 基于模板批量制作

```bash
python ai_doc_generator.py batch 合同模板.docx "为10个不同的客户生成采购合同，金额在5万到20万之间" ./output 10
```

### 5. AI 自由生成 — 无需模板，直接生成

```bash
python ai_doc_generator.py generate "帮我生成一份软件开发外包合同，甲方是XX科技，乙方是YY工作室，项目是电商App开发，总价50万" 合同.docx 合同
```

支持的文档类型: `合同`、`收据`、`报价单`、`协议`、`委托书` 等。

### 6. 批量自由生成

```bash
python ai_doc_generator.py batch-gen "生成不同项目的软件外包合同" ./contracts 5 合同
```

## Python API 调用

```python
from ai_doc_generator import AIDocGenerator

gen = AIDocGenerator(
    api_key="your-api-key",
    base_url="https://api.deepseek.com/v1",  # 可选
    model="deepseek-chat"                     # 可选
)

# 智能填充
result = gen.smart_fill(
    template_path="合同模板.docx",
    user_description="甲方是北京的科技公司，乙方是深圳的硬件厂商，金额约30万",
    output_path="输出合同.docx"
)

# 批量生成
result = gen.batch_fill(
    template_path="合同模板.docx",
    user_description="为5个不同供应商生成采购合同",
    output_dir="./output",
    count=5
)

# AI 自由生成
result = gen.ai_generate(
    user_description="一份租房合同，房东张三，租客李四，月租5000，租期一年",
    output_path="租房合同.docx",
    doc_type="合同"
)
```

## 模板制作说明

在 Word 文档中使用 `{{字段名}}` 作为占位符:

```
甲方: {{甲方名称}}
乙方: {{乙方名称}}
合同金额: {{金额}}元
签订日期: {{签订日期}}
```

也支持单花括号 `{字段名}` 格式。
