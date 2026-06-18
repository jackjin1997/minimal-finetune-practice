# 05. 运行日志

日期：2026-06-18

## 已完成

- 创建最小项目结构。
- 准备任务 JSON 抽取场景。
- 写入训练、验证、测试数据。
- 添加数据校验脚本。
- 创建 `.venv`。
- 安装 `mlx-lm`。
- 数据校验通过。
- 初始化本地 git 仓库。
- 创建 GitHub private 仓库并推送 `main` 分支。

数据校验结果：

```text
train.jsonl: 26 samples
valid.jsonl: 4 samples
test.jsonl: 4 samples
OK: 34 samples
```

当前系统 Python：

```text
Python 3.9.6
```

因为 Python 版本较旧，当前安装到的是兼容的 `mlx-lm 0.29.1`。

## MLX 设备检查

在受限执行环境里，MLX 导入时曾因为拿不到 Metal 设备崩溃。

在正常权限下检查成功：

```text
Device(gpu, 0)
```

结论：后续 `make baseline`、`make train-smoke`、`make train` 建议在正常终端里执行。

## 当前阻塞

第一次执行 baseline 时，需要从 Hugging Face 下载 `Qwen/Qwen3-0.6B`。

本次下载失败原因：

```text
HTTPSConnection(host='huggingface.co', port=443): Failed to establish a new connection: [Errno 60] Operation timed out
```

处理方式：

1. 确认网络能访问 Hugging Face。
2. 配置代理或可用镜像后重试 `make baseline`。
3. 如果已经在本地下载了模型，可以把 `MODEL` 指向本地模型目录：

```bash
MODEL=/path/to/local/model make baseline
MODEL=/path/to/local/model make train-smoke
```

后续使用镜像成功下载：

```bash
HF_ENDPOINT=https://hf-mirror.com make baseline
```

## 微调结果

Baseline 曾输出 `<think>` 和解释性内容，没有稳定遵守“只输出 JSON”。

40 step smoke train：

```text
Trainable parameters: 0.484% (2.884M/596.050M)
Iter 40: Val loss 0.515
Iter 40: Train loss 0.456
Test loss 0.504, Test ppl 1.656
```

240 step train 在小数据上过拟合：

```text
Iter 240: Val loss 0.703
Iter 240: Train loss 0.023
Test loss 0.695, Test ppl 2.004
```

补充 6 条边界样本后，使用 `--mask-prompt` 训练 100 step：

```text
Iter 100: Val loss 0.326
Iter 100: Train loss 0.018
Test loss 0.255, Test ppl 1.290
```

最终生成命令加入：

```bash
--chat-template-config '{"enable_thinking": false}'
```

最终示例输出：

```json
{"title":"补充支付失败错误码统计","type":"feature","priority":"high","due":"2026-06-21","owner":"后端","labels":["支付","失败","统计"],"brief":"整理支付失败错误码统计并补充至文档。"}
```

结论：最小微调闭环已经跑通。结果还不是产品级，因为 `brief` 仍有措辞偏差，下一轮应继续补数据而不是继续加训练步数。

## GitHub 仓库

远端仓库：

```text
https://github.com/jackjin1997/minimal-finetune-practice
```

当前远端名：

```text
origin
```
