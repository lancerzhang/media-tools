#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
媒体文件完整性检测工具
支持图片和视频文件的完整性验证
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict
from PIL import Image


class MediaChecker:
    """媒体文件检测器"""
    
    # 支持的文件扩展名
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.gif'}
    VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.m4v', '.webm'}
    
    def __init__(self, folder_path: str):
        """
        初始化检测器
        
        Args:
            folder_path: 要检测的文件夹路径
        """
        self.folder_path = Path(folder_path)
        if not self.folder_path.exists():
            raise ValueError(f"路径不存在: {folder_path}")
        
        self.results = {
            'images': {'ok': [], 'broken': []},
            'videos': {'ok': [], 'broken': []}
        }
    
    def check_image(self, file_path: Path) -> bool:
        """
        检测图片文件完整性
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            True 表示文件正常，False 表示文件损坏
        """
        try:
            with Image.open(file_path) as img:
                img.verify()
            # 二次验证：尝试加载图片数据
            with Image.open(file_path) as img:
                img.load()
            return True
        except Exception as e:
            print(f"  错误详情: {str(e)}")
            return False
    
    def check_video(self, file_path: Path) -> bool:
        """
        检测视频文件完整性
        
        Args:
            file_path: 视频文件路径
            
        Returns:
            True 表示文件正常，False 表示文件损坏
        """
        try:
            result = subprocess.run(
                ["ffmpeg", "-v", "error", "-i", str(file_path), "-f", "null", "-"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                timeout=300  # 5分钟超时
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"  检测超时（可能文件过大）")
            return False
        except FileNotFoundError:
            print(f"  错误: 未找到 ffmpeg，请确保已安装并添加到 PATH")
            return False
        except Exception as e:
            print(f"  错误详情: {str(e)}")
            return False
    
    def scan_images(self) -> None:
        """扫描并检测所有图片文件"""
        print("\n" + "="*60)
        print("开始检测图片文件...")
        print("="*60)
        
        image_files = []
        for ext in self.IMAGE_EXTENSIONS:
            image_files.extend(self.folder_path.rglob(f"*{ext}"))
        
        if not image_files:
            print("未找到图片文件")
            return
        
        total = len(image_files)
        print(f"找到 {total} 个图片文件\n")
        
        for idx, file_path in enumerate(image_files, 1):
            relative_path = file_path.relative_to(self.folder_path)
            print(f"[{idx}/{total}] 检测: {relative_path}")
            
            if self.check_image(file_path):
                print(f"  ✓ 正常")
                self.results['images']['ok'].append(str(relative_path))
            else:
                print(f"  ✗ 损坏")
                self.results['images']['broken'].append(str(relative_path))
    
    def scan_videos(self) -> None:
        """扫描并检测所有视频文件"""
        print("\n" + "="*60)
        print("开始检测视频文件...")
        print("="*60)
        
        video_files = []
        for ext in self.VIDEO_EXTENSIONS:
            video_files.extend(self.folder_path.rglob(f"*{ext}"))
        
        if not video_files:
            print("未找到视频文件")
            return
        
        total = len(video_files)
        print(f"找到 {total} 个视频文件\n")
        
        for idx, file_path in enumerate(video_files, 1):
            relative_path = file_path.relative_to(self.folder_path)
            print(f"[{idx}/{total}] 检测: {relative_path}")
            
            if self.check_video(file_path):
                print(f"  ✓ 正常")
                self.results['videos']['ok'].append(str(relative_path))
            else:
                print(f"  ✗ 损坏")
                self.results['videos']['broken'].append(str(relative_path))
    
    def print_summary(self) -> None:
        """打印检测摘要"""
        print("\n" + "="*60)
        print("检测摘要")
        print("="*60)
        
        # 图片统计
        img_ok = len(self.results['images']['ok'])
        img_broken = len(self.results['images']['broken'])
        img_total = img_ok + img_broken
        
        print(f"\n图片文件:")
        print(f"  总计: {img_total}")
        print(f"  正常: {img_ok}")
        print(f"  损坏: {img_broken}")
        
        if img_broken > 0:
            print(f"\n  损坏的图片文件:")
            for file in self.results['images']['broken']:
                print(f"    - {file}")
        
        # 视频统计
        vid_ok = len(self.results['videos']['ok'])
        vid_broken = len(self.results['videos']['broken'])
        vid_total = vid_ok + vid_broken
        
        print(f"\n视频文件:")
        print(f"  总计: {vid_total}")
        print(f"  正常: {vid_ok}")
        print(f"  损坏: {vid_broken}")
        
        if vid_broken > 0:
            print(f"\n  损坏的视频文件:")
            for file in self.results['videos']['broken']:
                print(f"    - {file}")
        
        print("\n" + "="*60)
    
    def save_report(self, report_path: str) -> None:
        """
        保存检测报告到文件
        
        Args:
            report_path: 报告文件路径
        """
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("媒体文件完整性检测报告\n")
            f.write("="*60 + "\n\n")
            
            # 图片报告
            img_ok = len(self.results['images']['ok'])
            img_broken = len(self.results['images']['broken'])
            img_total = img_ok + img_broken
            
            f.write(f"图片文件统计:\n")
            f.write(f"  总计: {img_total}\n")
            f.write(f"  正常: {img_ok}\n")
            f.write(f"  损坏: {img_broken}\n\n")
            
            if img_broken > 0:
                f.write("损坏的图片文件:\n")
                for file in self.results['images']['broken']:
                    f.write(f"  - {file}\n")
                f.write("\n")
            
            # 视频报告
            vid_ok = len(self.results['videos']['ok'])
            vid_broken = len(self.results['videos']['broken'])
            vid_total = vid_ok + vid_broken
            
            f.write(f"视频文件统计:\n")
            f.write(f"  总计: {vid_total}\n")
            f.write(f"  正常: {vid_ok}\n")
            f.write(f"  损坏: {vid_broken}\n\n")
            
            if vid_broken > 0:
                f.write("损坏的视频文件:\n")
                for file in self.results['videos']['broken']:
                    f.write(f"  - {file}\n")
        
        print(f"\n报告已保存到: {report_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='媒体文件完整性检测工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  检测图片:   python check_media.py --input ./photos --type image
  检测视频:   python check_media.py --input ./videos --type video
  检测全部:   python check_media.py --input ./media --type all
  生成报告:   python check_media.py --input ./media --type all --report report.txt
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='要检测的文件夹路径'
    )
    
    parser.add_argument(
        '--type', '-t',
        choices=['image', 'video', 'all'],
        default='all',
        help='检测类型: image(图片), video(视频), all(全部)'
    )
    
    parser.add_argument(
        '--report', '-r',
        help='保存检测报告的文件路径（可选）'
    )
    
    args = parser.parse_args()
    
    try:
        checker = MediaChecker(args.input)
        
        # 根据类型执行检测
        if args.type in ['image', 'all']:
            checker.scan_images()
        
        if args.type in ['video', 'all']:
            checker.scan_videos()
        
        # 打印摘要
        checker.print_summary()
        
        # 保存报告
        if args.report:
            checker.save_report(args.report)
        
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
