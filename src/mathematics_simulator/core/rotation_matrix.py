# -*- coding: utf-8 -*-
"""
方向余弦行列（Direction Cosine Matrix）関連の関数

3D空間における回転を表現する方向余弦行列の生成と操作を提供します。
"""

from typing import Union
import numpy as np
import math


def rot_x(theta: Union[float, np.ndarray]) -> np.ndarray:
    """
    X軸周りの回転行列を生成
    
    Args:
        theta: 回転角度（ラジアン）
        
    Returns:
        3x3回転行列
    """
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    return np.array([
        [1, 0, 0],
        [0, cos_theta, -sin_theta],
        [0, sin_theta, cos_theta]
    ])


def rot_y(theta: Union[float, np.ndarray]) -> np.ndarray:
    """
    Y軸周りの回転行列を生成
    
    Args:
        theta: 回転角度（ラジアン）
        
    Returns:
        3x3回転行列
    """
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    return np.array([
        [cos_theta, 0, sin_theta],
        [0, 1, 0],
        [-sin_theta, 0, cos_theta]
    ])


def rot_z(theta: Union[float, np.ndarray]) -> np.ndarray:
    """
    Z軸周りの回転行列を生成
    
    Args:
        theta: 回転角度（ラジアン）
        
    Returns:
        3x3回転行列
    """
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    return np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ])


def euler_to_rotation_matrix(
    roll: float, 
    pitch: float, 
    yaw: float, 
    order: str = 'ZYX',
    angle_unit: str = 'rad'
) -> np.ndarray:
    """
    オイラー角から回転行列を生成
    
    Args:
        roll: ロール角
        pitch: ピッチ角
        yaw: ヨー角
        order: 回転順序 ('ZYX', 'XYZ', etc.)
        angle_unit: 角度の単位 ('rad' or 'deg')
        
    Returns:
        3x3回転行列
    """
    if angle_unit == 'deg':
        roll = math.radians(roll)
        pitch = math.radians(pitch)
        yaw = math.radians(yaw)
    
    if order == 'ZYX':
        # ヨー→ピッチ→ロールの順
        R = rot_x(roll) @ rot_y(pitch) @ rot_z(yaw)
    elif order == 'XYZ':
        # ロール→ピッチ→ヨーの順
        R = rot_z(yaw) @ rot_y(pitch) @ rot_x(roll)
    else:
        raise ValueError(f"Unsupported rotation order: {order}")
    
    return R


def rotation_matrix_to_euler(
    R: np.ndarray, 
    order: str = 'ZYX',
    angle_unit: str = 'rad'
) -> tuple[float, float, float]:
    """
    回転行列からオイラー角を抽出
    
    Args:
        R: 3x3回転行列
        order: 回転順序 ('ZYX', 'XYZ', etc.)
        angle_unit: 角度の単位 ('rad' or 'deg')
        
    Returns:
        (roll, pitch, yaw)のタプル
    """
    if R.shape != (3, 3):
        raise ValueError("Rotation matrix must be 3x3")
    
    if order == 'ZYX':
        # ZYX順序での抽出
        pitch = math.asin(-R[2, 0])
        
        if abs(math.cos(pitch)) > 1e-6:
            roll = math.atan2(R[2, 1], R[2, 2])
            yaw = math.atan2(R[1, 0], R[0, 0])
        else:
            # ジンバルロック
            roll = 0
            yaw = math.atan2(-R[0, 1], R[1, 1])
    else:
        raise ValueError(f"Unsupported rotation order: {order}")
    
    if angle_unit == 'deg':
        roll = math.degrees(roll)
        pitch = math.degrees(pitch)
        yaw = math.degrees(yaw)
    
    return roll, pitch, yaw


def is_rotation_matrix(R: np.ndarray, tolerance: float = 1e-6) -> bool:
    """
    行列が回転行列かどうかを判定
    
    Args:
        R: 判定する行列
        tolerance: 許容誤差
        
    Returns:
        回転行列の場合True
    """
    if R.shape != (3, 3):
        return False
    
    # 直交性の確認: R @ R.T = I
    should_be_identity = R @ R.T
    identity = np.eye(3)
    if not np.allclose(should_be_identity, identity, atol=tolerance):
        return False
    
    # 行列式が1であることを確認
    det = np.linalg.det(R)
    if not np.isclose(det, 1.0, atol=tolerance):
        return False
    
    return True
