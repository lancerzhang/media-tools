#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
媒体文件批量压缩工具
支持图片和视频的批量压缩处理
"""

import os
import sys
import argparse
import subprocess
import time
from pathlib import Path
from typing import List, Tuple


class MediaCompressor:
    """媒体文件压缩器"""
    
    # 支持的文件扩展名
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
    VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.m4v'}
    
    def __init__(self, folder_path: str, crf: int = 28, image_quality: int = 4):
        """
        初始化压缩器
        
        Args:
            folder_path: 要处理的文件夹路径
            crf: 视频压缩质量参数 (18-28, 值越小质量越高)
            image_quality: 图片压缩质量参数 (2-31, 值越小质量越高)
        """
        self.folder_path = Path(folder_path)
        if not self.folder_path.exists():
            raise ValueError(f"路径不存在: {folder_path}")
        
        self.crf = crf
        self.image_quality = image_quality
        
        self.stats = {
            'images_processed': 0,
            'videos_processed': 0,
            'images_failed': 0,
            'videos_failed': 0
        }
    
    def compress_image(self, file_path: Path) -> bool:
        """
        压缩图片文件
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            True 表示成功，False 表示失败
        """
        temp_file = file_path.parent / f"{file_path.stem}_temp.jpg"
        
        try:
            # 使用 ffmpeg 压缩图片
            cmd = [
                'ffmpeg',
                '-hide_banner',
                '-loglevel', 'error',
                '-i', str(file_path),
                '-q:v', str(self.image_quality),
                '-y',
                str(temp_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            
            if result.returncode == 0 and temp_file.exists():
                # 替换原文件
                file_path.unlink()
                temp_file.rename(file_path.with_suffix('.jpg'))
                return True
            else:
                if temp_file.exists():
                    temp_file.unlink()
                return False
                
        except Exception as e:
            print(f"  错误: {str(e)}")
            if temp_file.exists():
                temp_file.unlink()
            return False
    
    def compress_video(self, file_path: Path) -> bool:
        """
        压缩视频文件
        
        Args:
            file_path: 视频文件路径
            
        Returns:
            True 表示成功，False 表示失败
        """
        temp_file = file_path.parent / f"{file_path.stem}_temp.mp4"
        
        try:
            # 使用 ffmpeg 压缩视频 (H.265/HEVC)
            cmd = [
                'ffmpeg',
                '-hide_banner',
                '-loglevel', 'error',
                '-i', str(file_path),
                '-c:v', 'libx265',
                '-crf', str(self.crf),
                '-tag:v', 'hvc1',
                '-c:a', 'copy',
                '-map_metadata', '0',
                '-y',
                str(temp_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=3600)  # 1小时超时
            
            if result.returncode == 0 and temp_file.exists():
                # 替换原文件
                file_path.unlink()
                temp_file.rename(file_path.with_suffix('.mp4'))
                return True
            else:
                if temp_file.exists():
                    temp_file.unlink()
                return False
                
        except subprocess.TimeoutExpired:
            print(f"  超时: 文件处理时间超过1小时")
            if temp_file.exists():
                temp_file.unlink()
            return False
        except Exception as e:
            print(f"  错误: {str(e)}")
            if temp_file.exists():
                temp_file.unlink()
            return False
    
    def process_images(self) -> None:
        """处理所有图片文件"""
        print("\n" + "="*60)
        print("开始处理图片文件...")
        print("="*60)
        
        image_files = []
        for ext in self.IMAGE_EXTENSIONS:
            image_files.extend(self.folder_path.rglob(f"*{ext}"))
        
        # 过滤临时文件
        image_files = [f for f in image_files if '_temp' not in f.stem]
        
        if not image_files:
            print("未找到图片文件")
            return
        
        total = len(image_files)
        print(f"找到 {total} 个图片文件\n")
        
        for idx, file_path in enumerate(image_files, 1):
            relative_path = file_path.relative_to(self.folder_path)
            print(f"[{idx}/{total}] 处理: {relative_path}")
            
            if self.compress_image(file_path):
                print(f"  ✓ 完成")
                self.stats['images_processed'] += 1
            else:
                print(f"  ✗ 失败")
                self.stats['images_failed'] += 1
    
    def process_videos(self) -> None:
        """处理所有视频文件"""
        print("\n" + "="*60)
        print("开始处理视频文件...")
        print("="*60)
        
        video_files = []
        for ext in self.VIDEO_EXTENSIONS:
            video_files.extend(self.folder_path.rglob(f"*{ext}"))
        
        # 过滤临时文件
        video_files = [f for f in video_files if '_temp' not in f.stem]
        
        if not video_files:
            print("未找到视频文件")
            return
        
        total = len(video_files)
        print(f"找到 {total} 个视频文件\n")
        
        for idx, file_path in enumerate(video_files, 1):
            relative_path = file_path.relative_to(self.folder_path)
            print(f"[{idx}/{total}] 处理: {relative_path}")
            
            if self.compress_video(file_path):
                print(f"  ✓ 完成")
                self.stats['videos_processed'] += 1
            else:
                print(f"  ✗ 失败")
                self.stats['videos_failed'] += 1
    
    def print_summary(self, elapsed_time: float) -> None:
        """
        打印处理摘要
        
        Args:
            elapsed_time: 总耗时（秒）
        """
        print("\n" + "="*60)
        print("处理摘要")
        print("="*60)
        
        total_processed = self.stats['images_processed'] + self.stats['videos_processed']
        total_failed = self.stats['images_failed'] + self.stats['videos_failed']
        
        print(f"\n图片:")
        print(f"  成功: {self.stats['images_processed']}")
        print(f"  失败: {self.stats['images_failed']}")
        
        print(f"\n视频:")
        print(f"  成功: {self.stats['videos_processed']}")
        print(f"  失败: {self.stats['videos_failed']}")
        
        print(f"\n总计:")
        print(f"  成功: {total_processed}")
        print(f"  失败: {total_failed}")
        
        # 格式化时间
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        print(f"  耗时: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        print("\n" + "="*60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='媒体文件批量压缩工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  压缩所有媒体:  python compress_media.py --input ./media
  自定义质量:    python compress_media.py --input ./media --crf 26
  仅压缩图片:    python compress_media.py --input ./photos --type image
  仅压缩视频:    python compress_media.py --input ./videos --type video

注意:
  - CRF 值越小质量越高 (推荐: 23-28)
  - 压缩会替换原文件，请提前备份！
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='要处理的文件夹路径'
    )
    
    parser.add_argument(
        '--type', '-t',
        choices=['image', 'video', 'all'],
        default='all',
        help='处理类型: image(图片), video(视频), all(全部)'
    )
    
    parser.add_argument(
        '--crf',
        type=int,
        default=28,
        help='视频压缩质量 (18-28, 默认28)'
    )
    
    parser.add_argument(
        '--image-quality',
        type=int,
        default=4,
        help='图片压缩质量 (2-31, 默认4)'
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if args.crf < 18 or args.crf > 28:
        print("警告: CRF 值建议在 18-28 之间", file=sys.stderr)
    
    try:
        print("\n⚠️  警告: 此操作会替换原文件，请确保已备份重要数据！")
        print("按 Ctrl+C 取消，或按 Enter 继续...")
        input()
        
        compressor = MediaCompressor(args.input, args.crf, args.image_quality)
        
        start_time = time.time()
        
        # 根据类型执行压缩
        if args.type in ['image', 'all']:
            compressor.process_images()
        
        if args.type in ['video', 'all']:
            compressor.process_videos()
        
        elapsed_time = time.time() - start_time
        
        # 打印摘要
        compressor.print_summary(elapsed_time)
        
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
