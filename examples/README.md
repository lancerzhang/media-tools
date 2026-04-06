# 示例文件夹

此文件夹用于存放测试用的示例媒体文件。

## 使用方法

1. 将一些测试图片和视频放到此目录
2. 运行检测或压缩脚本进行测试

## 建议

- 使用小文件进行测试（几MB以内）
- 测试前备份原始文件
- 验证效果后再处理大批量文件

## 测试命令

```bash
# 检测示例文件
python src/check_media.py --input examples --type all

# 压缩示例文件（注意：会替换原文件！）
python src/compress_media.py --input examples --type all
```
