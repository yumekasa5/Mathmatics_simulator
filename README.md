# Mathematics Simulator

3D座標系とアライメントシミュレーションのためのPythonツールセット

## 概要

このプロジェクトは、3D座標系の操作、視覚化、およびアライメントシミュレーションのための包括的なツールを提供します。

## 主な機能

- **3D座標系管理**: 原点と姿勢を持つ3D座標系の定義・操作
- **座標変換**: グローバル座標とローカル座標間の変換
- **3Dビジュアライゼーション**: PySide6とmatplotlibを使った3D座標系の視覚化
- **アライメントシミュレーション**: 座標系のアライメント処理
- **オイラー角サポート**: オイラー角からの座標系生成
- **回転行列操作**: 方向余弦行列による座標系変換

## インストール

### 開発環境のセットアップ

1. リポジトリのクローン:
```bash
git clone <repository-url>
cd Mathmatics_simulator
```

2. 仮想環境の作成とアクティベート:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. 依存関係のインストール:
```bash
pip install -e ".[dev]"
```

### 本番環境のインストール

```bash
pip install mathematics-simulator
```

## 使用方法

### パッケージのインストール（必須）

プロジェクトを開発モードでインストールしてください：

```bash
# 仮想環境をアクティベート
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 開発モードでインストール
pip install -e .
```

### 3D座標系ビューアの起動

```bash
# 方法1: モジュールとして実行
python -m mathematics_simulator.apps.coordinate_3d_viewer

# 方法2: 実行スクリプトを使用
python run_coordinate_viewer.py
```

### 基本的な座標系操作の例

```bash
python examples/coordinate_system_basic.py
```

または、Pythonスクリプトとして:

```python
from mathematics_simulator.apps.coordinate_3d_viewer import main
main()
```

### 基本的な座標系操作

```python
from mathematics_simulator.core.coordinate_system import CoordinateSystem
import numpy as np

# デフォルト座標系（ワールド座標系）
world_coords = CoordinateSystem()

# カスタム座標系の作成
custom_coords = CoordinateSystem(
    origin=[1, 2, 3],
    x_axis=[1, 0, 0],
    y_axis=[0, 1, 0],
    z_axis=[0, 0, 1]
)

# オイラー角からの座標系作成
euler_coords = CoordinateSystem.from_euler_angles(
    origin=[0, 0, 0],
    roll=0, pitch=30, yaw=45,
    angle_unit='deg'
)

# 座標変換
global_point = [10, 20, 30]
local_point = custom_coords.transform_point_to_local(global_point)
```

## プロジェクト構造

```
mathematics_simulator/
├── src/mathematics_simulator/    # メインパッケージ
│   ├── core/                     # コア機能
│   │   ├── coordinate_system.py  # 3D座標系クラス
│   │   └── rotation_matrix.py    # 回転行列関連
│   ├── apps/                     # アプリケーション
│   │   ├── coordinate_3d_viewer.py
│   │   └── alignment_sim.py
│   └── utils/                    # ユーティリティ
├── tests/                        # テストコード
├── docs/                         # ドキュメント
├── examples/                     # 使用例
└── scripts/                      # スクリプト
```

## 開発

### コードフォーマット

```bash
black src/ tests/
```

### リンティング

```bash
flake8 src/ tests/
mypy src/
```

### テスト実行

```bash
pytest
pytest --cov=mathematics_simulator  # カバレッジ付き
```

### pre-commitフックの設定

```bash
pre-commit install
```

## ライセンス

MIT License

## 貢献

プルリクエストや Issue の報告を歓迎します。

## 作者

Developer <developer@example.com>
