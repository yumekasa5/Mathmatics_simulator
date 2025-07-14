# -*- coding: utf-8 -*-
"""
3D座標系を定義するクラス

このモジュールは3D空間における座標系の定義、操作、変換機能を提供します。
"""

from typing import Optional, Union, Tuple
import numpy as np
import math


ArrayLike = Union[list, tuple, np.ndarray]


class CoordinateSystem:
    """
    3D座標系を定義するクラス
    
    原点座標と姿勢（3軸の方向ベクトル）を持つ3D座標系を表現し、
    座標変換、回転、平行移動などの操作を提供します。
    
    Attributes:
        origin (np.ndarray): 座標系の原点座標 [x, y, z]
        x_axis (np.ndarray): X軸の単位方向ベクトル
        y_axis (np.ndarray): Y軸の単位方向ベクトル  
        z_axis (np.ndarray): Z軸の単位方向ベクトル
    """
    
    def __init__(
        self, 
        origin: Optional[ArrayLike] = None,
        x_axis: Optional[ArrayLike] = None,
        y_axis: Optional[ArrayLike] = None,
        z_axis: Optional[ArrayLike] = None
    ) -> None:
        """
        座標系を初期化
        
        Args:
            origin: 原点座標 [x, y, z]. デフォルトは [0, 0, 0]
            x_axis: X軸方向ベクトル. デフォルトは [1, 0, 0]
            y_axis: Y軸方向ベクトル. デフォルトは [0, 1, 0]
            z_axis: Z軸方向ベクトル. デフォルトは [0, 0, 1]
            
        Raises:
            ValueError: ゼロベクトルが渡された場合
        """
        # デフォルト値の設定
        self.origin = np.array(
            origin if origin is not None else [0.0, 0.0, 0.0], 
            dtype=float
        )
        
        # デフォルトの軸ベクトル
        default_x = np.array([1.0, 0.0, 0.0])
        default_y = np.array([0.0, 1.0, 0.0])
        default_z = np.array([0.0, 0.0, 1.0])
        
        # 軸ベクトルの設定と正規化
        self.x_axis = self._normalize_vector(
            np.array(x_axis if x_axis is not None else default_x, dtype=float)
        )
        self.y_axis = self._normalize_vector(
            np.array(y_axis if y_axis is not None else default_y, dtype=float)
        )
        self.z_axis = self._normalize_vector(
            np.array(z_axis if z_axis is not None else default_z, dtype=float)
        )
        
        # 直交性をチェック
        self._validate_orthogonality()
    
    def _normalize_vector(self, vector: np.ndarray) -> np.ndarray:
        """
        ベクトルを正規化
        
        Args:
            vector: 正規化するベクトル
            
        Returns:
            正規化されたベクトル
            
        Raises:
            ValueError: ゼロベクトルの場合
        """
        norm = np.linalg.norm(vector)
        if norm < 1e-10:
            raise ValueError("Zero vector cannot be normalized")
        return vector / norm
    
    def _validate_orthogonality(self, tolerance: float = 1e-6) -> None:
        """
        座標軸の直交性をチェック
        
        Args:
            tolerance: 許容誤差
        """
        dot_xy = np.dot(self.x_axis, self.y_axis)
        dot_yz = np.dot(self.y_axis, self.z_axis)
        dot_zx = np.dot(self.z_axis, self.x_axis)
        
        if abs(dot_xy) > tolerance or abs(dot_yz) > tolerance or abs(dot_zx) > tolerance:
            print(
                f"Warning: Coordinate axes are not orthogonal "
                f"(dot products: {dot_xy:.6f}, {dot_yz:.6f}, {dot_zx:.6f})"
            )
    
    @classmethod
    def from_rotation_matrix(
        cls, 
        origin: ArrayLike, 
        rotation_matrix: np.ndarray
    ) -> 'CoordinateSystem':
        """
        回転行列から座標系を作成
        
        Args:
            origin: 原点座標
            rotation_matrix: 3x3回転行列
            
        Returns:
            新しい座標系インスタンス
            
        Raises:
            ValueError: 回転行列のサイズが不正な場合
        """
        if rotation_matrix.shape != (3, 3):
            raise ValueError("Rotation matrix must be 3x3")
            
        x_axis = rotation_matrix[:, 0]
        y_axis = rotation_matrix[:, 1]
        z_axis = rotation_matrix[:, 2]
        
        return cls(origin, x_axis, y_axis, z_axis)
    
    @classmethod
    def from_euler_angles(
        cls, 
        origin: ArrayLike, 
        roll: float, 
        pitch: float, 
        yaw: float, 
        angle_unit: str = 'rad'
    ) -> 'CoordinateSystem':
        """
        オイラー角から座標系を作成（ZYXオーダー）
        
        Args:
            origin: 原点座標
            roll: ロール角（X軸回転）
            pitch: ピッチ角（Y軸回転）
            yaw: ヨー角（Z軸回転）
            angle_unit: 角度の単位 ('rad' or 'deg')
            
        Returns:
            新しい座標系インスタンス
        """
        if angle_unit == 'deg':
            roll = math.radians(roll)
            pitch = math.radians(pitch)
            yaw = math.radians(yaw)
        
        # ZYX オイラー角から回転行列を作成
        cos_r, sin_r = math.cos(roll), math.sin(roll)
        cos_p, sin_p = math.cos(pitch), math.sin(pitch)
        cos_y, sin_y = math.cos(yaw), math.sin(yaw)
        
        rotation_matrix = np.array([
            [cos_y*cos_p, cos_y*sin_p*sin_r - sin_y*cos_r, cos_y*sin_p*cos_r + sin_y*sin_r],
            [sin_y*cos_p, sin_y*sin_p*sin_r + cos_y*cos_r, sin_y*sin_p*cos_r - cos_y*sin_r],
            [-sin_p, cos_p*sin_r, cos_p*cos_r]
        ])
        
        return cls.from_rotation_matrix(origin, rotation_matrix)
    
    def get_origin(self) -> np.ndarray:
        """原点座標を取得"""
        return self.origin.copy()
    
    def get_x_axis(self) -> np.ndarray:
        """X軸方向ベクトルを取得"""
        return self.x_axis.copy()
    
    def get_y_axis(self) -> np.ndarray:
        """Y軸方向ベクトルを取得"""
        return self.y_axis.copy()
    
    def get_z_axis(self) -> np.ndarray:
        """Z軸方向ベクトルを取得"""
        return self.z_axis.copy()
    
    def get_rotation_matrix(self) -> np.ndarray:
        """この座標系の回転行列を取得"""
        return np.column_stack([self.x_axis, self.y_axis, self.z_axis])
    
    def get_transformation_matrix(self) -> np.ndarray:
        """この座標系の同次変換行列を取得"""
        transform = np.eye(4)
        transform[:3, :3] = self.get_rotation_matrix()
        transform[:3, 3] = self.origin
        return transform
    
    def transform_point_to_local(self, global_point: ArrayLike) -> np.ndarray:
        """
        グローバル座標の点をこの座標系のローカル座標に変換
        
        Args:
            global_point: グローバル座標系での点
            
        Returns:
            ローカル座標系での点
        """
        global_point = np.array(global_point)
        relative_point = global_point - self.origin
        
        # この座標系の軸ベクトルに投影
        local_x = np.dot(relative_point, self.x_axis)
        local_y = np.dot(relative_point, self.y_axis)
        local_z = np.dot(relative_point, self.z_axis)
        
        return np.array([local_x, local_y, local_z])
    
    def transform_point_to_global(self, local_point: ArrayLike) -> np.ndarray:
        """
        この座標系のローカル座標の点をグローバル座標に変換
        
        Args:
            local_point: ローカル座標系での点
            
        Returns:
            グローバル座標系での点
        """
        local_point = np.array(local_point)
        
        # ローカル座標をグローバル座標に変換
        global_point = (self.origin + 
                       local_point[0] * self.x_axis + 
                       local_point[1] * self.y_axis + 
                       local_point[2] * self.z_axis)
        
        return global_point
    
    def transform_vector_to_local(self, global_vector: ArrayLike) -> np.ndarray:
        """
        グローバル座標系のベクトルをローカル座標系に変換
        
        Args:
            global_vector: グローバル座標系でのベクトル
            
        Returns:
            ローカル座標系でのベクトル
        """
        global_vector = np.array(global_vector)
        
        local_x = np.dot(global_vector, self.x_axis)
        local_y = np.dot(global_vector, self.y_axis)
        local_z = np.dot(global_vector, self.z_axis)
        
        return np.array([local_x, local_y, local_z])
    
    def transform_vector_to_global(self, local_vector: ArrayLike) -> np.ndarray:
        """
        ローカル座標系のベクトルをグローバル座標系に変換
        
        Args:
            local_vector: ローカル座標系でのベクトル
            
        Returns:
            グローバル座標系でのベクトル
        """
        local_vector = np.array(local_vector)
        
        global_vector = (local_vector[0] * self.x_axis + 
                        local_vector[1] * self.y_axis + 
                        local_vector[2] * self.z_axis)
        
        return global_vector
    
    def set_origin(self, new_origin: ArrayLike) -> None:
        """原点を設定"""
        self.origin = np.array(new_origin, dtype=float)
    
    def translate(self, translation: ArrayLike) -> None:
        """座標系を平行移動"""
        self.origin += np.array(translation)
    
    def rotate(self, rotation_matrix: np.ndarray) -> None:
        """
        座標系を回転
        
        Args:
            rotation_matrix: 3x3回転行列
            
        Raises:
            ValueError: 回転行列のサイズが不正な場合
        """
        if rotation_matrix.shape != (3, 3):
            raise ValueError("Rotation matrix must be 3x3")
            
        self.x_axis = rotation_matrix @ self.x_axis
        self.y_axis = rotation_matrix @ self.y_axis
        self.z_axis = rotation_matrix @ self.z_axis
        
        # 正規化（数値誤差対策）
        self.x_axis = self._normalize_vector(self.x_axis)
        self.y_axis = self._normalize_vector(self.y_axis)
        self.z_axis = self._normalize_vector(self.z_axis)
    
    def __str__(self) -> str:
        """文字列表現"""
        return (f"CoordinateSystem(\n"
                f"  Origin: {self.origin}\n"
                f"  X-axis: {self.x_axis}\n"
                f"  Y-axis: {self.y_axis}\n"
                f"  Z-axis: {self.z_axis}\n"
                f")")
    
    def __repr__(self) -> str:
        return self.__str__()
