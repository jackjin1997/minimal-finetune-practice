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

数据校验结果：

```text
train.jsonl: 20 samples
valid.jsonl: 4 samples
test.jsonl: 4 samples
OK: 28 samples
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
