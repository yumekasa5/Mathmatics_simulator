#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
座標系の基本的な使用例
"""

import sys
import os
from pathlib import Path

# プロジェクトのsrcディレクトリをPythonパスに追加
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from mathematics_simulator.core.coordinate_system import CoordinateSystem
import numpy as np


def basic_coordinate_system_example():
    """基本的な座標系の使用例"""
    print("=== 基本的な座標系の使用例 ===")
    
    # デフォルト座標系（ワールド座標系）
    world_coords = CoordinateSystem()
    print("ワールド座標系:")
    print(world_coords)
    print()
    
    # カスタム座標系の作成
    custom_coords = CoordinateSystem(
        origin=[1, 2, 3],
        x_axis=[1, 0, 0],
        y_axis=[0, 1, 0],
        z_axis=[0, 0, 1]
    )
    print("カスタム座標系:")
    print(custom_coords)
    print()


def euler_angles_example():
    """オイラー角を使った座標系の例"""
    print("=== オイラー角からの座標系作成 ===")
    
    # オイラー角から座標系を作成
    euler_coords = CoordinateSystem.from_euler_angles(
        origin=[0, 0, 0],
        roll=0, pitch=30, yaw=45,
        angle_unit='deg'
    )
    print("オイラー角座標系 (roll=0°, pitch=30°, yaw=45°):")
    print(euler_coords)
    print()


def coordinate_transformation_example():
    """座標変換の例"""
    print("=== 座標変換の例 ===")
    
    # Y軸方向に1移動、Z軸周り45度回転した座標系
    coords = CoordinateSystem.from_euler_angles([0, 1, 0], 0, 0, 45, 'deg')
    
    # グローバル点の定義
    global_point = [2, 1, 0]
    print(f"グローバル点: {global_point}")
    
    # ローカル座標に変換
    local_point = coords.transform_point_to_local(global_point)
    print(f"ローカル座標: {local_point}")
    
    # グローバル座標に逆変換
    recovered_global = coords.transform_point_to_global(local_point)
    print(f"逆変換結果: {recovered_global}")
    print()


def rotation_matrix_example():
    """回転行列の例"""
    print("=== 回転行列の例 ===")
    
    coords = CoordinateSystem.from_euler_angles([0, 0, 0], 30, 45, 60, 'deg')
    
    # 回転行列を取得
    rotation_matrix = coords.get_rotation_matrix()
    print("回転行列:")
    print(rotation_matrix)
    print()
    
    # 同次変換行列を取得
    transform_matrix = coords.get_transformation_matrix()
    print("同次変換行列:")
    print(transform_matrix)
    print()


def multiple_coordinate_systems_example():
    """複数の座標系を使った例"""
    print("=== 複数座標系の例 ===")
    
    # ロボットベース座標系
    robot_base = CoordinateSystem(origin=[1, 0, 0])
    print("ロボットベース座標系:")
    print(robot_base)
    
    # ロボットアーム座標系（ベースから相対的に定義）
    arm_coords = CoordinateSystem.from_euler_angles([0.5, 0, 0.3], 0, 0, 30, 'deg')
    print("\nロボットアーム座標系:")
    print(arm_coords)
    
    # ワールド座標系の点をそれぞれの座標系で表現
    world_point = [2, 1, 0.5]
    
    base_local = robot_base.transform_point_to_local(world_point)
    arm_local = arm_coords.transform_point_to_local(world_point)
    
    print(f"\nワールド点: {world_point}")
    print(f"ベース座標系での表現: {base_local}")
    print(f"アーム座標系での表現: {arm_local}")
    print()


if __name__ == "__main__":
    basic_coordinate_system_example()
    euler_angles_example()
    coordinate_transformation_example()
    rotation_matrix_example()
    multiple_coordinate_systems_example()
