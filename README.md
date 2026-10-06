# lecture_ws

ROS 2 Jazzy を使ったロボット講習用ワークスペースです。
ロボットモデルと Gazebo シミュレーション、ゲームパッド操作に加え、ROS 2 と STM32 のシリアル通信サンプルを収録しています。

## パッケージ構成

| パッケージ / ディレクトリ | 内容 |
| --- | --- |
| `lecture_description` | ロボットの URDF/Xacro、メッシュ、RViz 表示用設定 |
| `lecture_simulation` | Gazebo Sim のフィールド、ロボットのスポーン、ROS 2 ブリッジ |
| `lecture_teleop` | `sensor_msgs/msg/Joy` を `geometry_msgs/msg/Twist` に変換する操作学習用ノード |
| `lecture_teleop_cpp` | `sensor_msgs/msg/Joy` を `geometry_msgs/msg/Twist` に変換する操作学習用ノード（C++版） |
| `serial_communication` | PC 側から UART を送受信する ROS 2 ノード |
| `lecture_bringup` | UART 送受信ノードを起動する launch ファイル |
| `stm32/uart_send` | STM32 からカウント値を送信する PlatformIO プロジェクト |
| `stm32/uart_recv` | STM32 が受信した文字列をエコーバックする PlatformIO プロジェクト |
| `python_practice` | Python の基礎練習用コード |

## 動作環境

- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic / `ros_gz`
- `colcon`
- `rosdep`
- `vcs`
- `just`
- PlatformIO（STM32 サンプルを使う場合）

VS Code の Dev Container を使う場合は、このリポジトリをコンテナで開いてください。

## セットアップ

依存リポジトリの取得と rosdep による依存パッケージのインストールを行います。

```bash
just deps
```

続けて、ワークスペースをビルドします。

```bash
just build
source install/setup.bash
```

新しいターミナルを開いた場合も、実行前に `source install/setup.bash` を実行してください。

## ロボットモデルを RViz で表示する

```bash
ros2 launch lecture_description display.launch.py
```

Joint State Publisher の GUI が不要な場合は、次のように起動できます。

```bash
ros2 launch lecture_description display.launch.py gui:=False
```

## シミュレーションを起動する

フィールドとロボットを Gazebo Sim で起動します。

```bash
ros2 launch lecture_simulation simulation.launch.py
```

GUI を表示せずに実行する場合は `headless:=True` を指定します。

```bash
ros2 launch lecture_simulation simulation.launch.py headless:=True
```

初期位置は `x_pose`、`y_pose`、`z_pose`、`roll`、`pitch`、`yaw` で変更できます。

```bash
ros2 launch lecture_simulation simulation.launch.py x_pose:=0.0 y_pose:=0.0 yaw:=1.57
```

シミュレーションでは、主に次のトピックを Gazebo と ROS 2 の間でブリッジします。

- ROS 2 から Gazebo: `/cmd_vel`
- Gazebo から ROS 2: `/clock`、`joint_states`、`odom`、`tf`、`imu`、`scan`
- カメラ: `/rgbd_camera/image`、`/rgbd_camera/depth_image`、`/rgbd_camera/camera_info`

## ゲームパッド操作

ゲームパッドを接続して、Joy ノード、`joy_to_cmd_vel` ノード、動作確認用の turtlesim を起動します。

```bash
ros2 launch lecture_teleop teleop.launch.py
```

`joy_to_cmd_vel` は `/joy` を購読し、移動指令を `/cmd_vel` に配信します。このパッケージは Joy メッセージから Twist メッセージへの変換処理を実装する講習用の構成です。

シミュレーションのロボットを操作するときは、シミュレーション、Joy ノード、変換ノードを別々のターミナルで起動します。

```bash
# ターミナル 1
ros2 launch lecture_simulation simulation.launch.py

# ターミナル 2
ros2 run joy joy_node

# ターミナル 3
ros2 run lecture_teleop joy_to_cmd_vel
```

## ROS 2 と STM32 の UART 通信

サンプルは 115200 bps を使用し、既定のポートは `/dev/ttyACM0` です。STM32 側は NUCLEO-F303K8 向けの PlatformIO プロジェクトです。

### STM32 から受信する

`stm32/uart_send` を STM32 に書き込み、PC 側の受信ノードを起動します。

```bash
just run uart_recv
```

別のシリアルポートを使う場合は launch 引数で指定します。

```bash
just run uart_recv port:=/dev/ttyUSB0
```

STM32 は1秒ごとにカウント値を送信し、ROS 2 ノードは受信内容をログに表示します。

### STM32 へ送信する

`stm32/uart_recv` を STM32 に書き込み、PC 側の送信ノードを起動します。

```bash
just run uart_send
```

```bash
just run uart_send port:=/dev/ttyUSB0
```

ROS 2 ノードは1秒ごとに文字列を送信し、STM32 は受信した文字列をエコーバックします。

シリアルポートを開けない場合は、デバイス名とアクセス権限を確認してください。

```bash
ls -l /dev/ttyACM* /dev/ttyUSB*
```

## 開発コマンド

```bash
# 利用できるコマンドを表示
just

# 依存関係をインストール
just deps

# 全パッケージ、または指定パッケージをビルド
just build
just build lecture_teleop

# 全パッケージ、または指定パッケージをテスト
just test
just test lecture_teleop

# lecture_bringup の launch ファイルを実行
just run uart_recv

# フォーマット
just format

# ビルド生成物を削除
just clean
```

## ディレクトリ構成

```text
.
├── lecture_description/   # ロボットモデルと RViz 設定
├── lecture_simulation/    # Gazebo Sim のワールドと launch
├── lecture_teleop/        # ゲームパッド操作
├── lecture_teleop_cpp/    # rclcpp版を実装する講習用の雛形
├── serial_communication/  # ROS 2 UART ノード
├── lecture_bringup/       # UART launch ファイル
├── stm32/                 # PlatformIO サンプル
├── python_practice/       # Python 練習コード
├── build_depends.repos    # vcs import 用の依存定義
└── justfile               # 開発コマンド
```

## フォーマットとテスト

```bash
pre-commit install
pre-commit run --all-files
```

CI では ROS 2 Jazzy 環境で、依存関係のインストール、フォーマット、ビルド、テストを実行します。
