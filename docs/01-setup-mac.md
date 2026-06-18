# 01. Mac 环境准备

目标：在 Mac Apple Silicon 上准备一个能跑 `mlx-lm` 的 Python 环境。

## 1. 检查 Python

```bash
python3 --version
```

建议使用 Python 3.11 或 3.12。系统自带 Python 3.9 也可能能安装旧版本 `mlx-lm`，但新模型和新特性更建议用较新的 Python。

## 2. 创建虚拟环境

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
```

## 3. 检查 MLX 是否能看到 GPU

```bash
.venv/bin/python -c "import mlx.core as mx; print(mx.default_device())"
```

期望看到类似：

```text
Device(gpu, 0)
```

如果在某些受限 shell 或沙箱中崩溃，但在正常终端可用，训练和推理请在正常终端执行。

## 4. 检查数据

```bash
make check-data
```

当前项目应输出：

```text
train.jsonl: 20 samples
valid.jsonl: 4 samples
test.jsonl: 4 samples
OK: 28 samples
```

## 5. 模型下载

第一次执行 `make baseline` 会下载模型权重，耗时取决于网络。

```bash
make baseline
```

如果 Hugging Face 连接超时，先确认网络代理或镜像配置，再重试。
