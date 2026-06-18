# 最小微调模型实践

用一台 Mac 跑通一次最小可理解的 LoRA 微调。

这个项目的目标不是训练一个“厉害模型”，而是把微调学习路径压到最小：选一个明确场景，准备少量数据，跑原模型 baseline，做 LoRA 训练，再对比 adapter 前后的输出。

## 场景

自然语言需求 -> 结构化任务 JSON。

例子：

```text
请把支付失败的错误码统计补上，2026-06-21 前给后端同学一版，优先级高。
```

期望输出：

```json
{
  "title": "补充支付失败错误码统计",
  "type": "feature",
  "priority": "high",
  "due": "2026-06-21",
  "owner": "后端",
  "labels": ["支付", "错误码", "统计"],
  "brief": "补充支付失败错误码统计，并在截止日期前交付给后端同学。"
}
```

这个场景适合入门，因为它训练的是“输出格式、字段约束、表达风格”，结果能直接检查，不需要复杂评测集。

## 技术选择

- 机器：Mac Apple Silicon 就够了。
- 框架：`mlx-lm`。
- 起步模型：`Qwen/Qwen3-0.6B`。
- 微调方式：LoRA，先不做全量微调。
- 数据规模：先用几十条样例跑通流程，再逐步扩充。

## 项目结构

```text
.
├── data/
│   ├── train.jsonl
│   ├── valid.jsonl
│   └── test.jsonl
├── docs/
│   ├── 01-setup-mac.md
│   ├── 02-data-format.md
│   ├── 03-run-finetune.md
│   ├── 04-concepts.md
│   ├── 05-run-log.md
│   └── 06-publish-github.md
├── prompts/
│   └── task_json_prompt.txt
├── scripts/
│   └── check_data.py
├── Makefile
└── requirements.txt
```

## 快速开始

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
make check-data
```

看原模型输出：

```bash
make baseline
```

跑一次极小训练，确认链路通：

```bash
make train-smoke
```

正式多跑一点：

```bash
make train
```

测试和生成：

```bash
make test
make generate
```

## 学习路径

1. 阅读 [Mac 环境准备](docs/01-setup-mac.md)。
2. 阅读 [数据格式](docs/02-data-format.md)，理解 `messages` 样本。
3. 跑 `make baseline`，记录原模型表现。
4. 跑 `make train-smoke`，先确认训练链路。
5. 跑 `make train` 和 `make generate`，对比 adapter 前后输出。
6. 改 10 条自己的样本，重新训练，观察模型是否更贴近你的格式。
7. 按 [发布到 GitHub](docs/06-publish-github.md) 推到远端仓库。

## 当前状态

- 数据集已准备：20 条训练、4 条验证、4 条测试。
- 数据校验已通过：`make check-data`。
- 本机已创建 `.venv` 并安装 `mlx-lm`。
- Hugging Face 模型下载曾超时，排障记录见 [运行日志](docs/05-run-log.md)。

## 一句话理解微调

微调不是给模型装一个数据库，而是用样本把模型的行为往某个方向推。这个项目先练“稳定按 schema 输出 JSON”，这是最容易观察也最适合入门的微调目标。
