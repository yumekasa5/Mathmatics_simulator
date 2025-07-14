"""
回転行列関数のテスト
"""

import numpy as np
import pytest
import math
from mathematics_simulator.core.rotation_matrix import (
    rot_x, rot_y, rot_z, euler_to_rotation_matrix, 
    rotation_matrix_to_euler, is_rotation_matrix
)


class TestRotationMatrix:
    """回転行列関数のテストスイート"""
    
    def test_rot_x(self):
        """X軸回転のテスト"""
        # 90度回転
        R = rot_x(math.pi/2)
        
        # 期待される結果
        expected = np.array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0]
        ])
        
        np.testing.assert_array_almost_equal(R, expected)
        assert is_rotation_matrix(R)
    
    def test_rot_y(self):
        """Y軸回転のテスト"""
        # 90度回転
        R = rot_y(math.pi/2)
        
        # 期待される結果
        expected = np.array([
            [0, 0, 1],
            [0, 1, 0],
            [-1, 0, 0]
        ])
        
        np.testing.assert_array_almost_equal(R, expected)
        assert is_rotation_matrix(R)
    
    def test_rot_z(self):
        """Z軸回転のテスト"""
        # 90度回転
        R = rot_z(math.pi/2)
        
        # 期待される結果
        expected = np.array([
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
        
        np.testing.assert_array_almost_equal(R, expected)
        assert is_rotation_matrix(R)
    
    def test_euler_to_rotation_matrix_zyx(self):
        """オイラー角から回転行列への変換テスト (ZYX)"""
        roll, pitch, yaw = 0, 0, 90  # Z軸90度回転のみ
        R = euler_to_rotation_matrix(roll, pitch, yaw, 'ZYX', 'deg')
        
        expected = rot_z(math.pi/2)
        np.testing.assert_array_almost_equal(R, expected)
    
    def test_euler_to_rotation_matrix_xyz(self):
        """オイラー角から回転行列への変換テスト (XYZ)"""
        roll, pitch, yaw = 90, 0, 0  # X軸90度回転のみ
        R = euler_to_rotation_matrix(roll, pitch, yaw, 'XYZ', 'deg')
        
        expected = rot_x(math.pi/2)
        np.testing.assert_array_almost_equal(R, expected)
    
    def test_rotation_matrix_to_euler_zyx(self):
        """回転行列からオイラー角への変換テスト"""
        # 既知のオイラー角
        original_roll, original_pitch, original_yaw = 30, 45, 60
        
        # 回転行列に変換
        R = euler_to_rotation_matrix(original_roll, original_pitch, original_yaw, 'ZYX', 'deg')
        
        # 逆変換
        roll, pitch, yaw = rotation_matrix_to_euler(R, 'ZYX', 'deg')
        
        # 元の値と比較
        assert np.isclose(roll, original_roll)
        assert np.isclose(pitch, original_pitch)
        assert np.isclose(yaw, original_yaw)
    
    def test_is_rotation_matrix_valid(self):
        """有効な回転行列の判定テスト"""
        # 単位行列
        assert is_rotation_matrix(np.eye(3))
        
        # Z軸90度回転
        R = rot_z(math.pi/2)
        assert is_rotation_matrix(R)
        
        # 複合回転
        R = rot_z(0.5) @ rot_y(0.3) @ rot_x(0.7)
        assert is_rotation_matrix(R)
    
    def test_is_rotation_matrix_invalid(self):
        """無効な行列の判定テスト"""
        # 非正方行列
        assert not is_rotation_matrix(np.array([[1, 0], [0, 1]]))
        
        # 非直交行列
        non_orthogonal = np.array([
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        assert not is_rotation_matrix(non_orthogonal)
        
        # 行列式が-1の行列（反射を含む）
        reflection = np.array([
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        assert not is_rotation_matrix(reflection)
    
    def test_identity_rotation(self):
        """恒等回転のテスト"""
        # 0度回転
        for rot_func in [rot_x, rot_y, rot_z]:
            R = rot_func(0)
            np.testing.assert_array_almost_equal(R, np.eye(3))
    
    def test_rotation_composition(self):
        """回転の合成テスト"""
        # 90度 + 90度 = 180度
        R1 = rot_z(math.pi/2)
        R2 = rot_z(math.pi/2)
        R_composed = R2 @ R1
        
        R_direct = rot_z(math.pi)
        np.testing.assert_array_almost_equal(R_composed, R_direct)
    
    def test_unsupported_order_error(self):
        """サポートされていない回転順序のエラーテスト"""
        with pytest.raises(ValueError, match="Unsupported rotation order"):
            euler_to_rotation_matrix(0, 0, 0, 'ABC')
        
        R = np.eye(3)
        with pytest.raises(ValueError, match="Unsupported rotation order"):
            rotation_matrix_to_euler(R, 'ABC')
