#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
開発環境セットアップスクリプト
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """コマンドを実行し、結果を表示"""
    print(f"実行中: {description}")
    print(f"コマンド: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ 成功")
        if result.stdout:
            print(f"出力: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ エラー: {e}")
        if e.stderr:
            print(f"エラー詳細: {e.stderr}")
        return False


def setup_development_environment():
    """開発環境をセットアップ"""
    print("=== Mathematics Simulator 開発環境セットアップ ===\n")
    
    # プロジェクトルートに移動
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"プロジェクトディレクトリ: {project_root}\n")
    
    # 仮想環境の確認
    if not Path(".venv").exists():
        print("仮想環境が見つかりません。")
        create_venv = input("仮想環境を作成しますか？ (y/n): ")
        if create_venv.lower() == 'y':
            run_command("python -m venv .venv", "仮想環境の作成")
        else:
            print("仮想環境が必要です。終了します。")
            return
    
    # 仮想環境のアクティベート確認
    venv_python = ".venv\\Scripts\\python.exe" if os.name == 'nt' else ".venv/bin/python"
    if not Path(venv_python).exists():
        print("仮想環境のPythonが見つかりません。")
        return
    
    # パッケージのインストール
    commands = [
        (f"{venv_python} -m pip install --upgrade pip", "pipのアップグレード"),
        (f"{venv_python} -m pip install -e .", "パッケージのインストール (開発モード)"),
        (f"{venv_python} -m pip install -e \".[dev]\"", "開発依存関係のインストール"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"エラーが発生しました: {description}")
            return
    
    print("\n=== セットアップ完了 ===")
    print("次のコマンドで仮想環境をアクティベートしてください:")
    if os.name == 'nt':
        print("  .venv\\Scripts\\activate")
    else:
        print("  source .venv/bin/activate")
    
    print("\nアプリケーションの実行:")
    print("  python -m mathematics_simulator.apps.coordinate_3d_viewer")
    
    print("\nテストの実行:")
    print("  pytest")


if __name__ == "__main__":
    setup_development_environment()
