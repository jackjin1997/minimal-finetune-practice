# 03. 跑通微调

目标：按最小闭环完成 baseline、训练、测试和生成。

## 1. Baseline

先看原模型在同一条 prompt 上的输出。

```bash
make baseline
```

记录观察点：

- 是否只输出 JSON。
- 字段是否完整。
- `type` 和 `priority` 是否符合枚举。
- `due` 是否是 `YYYY-MM-DD` 或 `null`。
- 是否输出额外解释。

## 2. Smoke Train

先跑很少步数，只确认训练链路可用。

```bash
make train-smoke
```

默认参数：

```text
model: Qwen/Qwen3-0.6B
iters: 40
batch-size: 1
learning-rate: 1e-5
mask-prompt: true
adapter-path: adapters/task-json-qwen3-0.6b
```

## 3. Train

```bash
make train
```

默认 `ITERS=100`。可以覆盖：

```bash
ITERS=160 make train
```

## 4. Test

```bash
make test
```

这一步用 `data/test.jsonl` 看 loss，不要只看一个人工样例。`Makefile` 里的 test 也使用 `--mask-prompt`，和训练口径保持一致。

## 5. Generate

```bash
make generate
```

它会加载同一个 base model 和 LoRA adapter，对 `prompts/system.txt` 和 `prompts/user.txt` 生成结果。

## 6. 对比记录

建议把结果记录成：

```text
baseline:
...

after lora:
...

问题:
- ...

下一轮数据:
- ...
```

如果输出格式不稳，优先补相似的训练样本，而不是先调复杂参数。

## Qwen3 Thinking

Qwen3 默认可能输出 `<think>...</think>`。本项目的 `Makefile` 已在生成命令里加入：

```bash
--chat-template-config '{"enable_thinking": false}'
```

这样更适合结构化 JSON 输出练习。
