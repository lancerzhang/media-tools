#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
提供通用的辅助功能
"""

import os
import subprocess
from pathlib import Path
from typing import Optional


def check_ffmpeg_installed() -> bool:
    """
    检查 FFmpeg 是否已安装
    
    Returns:
        True 表示已安装，False 表示未安装
    """
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_file_size(file_path: Path) -> str:
    """
    获取文件大小的可读格式
    
    Args:
        file_path: 文件路径
        
    Returns:
        格式化的文件大小字符串
    """
    size = file_path.stat().st_size
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    
    return f"{size:.2f} PB"


def format_duration(seconds: float) -> str:
    """
    格式化时间duration
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的时间字符串 (HH:MM:SS)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def ensure_directory(dir_path: Path) -> None:
    """
    确保目录存在，不存在则创建
    
    Args:
        dir_path: 目录路径
    """
    dir_path.mkdir(parents=True, exist_ok=True)


def is_temp_file(file_path: Path) -> bool:
    """
    判断是否为临时文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        True 表示是临时文件
    """
    return '_temp' in file_path.stem or file_path.stem.startswith('.')


def get_media_info(file_path: Path) -> Optional[dict]:
    """
    获取媒体文件信息
    
    Args:
        file_path: 媒体文件路径
        
    Returns:
        包含媒体信息的字典，失败返回 None
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            str(file_path)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=30,
            text=True
        )
        
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
        
        return None
        
    except Exception:
        return None
