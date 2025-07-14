#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
3D座標系ビューアの実行スクリプト
"""

import sys
import os
from pathlib import Path

def main():
    """メイン関数"""
    # プロジェクトのsrcディレクトリをPythonパスに追加
    project_root = Path(__file__).parent
    src_path = project_root / "src"
    
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    try:
        from mathematics_simulator.apps.coordinate_3d_viewer import main as viewer_main
        print("3D Coordinate System Viewer を起動中...")
        viewer_main()
    except ImportError as e:
        print(f"インポートエラー: {e}")
        print("パッケージが開発モードでインストールされていない可能性があります。")
        print("次のコマンドを実行してください:")
        print("  pip install -e .")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
