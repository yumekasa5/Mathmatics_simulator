"""
CoordinateSystemクラスのテスト
"""

import numpy as np
import pytest
import math
from mathematics_simulator.core.coordinate_system import CoordinateSystem


class TestCoordinateSystem:
    """CoordinateSystemクラスのテストスイート"""
    
    def test_default_initialization(self):
        """デフォルト初期化のテスト"""
        coords = CoordinateSystem()
        
        np.testing.assert_array_equal(coords.get_origin(), [0, 0, 0])
        np.testing.assert_array_equal(coords.get_x_axis(), [1, 0, 0])
        np.testing.assert_array_equal(coords.get_y_axis(), [0, 1, 0])
        np.testing.assert_array_equal(coords.get_z_axis(), [0, 0, 1])
    
    def test_custom_initialization(self):
        """カスタム初期化のテスト"""
        origin = [1, 2, 3]
        x_axis = [1, 0, 0]
        y_axis = [0, 1, 0]
        z_axis = [0, 0, 1]
        
        coords = CoordinateSystem(origin, x_axis, y_axis, z_axis)
        
        np.testing.assert_array_equal(coords.get_origin(), origin)
        np.testing.assert_array_equal(coords.get_x_axis(), x_axis)
        np.testing.assert_array_equal(coords.get_y_axis(), y_axis)
        np.testing.assert_array_equal(coords.get_z_axis(), z_axis)
    
    def test_vector_normalization(self):
        """ベクトル正規化のテスト"""
        # 非正規化ベクトルで初期化
        x_axis = [2, 0, 0]  # 長さ2
        y_axis = [0, 3, 0]  # 長さ3
        z_axis = [0, 0, 4]  # 長さ4
        
        coords = CoordinateSystem(x_axis=x_axis, y_axis=y_axis, z_axis=z_axis)
        
        # すべて単位ベクトルになっているはず
        assert np.isclose(np.linalg.norm(coords.get_x_axis()), 1.0)
        assert np.isclose(np.linalg.norm(coords.get_y_axis()), 1.0)
        assert np.isclose(np.linalg.norm(coords.get_z_axis()), 1.0)
    
    def test_zero_vector_error(self):
        """ゼロベクトルエラーのテスト"""
        with pytest.raises(ValueError, match="Zero vector cannot be normalized"):
            CoordinateSystem(x_axis=[0, 0, 0])
    
    def test_from_euler_angles(self):
        """オイラー角からの作成テスト"""
        origin = [1, 2, 3]
        roll, pitch, yaw = 0, 0, 90  # Z軸周り90度回転
        
        coords = CoordinateSystem.from_euler_angles(origin, roll, pitch, yaw, 'deg')
        
        np.testing.assert_array_equal(coords.get_origin(), origin)
        # 90度回転後のX軸は元のY軸方向になるはず
        np.testing.assert_array_almost_equal(coords.get_x_axis(), [0, 1, 0], decimal=10)
    
    def test_from_rotation_matrix(self):
        """回転行列からの作成テスト"""
        origin = [0, 0, 0]
        # 90度Z軸回転の回転行列
        rotation_matrix = np.array([
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
        
        coords = CoordinateSystem.from_rotation_matrix(origin, rotation_matrix)
        
        np.testing.assert_array_almost_equal(coords.get_x_axis(), [0, 1, 0])
        np.testing.assert_array_almost_equal(coords.get_y_axis(), [-1, 0, 0])
        np.testing.assert_array_almost_equal(coords.get_z_axis(), [0, 0, 1])
    
    def test_point_transformation(self):
        """座標変換のテスト"""
        # Y軸方向に1移動、Z軸周り90度回転した座標系
        coords = CoordinateSystem.from_euler_angles([0, 1, 0], 0, 0, 90, 'deg')
        
        # グローバル点 (1, 0, 0) をローカル座標に変換
        global_point = [1, 0, 0]
        local_point = coords.transform_point_to_local(global_point)
        
        # 期待される結果: 座標系から見て (1, -1, 0)
        expected_local = [1, -1, 0]
        np.testing.assert_array_almost_equal(local_point, expected_local)
        
        # 逆変換のテスト
        recovered_global = coords.transform_point_to_global(local_point)
        np.testing.assert_array_almost_equal(recovered_global, global_point)
    
    def test_vector_transformation(self):
        """ベクトル変換のテスト"""
        # Z軸周り90度回転した座標系
        coords = CoordinateSystem.from_euler_angles([0, 0, 0], 0, 0, 90, 'deg')
        
        # グローバルベクトル (1, 0, 0)
        global_vector = [1, 0, 0]
        local_vector = coords.transform_vector_to_local(global_vector)
        
        # 期待される結果: (0, -1, 0)
        expected_local = [0, -1, 0]
        np.testing.assert_array_almost_equal(local_vector, expected_local)
        
        # 逆変換のテスト
        recovered_global = coords.transform_vector_to_global(local_vector)
        np.testing.assert_array_almost_equal(recovered_global, global_vector)
    
    def test_rotation_matrix_property(self):
        """回転行列取得のテスト"""
        coords = CoordinateSystem.from_euler_angles([0, 0, 0], 30, 45, 60, 'deg')
        rotation_matrix = coords.get_rotation_matrix()
        
        # 回転行列の性質をチェック
        assert rotation_matrix.shape == (3, 3)
        
        # 直交行列であることを確認
        identity = np.eye(3)
        np.testing.assert_array_almost_equal(
            rotation_matrix @ rotation_matrix.T, identity
        )
        
        # 行列式が1であることを確認
        assert np.isclose(np.linalg.det(rotation_matrix), 1.0)
    
    def test_transformation_matrix(self):
        """同次変換行列のテスト"""
        origin = [1, 2, 3]
        coords = CoordinateSystem.from_euler_angles(origin, 0, 0, 90, 'deg')
        transform = coords.get_transformation_matrix()
        
        assert transform.shape == (4, 4)
        
        # 最後の行は [0, 0, 0, 1] であるはず
        np.testing.assert_array_equal(transform[3, :], [0, 0, 0, 1])
        
        # 原点が正しく設定されているはず
        np.testing.assert_array_equal(transform[:3, 3], origin)
    
    def test_translation(self):
        """平行移動のテスト"""
        coords = CoordinateSystem()
        original_origin = coords.get_origin().copy()
        
        translation = [1, 2, 3]
        coords.translate(translation)
        
        expected_origin = original_origin + translation
        np.testing.assert_array_equal(coords.get_origin(), expected_origin)
    
    def test_rotation(self):
        """回転のテスト"""
        coords = CoordinateSystem()
        
        # Z軸周り90度回転
        rotation_matrix = np.array([
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])
        
        coords.rotate(rotation_matrix)
        
        # X軸が元のY軸方向になるはず
        np.testing.assert_array_almost_equal(coords.get_x_axis(), [0, 1, 0])
        np.testing.assert_array_almost_equal(coords.get_y_axis(), [-1, 0, 0])
        np.testing.assert_array_almost_equal(coords.get_z_axis(), [0, 0, 1])
    
    def test_string_representation(self):
        """文字列表現のテスト"""
        coords = CoordinateSystem()
        str_repr = str(coords)
        
        assert "CoordinateSystem" in str_repr
        assert "Origin" in str_repr
        assert "X-axis" in str_repr
        assert "Y-axis" in str_repr
        assert "Z-axis" in str_repr
