# 02. 数据格式

本项目使用聊天格式 JSONL。

训练目录固定为：

```text
data/train.jsonl
data/valid.jsonl
data/test.jsonl
```

每一行是一条样本：

```json
{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

## system

告诉模型角色、输出格式和枚举约束。

本项目要求模型只输出一个 JSON 对象，字段固定为：

```text
title, type, priority, due, owner, labels, brief
```

枚举约束：

```text
type: bug, feature, ops, research, docs
priority: low, medium, high, urgent
```

分类规则：

```text
实现或补充产品能力归 feature。
整理说明、FAQ、手册、流程图归 docs。
排障修复归 bug。
监控、告警、备份、证书和部署运行归 ops。
技术选型和方案比较归 research。
```

## user

自然语言需求。

```text
支付回调偶尔重复入账，后端今天先排查根因，紧急。
```

## assistant

目标输出，必须是合法 JSON 字符串。

```json
{
  "title": "排查支付回调重复入账",
  "type": "bug",
  "priority": "urgent",
  "due": null,
  "owner": "后端",
  "labels": ["支付", "回调", "账务"],
  "brief": "排查支付回调导致重复入账的偶发问题并定位根因。"
}
```

## 写数据的原则

- 每条样本只教一个清晰行为。
- 输出字段顺序保持一致。
- 枚举值不要混用同义词，例如不要一会儿写 `high`，一会儿写 `高`。
- 不要把没有说清楚的信息硬编进去；没有 owner 或 due 就用 `null`。
- 训练集、验证集、测试集不要放完全重复的 user 文本。

## 校验

```bash
make check-data
```

校验脚本会检查：

- JSONL 每行是否可解析。
- 是否正好包含 `system/user/assistant` 三段消息。
- assistant 内容是否是合法 JSON。
- 字段是否完整。
- `type` 和 `priority` 是否落在允许枚举里。
- `due` 是否是 `YYYY-MM-DD` 或 `null`。
- 是否有多余字段。
- system prompt 是否和 `prompts/system.txt` 保持一致。
