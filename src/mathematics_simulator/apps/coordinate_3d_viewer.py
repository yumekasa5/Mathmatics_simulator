# -*- coding: utf-8 -*-
"""
3D座標空間ビューア

PySide6とmatplotlibを使用した3D座標系の視覚化アプリケーション
"""

import sys
from typing import Optional
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, 
    QHBoxLayout, QWidget, QPushButton, QLabel,
    QDoubleSpinBox, QGroupBox
)
from PySide6.QtCore import Qt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ..core.coordinate_system import CoordinateSystem


class Matplotlib3DWidget(FigureCanvas):
    """matplotlib 3Dプロット用ウィジェット"""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        3D matplotlib ウィジェットを初期化
        
        Args:
            parent: 親ウィジェット
        """
        self.figure = Figure(figsize=(8, 6))
        super().__init__(self.figure)
        self.setParent(parent)
        
        # 3Dプロットを作成
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.setup_plot()
        
    def setup_plot(self) -> None:
        """3Dプロットの初期設定"""
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y') 
        self.ax.set_zlabel('Z')
        self.ax.set_title('3D Coordinate System Viewer')
        
        # 軸の範囲を設定
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-2, 2])
        
        # グリッドを表示
        self.ax.grid(True)
        
    def plot_coordinate_system(
        self, 
        coord_system: CoordinateSystem, 
        name: str = "CoordSys", 
        color_scheme: str = 'rgb'
    ) -> None:
        """
        座標系を3Dプロットに描画
        
        Args:
            coord_system: 描画する座標系
            name: 座標系の名前
            color_scheme: 色スキーム ('rgb', 'xyz', 'cool')
        """
        origin = coord_system.get_origin()
        x_axis = coord_system.get_x_axis()
        y_axis = coord_system.get_y_axis()
        z_axis = coord_system.get_z_axis()
        
        # 軸の長さ
        axis_length = 1.5
        
        # 色の設定
        colors = {
            'rgb': ['red', 'green', 'blue'],
            'xyz': ['red', 'green', 'blue'],
            'cool': ['cyan', 'magenta', 'yellow']
        }
        axis_colors = colors.get(color_scheme, colors['rgb'])
        
        # X軸（赤）
        self.ax.quiver(
            origin[0], origin[1], origin[2],
            x_axis[0] * axis_length, x_axis[1] * axis_length, x_axis[2] * axis_length,
            color=axis_colors[0], arrow_length_ratio=0.1, linewidth=3, 
            label=f'{name}-X'
        )
        
        # Y軸（緑）
        self.ax.quiver(
            origin[0], origin[1], origin[2],
            y_axis[0] * axis_length, y_axis[1] * axis_length, y_axis[2] * axis_length,
            color=axis_colors[1], arrow_length_ratio=0.1, linewidth=3, 
            label=f'{name}-Y'
        )
        
        # Z軸（青）
        self.ax.quiver(
            origin[0], origin[1], origin[2],
            z_axis[0] * axis_length, z_axis[1] * axis_length, z_axis[2] * axis_length,
            color=axis_colors[2], arrow_length_ratio=0.1, linewidth=3, 
            label=f'{name}-Z'
        )
        
        # 原点をマーク
        self.ax.scatter(
            origin[0], origin[1], origin[2], 
            color='black', s=50, alpha=0.8, label=f'{name} Origin'
        )
        
    def clear_plot(self) -> None:
        """プロットをクリア"""
        self.ax.clear()
        self.setup_plot()
        
    def refresh_plot(self) -> None:
        """プロットを更新"""
        self.draw()


class CoordinateSystemViewer(QMainWindow):
    """3D座標系ビューアのメインウィンドウ"""
    
    def __init__(self) -> None:
        """メインウィンドウを初期化"""
        super().__init__()
        self.setWindowTitle("3D Coordinate System Viewer")
        self.setGeometry(100, 100, 1200, 800)
        
        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # レイアウト
        main_layout = QHBoxLayout(main_widget)
        
        # 3Dプロット部分
        self.plot_widget = Matplotlib3DWidget()
        main_layout.addWidget(self.plot_widget, 2)  # 比率2
        
        # コントロールパネル
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel, 1)  # 比率1
        
        # 初期表示
        self.update_plot()
        
    def create_control_panel(self) -> QWidget:
        """コントロールパネルを作成"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # ワールド座標系グループ
        world_group = QGroupBox("World Coordinate System")
        world_layout = QVBoxLayout(world_group)
        
        show_world_btn = QPushButton("Show World Coordinates")
        show_world_btn.clicked.connect(self.show_world_coordinates)
        world_layout.addWidget(show_world_btn)
        
        layout.addWidget(world_group)
        
        # カスタム座標系グループ
        custom_group = QGroupBox("Custom Coordinate System")
        custom_layout = QVBoxLayout(custom_group)
        
        # 原点設定
        origin_label = QLabel("Origin (X, Y, Z):")
        custom_layout.addWidget(origin_label)
        
        origin_layout = QHBoxLayout()
        self.origin_x = QDoubleSpinBox()
        self.origin_x.setRange(-5.0, 5.0)
        self.origin_x.setSingleStep(0.1)
        self.origin_x.setValue(1.0)
        
        self.origin_y = QDoubleSpinBox()
        self.origin_y.setRange(-5.0, 5.0)
        self.origin_y.setSingleStep(0.1)
        self.origin_y.setValue(0.0)
        
        self.origin_z = QDoubleSpinBox()
        self.origin_z.setRange(-5.0, 5.0)
        self.origin_z.setSingleStep(0.1)
        self.origin_z.setValue(0.0)
        
        origin_layout.addWidget(self.origin_x)
        origin_layout.addWidget(self.origin_y)
        origin_layout.addWidget(self.origin_z)
        custom_layout.addLayout(origin_layout)
        
        # オイラー角設定
        euler_label = QLabel("Euler Angles (Roll, Pitch, Yaw) [deg]:")
        custom_layout.addWidget(euler_label)
        
        euler_layout = QHBoxLayout()
        self.roll = QDoubleSpinBox()
        self.roll.setRange(-180.0, 180.0)
        self.roll.setSingleStep(5.0)
        self.roll.setValue(0.0)
        
        self.pitch = QDoubleSpinBox()
        self.pitch.setRange(-180.0, 180.0)
        self.pitch.setSingleStep(5.0)
        self.pitch.setValue(0.0)
        
        self.yaw = QDoubleSpinBox()
        self.yaw.setRange(-180.0, 180.0)
        self.yaw.setSingleStep(5.0)
        self.yaw.setValue(45.0)
        
        euler_layout.addWidget(self.roll)
        euler_layout.addWidget(self.pitch)
        euler_layout.addWidget(self.yaw)
        custom_layout.addLayout(euler_layout)
        
        # ボタン
        update_btn = QPushButton("Update Custom Coordinates")
        update_btn.clicked.connect(self.update_custom_coordinates)
        custom_layout.addWidget(update_btn)
        
        show_both_btn = QPushButton("Show Both Systems")
        show_both_btn.clicked.connect(self.show_both_systems)
        custom_layout.addWidget(show_both_btn)
        
        layout.addWidget(custom_group)
        
        # その他のコントロール
        other_group = QGroupBox("View Controls")
        other_layout = QVBoxLayout(other_group)
        
        clear_btn = QPushButton("Clear Plot")
        clear_btn.clicked.connect(self.clear_plot)
        other_layout.addWidget(clear_btn)
        
        reset_view_btn = QPushButton("Reset View")
        reset_view_btn.clicked.connect(self.reset_view)
        other_layout.addWidget(reset_view_btn)
        
        layout.addWidget(other_group)
        
        # スペーサー
        layout.addStretch()
        
        return panel
        
    def show_world_coordinates(self) -> None:
        """ワールド座標系を表示"""
        self.plot_widget.clear_plot()
        
        # ワールド座標系（デフォルト）
        world_coords = CoordinateSystem()
        self.plot_widget.plot_coordinate_system(world_coords, "World", 'rgb')
        
        self.plot_widget.refresh_plot()
        
    def update_custom_coordinates(self) -> None:
        """カスタム座標系を更新表示"""
        self.plot_widget.clear_plot()
        
        # カスタム座標系をオイラー角から作成
        origin = [self.origin_x.value(), self.origin_y.value(), self.origin_z.value()]
        roll = self.roll.value()
        pitch = self.pitch.value()
        yaw = self.yaw.value()
        
        custom_coords = CoordinateSystem.from_euler_angles(
            origin, roll, pitch, yaw, 'deg'
        )
        
        self.plot_widget.plot_coordinate_system(custom_coords, "Custom", 'cool')
        
        self.plot_widget.refresh_plot()
        
    def show_both_systems(self) -> None:
        """両方の座標系を表示"""
        self.plot_widget.clear_plot()
        
        # ワールド座標系
        world_coords = CoordinateSystem()
        self.plot_widget.plot_coordinate_system(world_coords, "World", 'rgb')
        
        # カスタム座標系
        origin = [self.origin_x.value(), self.origin_y.value(), self.origin_z.value()]
        roll = self.roll.value()
        pitch = self.pitch.value()
        yaw = self.yaw.value()
        
        custom_coords = CoordinateSystem.from_euler_angles(
            origin, roll, pitch, yaw, 'deg'
        )
        
        self.plot_widget.plot_coordinate_system(custom_coords, "Custom", 'cool')
        
        # 凡例を追加
        self.plot_widget.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        self.plot_widget.refresh_plot()
        
    def clear_plot(self) -> None:
        """プロットをクリア"""
        self.plot_widget.clear_plot()
        self.plot_widget.refresh_plot()
        
    def reset_view(self) -> None:
        """ビューをリセット"""
        self.plot_widget.ax.view_init(elev=20, azim=45)
        self.plot_widget.refresh_plot()
        
    def update_plot(self) -> None:
        """初期プロットの更新"""
        self.show_world_coordinates()


def main() -> None:
    """メイン関数"""
    app = QApplication(sys.argv)
    
    # メインウィンドウを作成
    viewer = CoordinateSystemViewer()
    viewer.show()
    
    # アプリケーション実行
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
