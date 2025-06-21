# 模型卡片生成器

这是一个用于生成模型卡片图像的 Python 工具，可以将 logo 和标题组合到背景图像上，创建专业的模型展示卡片。

## 功能特点

- 将 logo 图像裁剪为圆形并添加到背景图像上
- 支持自定义 logo 位置、大小和边框
- 添加模型标题文字，支持字体大小和粗体设置
- 自动根据标题生成输出文件名
- 支持多种图像格式（PNG、JPEG等）

## 安装依赖

```bash
pip install Pillow
```

## 使用方法

### 基本用法

```bash
python draw-model.py --title "我的模型" --background bg.png --logo ./logos/logo.png
```

这将生成一个名为 `我的模型.png` 的输出文件。

### 常用参数示例

```bash
# 基础使用（只需要必需参数）
python draw-model.py  --background bg.png --logo ./logos/claude.png --title "claude-3-5-sonnet-latest"
python draw-model.py  --background bg.png --logo ./logos/claude.png --title "claude-sonnet-4"
python draw-model.py  --background bg.png --logo ./logos/deepseek.png --title "deepseek-r1-250528"
python draw-model.py  --background bg.png --logo ./logos/deepseek.png --title "deepseek-v3-20250324"
python draw-model.py  --background bg.png --logo ./logos/gemini.png --title "gemini-2.5-pro"
python draw-model.py  --background bg.png --logo ./logos/openai.png --title "gpt-3.5-turbo"
python draw-model.py  --background bg.png --logo ./logos/openai.png --title "gpt-4o"
python draw-model.py  --background bg.png --logo ./logos/openai.png --title "gpt-4o-mini"
python draw-model.py  --background bg.png --logo ./logos/qwen.png --title "qwen3-30b-a3b"
python draw-model.py  --background bg.png --logo ./logos/qwen.png --title "qwq-32b-preview"
```

## 支持的模型列表

以下是当前支持的AI模型及其对应的资源文件：

| 模型名称 | 开发商 | 模型卡片 | 详细描述 | Logo |
|---------|--------|----------|----------|------|
| Claude 3.5 Sonnet Latest | Anthropic | ![Claude 3.5 Sonnet Latest](./results/claude-3-5-sonnet-latest.png) | [详细描述](./desc/claude-3-5-sonnet-latest.md) | ![claude](./logos/claude.png) |
| Claude Sonnet 4 | Anthropic | ![Claude Sonnet 4](./results/claude-sonnet-4.png) | [详细描述](./desc/claude-sonnet-4.md) | ![claude](./logos/claude.png) |
| DeepSeek R1 | DeepSeek AI | ![DeepSeek R1](./results/deepseek-r1-250528.png) | [详细描述](./desc/deepseek-r1-250528.md) | ![deepseek](./logos/deepseek.png) |
| DeepSeek V3 | DeepSeek AI | ![DeepSeek V3](./results/deepseek-v3-20250324.png) | [详细描述](./desc/deepseek-v3-20250324.md) | ![deepseek](./logos/deepseek.png) |
| Gemini 2.5 Pro | Google DeepMind | ![Gemini 2.5 Pro](./results/gemini-25-pro.png) | [详细描述](./desc/gemini-25-pro.md) | ![gemini](./logos/gemini.png) |
| GPT-3.5 Turbo | OpenAI | ![GPT-3.5 Turbo](./results/gpt-35-turbo.png) | [详细描述](./desc/gpt-35-turbo.md) | ![openai](./logos/openai.png) |
| GPT-4o | OpenAI | ![GPT-4o](./results/gpt-4o.png) | [详细描述](./desc/gpt-4o.md) | ![openai](./logos/openai.png) |
| GPT-4o Mini | OpenAI | ![GPT-4o Mini](./results/gpt-4o-mini.png) | [详细描述](./desc/gpt-4o-mini.md) | ![openai](./logos/openai.png) |
| Qwen3 30B A3B | 阿里巴巴 | ![Qwen3 30B A3B](./results/qwen3-30b-a3b.png) | [详细描述](./desc/qwen3-30b-a3b.md) | ![qwen](./logos/qwen.png) |
| QwQ 32B Preview | 阿里巴巴 | ![QwQ 32B Preview](./results/qwq-32b-preview.png) | [详细描述](./desc/qwq-32b-preview.md) | ![qwen](./logos/qwen.png) |

### 目录结构
```
draw-model/
├── logos/          # 模型Logo文件
├── results/        # 生成的模型卡片
├── desc/           # 模型详细描述文档
├── bg.png          # 背景图像
└── draw-model.py   # 主程序
```

## 参数说明

### 必需参数
- `--title` / `-t`: 模型卡片的标题文字
- `--background` / `-b`: 背景图像文件路径
- `--logo` / `-l`: logo图像文件路径

### 可选参数（带默认值）
- `--output` / `-o`: 输出文件路径（默认：根据标题自动生成）
- `--circle-center-x`: logo圆形的中心X坐标（默认：80）
- `--circle-radius`: logo圆形的半径（默认：43）
- `--logo-border-width`: logo边框宽度（默认：0）
- `--logo-border-color`: logo边框颜色（默认：white）
- `--logo-bg-color`: logo背景颜色（默认：white）
- `--title-position-x`: 标题文字的X位置（默认：自动计算）
- `--title-font-size`: 标题字体大小（默认：50）
- `--bold`: 使用粗体字体（标志参数，不需要值）
- `--font-path`: 自定义字体文件路径（.ttf格式）

## 使用技巧

1. **图像准备**：
   - 背景图像建议使用较大分辨率，确保有足够空间放置logo和标题
   - logo图像建议使用正方形或接近正方形的图像，效果更佳

2. **参数调整**：
   - 如果logo太小，增加 `--circle-radius` 值
   - 如果标题位置不合适，调整 `--title-position-x` 值
   - 对于长标题，可能需要减小 `--title-font-size` 值

3. **字体设置**：
   - 系统会自动寻找常用字体文件
   - 如需特定字体效果，可使用 `--font-path` 指定字体文件

## 输出文件

- 默认输出文件名基于标题自动生成（特殊字符会被清理，空格替换为下划线）
- 支持PNG和JPEG格式输出
- 图像质量保持原始分辨率

## 错误处理

程序会检查输入文件是否存在，如果背景图像或logo文件不存在，会显示相应的错误信息。

## 查看帮助

```bash
python draw-model.py --help
```

这将显示所有可用参数的详细说明和使用示例。
