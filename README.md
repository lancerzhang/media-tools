# 媒体文件处理工具集 / Media Processing Toolkit

一个功能强大的媒体文件处理工具集，支持批量压缩和完整性检测。

A powerful media file processing toolkit that supports batch compression and integrity verification.

## ✨ 功能特性 / Features

### 📦 媒体压缩 / Media Compression
- **图片压缩**：支持 JPG, PNG, BMP, TIFF, WebP 等格式，转换为高质量 JPEG
- **视频压缩**：支持 MP4, MKV, AVI, MOV 等格式，使用 H.265/HEVC 编码
- **批量处理**：递归扫描目录，自动处理所有媒体文件
- **进度统计**：实时显示处理进度和耗时

### 🔍 完整性检测 / Integrity Check
- **图片检测**：使用 Pillow 库验证图片文件完整性
- **视频检测**：使用 FFmpeg 检测视频文件是否损坏
- **批量扫描**：一键扫描整个目录并生成检测报告
- **详细报告**：输出每个文件的检测状态（正常/损坏）

## 📋 系统要求 / Requirements

### Windows 批处理脚本
- Windows 7/8/10/11
- [FFmpeg](https://ffmpeg.org/download.html) 已安装并添加到 PATH

### Python 脚本
- Python 3.6+
- Pillow 库：`pip install Pillow`
- FFmpeg 已安装并添加到 PATH

## 🚀 快速开始 / Quick Start

### 1. 媒体压缩

#### Windows 批处理方式
```bash
# 将 compress_media.bat 放到要处理的目录
# 双击运行即可
compress_media.bat
```

#### Python 方式
```bash
# 压缩指定目录的所有媒体文件
python src/compress_media.py --input "your_folder"

# 自定义视频质量参数（默认28，值越小质量越高）
python src/compress_media.py --input "your_folder" --crf 26
```

### 2. 完整性检测

```bash
# 检测图片文件
python src/check_media.py --input "your_folder" --type image

# 检测视频文件
python src/check_media.py --input "your_folder" --type video

# 检测所有媒体文件
python src/check_media.py --input "your_folder" --type all

# 生成详细报告
python src/check_media.py --input "your_folder" --type all --report report.txt
```

## 📁 项目结构 / Project Structure

```
media-processing-toolkit/
├── src/                      # 源代码目录
│   ├── compress_media.py     # Python 压缩脚本
│   ├── check_media.py        # 媒体检测脚本
│   └── utils.py              # 工具函数
├── scripts/                  # 批处理脚本
│   └── compress_media.bat    # Windows 批处理压缩脚本
├── docs/                     # 文档目录
│   ├── compression_guide.md  # 压缩使用指南
│   └── check_guide.md        # 检测使用指南
├── examples/                 # 示例文件
├── requirements.txt          # Python 依赖
└── README.md                 # 项目说明
```

## ⚙️ 配置说明 / Configuration

### 视频压缩质量参数
- **CRF 值**：控制视频压缩质量（18-28 推荐）
  - 18-20：高质量（文件较大）
  - 23-25：平衡质量（推荐）
  - 26-28：较小文件（适合 4K/1080P）

### 图片压缩质量
- 默认使用 FFmpeg `-q:v 4` 参数
- 可在脚本中修改以调整质量

## ⚠️ 重要提示 / Important Notes

1. **备份数据**：压缩操作会替换原文件，请务必提前备份！
2. **测试先行**：建议先用小批量文件测试效果
3. **磁盘空间**：确保有足够的临时空间用于处理
4. **处理时间**：大文件和高质量设置会需要较长时间

## 📖 详细文档 / Documentation

- [压缩功能使用指南](docs/compression_guide.md)
- [检测功能使用指南](docs/check_guide.md)

## 📄 许可证 / License

MIT License - 可自由用于个人和商业项目

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式 / Contact

如有问题或建议，欢迎提交 Issue。

---

**注意**：本工具整合了 Windows 批处理媒体压缩和 Python 媒体检测功能，为用户提供完整的媒体文件处理解决方案。
