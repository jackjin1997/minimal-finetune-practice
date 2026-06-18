# 06. 发布到 GitHub

本项目的展示名称是：

```text
最小微调模型实践
```

建议远端仓库 slug 使用英文，方便 URL、命令行和包管理：

```text
minimal-finetune-practice
```

## 1. 初始化本地仓库

```bash
git init
git add .
git commit -m "init minimal LoRA finetune practice"
```

## 2. 创建 GitHub 远端

如果使用 GitHub CLI：

```bash
gh repo create minimal-finetune-practice --private --source=. --remote=origin --push
```

如果要公开：

```bash
gh repo create minimal-finetune-practice --public --source=. --remote=origin --push
```

## 3. 手动创建远端后推送

如果你在网页上创建了仓库：

```bash
git remote add origin git@github.com:<your-name>/minimal-finetune-practice.git
git branch -M main
git push -u origin main
```

## 4. 不要提交的内容

`.gitignore` 已经忽略：

```text
.venv/
adapters/
models/
outputs/
runs/
checkpoints/
.env
.env.*
__pycache__/
.DS_Store
*.pyc
```

后续真实训练得到的 adapter 默认放在 `adapters/`，一般不直接提交到 GitHub。需要分享时，可以单独上传到模型仓库或 release。
