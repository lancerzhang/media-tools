# 媒体文件检测使用指南

## 概述

媒体文件检测工具可以帮助你快速扫描目录中的图片和视频文件，检测是否存在损坏或无法正常打开的文件。

## 功能特点

- ✅ 支持图片完整性检测（使用 Pillow）
- ✅ 支持视频完整性检测（使用 FFmpeg）
- ✅ 递归扫描所有子目录
- ✅ 详细的检测报告
- ✅ 可导出报告文件
- ✅ 实时显示检测进度

## 安装依赖

```bash
pip install -r requirements.txt
```

确保 FFmpeg 已安装并添加到系统 PATH。

## 基本用法

### 检测所有媒体文件

```bash
python src/check_media.py --input "your_folder" --type all
```

### 仅检测图片

```bash
python src/check_media.py --input "photos" --type image
```

### 仅检测视频

```bash
python src/check_media.py --input "videos" --type video
```

### 生成报告文件

```bash
python src/check_media.py --input "media" --type all --report report.txt
```

## 参数说明

| 参数 | 简写 | 说明 | 可选值 |
|------|------|------|--------|
| `--input` | `-i` | 要检测的文件夹路径 | 必填 |
| `--type` | `-t` | 检测类型 | image / video / all |
| `--report` | `-r` | 报告文件保存路径 | 可选 |

## 支持的文件格式

### 图片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)
- GIF (.gif)

### 视频格式

- MP4 (.mp4)
- MKV (.mkv)
- AVI (.avi)
- MOV (.mov)
- FLV (.flv)
- WMV (.wmv)
- M4V (.m4v)
- WebM (.webm)

## 检测原理

### 图片检测

使用 Python Pillow 库进行两次验证：

1. **第一次验证**：使用 `Image.verify()` 检查文件头和基本结构
2. **第二次验证**：使用 `Image.load()` 尝试加载完整图片数据

只有两次验证都通过，才认为图片文件完整。

```python
from PIL import Image

def check_image(path):
    try:
        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            img.load()
        return True
    except:
        return False
```

### 视频检测

使用 FFmpeg 进行完整性检查：

```bash
ffmpeg -v error -i input.mp4 -f null -
```

FFmpeg 会尝试解码整个视频文件，如果发现任何错误会返回非零退出码。

```python
import subprocess

def check_video(path):
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "null", "-"],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    return result.returncode == 0
```

## 输出示例

### 控制台输出

```
============================================================
开始检测图片文件...
============================================================
找到 150 个图片文件

[1/150] 检测: photos/2023/IMG_001.jpg
  ✓ 正常
[2/150] 检测: photos/2023/IMG_002.png
  ✗ 损坏
  错误详情: cannot identify image file

...

============================================================
开始检测视频文件...
============================================================
找到 50 个视频文件

[1/50] 检测: videos/2023/VID_001.mp4
  ✓ 正常
[2/50] 检测: videos/2023/VID_002.mov
  ✗ 损坏

...

============================================================
检测摘要
============================================================

图片文件:
  总计: 150
  正常: 148
  损坏: 2

  损坏的图片文件:
    - photos/2023/IMG_002.png
    - photos/2024/IMG_099.jpg

视频文件:
  总计: 50
  正常: 49
  损坏: 1

  损坏的视频文件:
    - videos/2023/VID_002.mov

============================================================
```

### 报告文件格式

```
媒体文件完整性检测报告
============================================================

图片文件统计:
  总计: 150
  正常: 148
  损坏: 2

损坏的图片文件:
  - photos/2023/IMG_002.png
  - photos/2024/IMG_099.jpg

视频文件统计:
  总计: 50
  正常: 49
  损坏: 1

损坏的视频文件:
  - videos/2023/VID_002.mov
```

## 使用场景

### 1. 数据迁移后验证

```bash
# 迁移完成后检测所有文件
python src/check_media.py --input "/new/location" --type all --report migration_check.txt
```

### 2. 定期健康检查

```bash
# 每月检查一次媒体库
python src/check_media.py --input "/media/library" --type all --report monthly_check.txt
```

### 3. 压缩前后对比

```bash
# 压缩前检测
python src/check_media.py --input "/original" --type all --report before.txt

# 压缩后检测
python src/check_media.py --input "/compressed" --type all --report after.txt
```

### 4. 恢复数据验证

```bash
# 从备份恢复后验证
python src/check_media.py --input "/restored" --type all --report restore_check.txt
```

## 性能考虑

### 检测速度

- **图片检测**：非常快，通常每秒可检测数十到上百个文件
- **视频检测**：较慢，取决于视频大小和编码，大文件可能需要数秒到数分钟

### 超时设置

- 图片检测：无超时限制（通常很快）
- 视频检测：默认 5 分钟超时，可在代码中修改

```python
# 在 check_media.py 中修改超时时间
result = subprocess.run(
    [...],
    timeout=300  # 修改为需要的秒数
)
```

### 大规模检测建议

1. **分批处理**：对于数万个文件，建议按目录分批检测
2. **夜间运行**：视频检测耗时较长，可以在夜间运行
3. **并行处理**：可以修改代码支持多进程并行检测

## 常见问题

### Q: 检测会修改文件吗？

A: 不会。检测是只读操作，不会对文件进行任何修改。

### Q: 检测需要多长时间？

A: 取决于文件数量和大小：
- 1000 张图片：约 1-2 分钟
- 100 个视频（每个 100MB）：约 10-30 分钟

### Q: 为什么视频检测这么慢？

A: FFmpeg 需要解码整个视频文件来检测完整性，这是一个 CPU 密集型操作。

### Q: 可以跳过某些文件吗？

A: 可以修改代码添加过滤条件：

```python
# 跳过大于 1GB 的文件
if file_path.stat().st_size > 1024 * 1024 * 1024:
    continue
```

### Q: 检测到损坏文件怎么办？

A: 建议：
1. 尝试用专业工具修复
2. 从备份恢复
3. 如果是压缩导致的，使用原始文件重新压缩

### Q: 误报怎么办？

A: 可能原因：
- 文件正在被其他程序使用
- 文件格式特殊或损坏的元数据
- 建议手动验证可疑文件

## 高级用法

### 自定义检测逻辑

可以修改 `MediaChecker` 类添加自定义检测：

```python
def check_image_advanced(self, file_path: Path) -> bool:
    """高级图片检测"""
    try:
        with Image.open(file_path) as img:
            # 检查基本信息
            img.verify()
            
        with Image.open(file_path) as img:
            # 检查尺寸
            if img.size[0] < 10 or img.size[1] < 10:
                return False
            
            # 检查颜色模式
            if img.mode not in ['RGB', 'RGBA', 'L']:
                return False
            
            # 尝试加载数据
            img.load()
            
        return True
    except:
        return False
```

### 并行检测

使用 Python 多进程加速：

```python
from multiprocessing import Pool

def check_files_parallel(files, num_workers=4):
    with Pool(num_workers) as pool:
        results = pool.map(check_image, files)
    return results
```

### 集成到自动化流程

```python
# 作为模块导入
from check_media import MediaChecker

checker = MediaChecker('/path/to/media')
checker.scan_images()
checker.scan_videos()

# 获取结果
broken_images = checker.results['images']['broken']
if broken_images:
    # 发送通知或执行其他操作
    send_alert(f"发现 {len(broken_images)} 个损坏的图片")
```

## 故障排除

### FFmpeg 未找到

```
错误: 未找到 ffmpeg，请确保已安装并添加到 PATH
```

解决方法：
1. 下载 FFmpeg：https://ffmpeg.org/download.html
2. 添加到系统 PATH
3. 验证：`ffmpeg -version`

### Pillow 安装失败

```bash
# Windows
pip install Pillow

# 如果失败，尝试使用预编译版本
pip install --only-binary :all: Pillow

# Linux
sudo apt-get install python3-pil
pip install Pillow
```

### 权限错误

确保对检测目录有读取权限：

```bash
# Linux/Mac
chmod -R +r /path/to/media

# Windows
# 右键 -> 属性 -> 安全 -> 编辑权限
```

## 最佳实践

1. **定期检测**：建议每月或每季度检测一次媒体库
2. **保存报告**：每次检测都保存报告，便于对比
3. **及时处理**：发现损坏文件及时处理，避免数据丢失
4. **结合备份**：检测不能替代备份，定期备份很重要
5. **压缩前检测**：压缩前先检测，避免压缩损坏文件
