# Minimal Fine-Tuning Practice

A small, reproducible LoRA fine-tuning walkthrough that runs on a Mac with Apple Silicon.

The goal is not to build a powerful model. The goal is to make the fine-tuning loop concrete: pick a narrow scenario, prepare a tiny dataset, run a baseline, train a LoRA adapter, test it, and compare generation results.

## Scenario

Natural-language task request -> structured task JSON.

Example input:

```text
Please add statistics for payment failure error codes and give backend engineers a version before 2026-06-21. High priority.
```

Expected output shape:

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

This scenario is useful for learning because the result is easy to inspect: valid JSON, fixed fields, constrained enum values, extracted dates, and stable wording.

## Stack

- Machine: Mac with Apple Silicon.
- Framework: `mlx-lm`.
- Base model: `Qwen/Qwen3-0.6B`.
- Method: LoRA, not full fine-tuning.
- Dataset: 26 train samples, 4 validation samples, 4 test samples.

## Quick Start

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
make check-data
```

Run baseline:

```bash
make baseline
```

Train and test:

```bash
make train
make test
```

Generate with both the test-style prompt and an unseen prompt:

```bash
make generate
make generate-unseen
```

If Hugging Face access is slow or blocked:

```bash
HF_ENDPOINT=https://hf-mirror.com make baseline
HF_ENDPOINT=https://hf-mirror.com make train
HF_ENDPOINT=https://hf-mirror.com make generate-unseen
```

## Current Result

After synchronizing the dataset system prompt with `prompts/system.txt`, training with `--mask-prompt` for 100 iterations produced:

```text
Test loss 0.240, Test ppl 1.272
```

Unseen prompt:

```text
请把发票开具失败的原因统计入口补到财务后台，2026-07-02 前给产品和后端确认，高优先级。
```

Generated output:

```json
{"title":"补充发票开具失败原因统计入口","type":"feature","priority":"high","due":"2026-07-02","owner":"产品和后端","labels":["财务","发票","统计"],"brief":"在财务后台补充发票开具失败原因统计入口。"}
```

## HTML Notes

The visual bilingual version is available in [index.html](index.html). It is a static step-by-step tutorial with no external dependencies, organized as learning goals, principle, run steps, results, and pitfalls.

## License

This project is licensed under the [MIT License](LICENSE). Base models, model weights, and third-party dependencies follow their own licenses.
