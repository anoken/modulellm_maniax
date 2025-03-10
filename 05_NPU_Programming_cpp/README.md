# 第5章:C++でNPU推論

- ax_classification:<br>
 MobileNetV2の推論プログラム<br>
- ax_depth_anything:<br>
 DepthAnything の推論プログラム<br>
- camera_streaming:<br>
 USB カメラの画像をストリーミング配信<br>
- ax_depth_anything_video_stream:<br>
  DepthAnything の推論をストリーミング配信<br>


#  preparation

Module-LLMのC++開発環境を構築します。<br>

ax620e_bsp_sdk: https://github.com/AXERA-TECH/ax620e_bsp_sdk<br>
ax-samples: https://github.com/AXERA-TECH/ax-samples<br>
opencv-mobile: https://github.com/nihui/opencv-mobile<br>

## クロスコンパイラのインストール

Module-LLMのax630cはArmの64Bitプロセッサを搭載しているため、aarch64用のクロスコンパイラをインストールします。

```bash
$sudo apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
```

## AX620Q BSP SDKのダウンロード

AX620E BSP SDKをAXERAのGitHubリポジトリからダウンロードし、/opt/に配置します。

```bash
$git clone https://github.com/AXERA-TECH/ax620e_bsp_sdk
$sudo cp -r ax620q_bsp_sdk /opt/
```

## ax-samplesのダウンロード

AXERAのC++言語用のサンプルプログラム「ax-samples」をダウンロードし、/opt/に配置します。

```bash
$git clone https://github.com/AXERA-TECH/ax-samples
$sudo cp -r ax-samples /opt/
```

## OpenCV-Mobileのインストール

エッジデバイス向けに最適化された軽量版OpenCVライブラリOpenCV-Mobileをインストールします。

```bash
$cd /opt/ax-samples
$mkdir -p ./3rdparty
$wget https://github.com/anoken/modulellm_maniax/releases/download/opencv_mobile/opencv-aarch64-linux.zip
$unzip opencv-aarch64-linux.zip -d ./3rdparty
```

## ax_classificationのビルド

```bash
$ git clone https://github.com/anoken/modulellm_maniax/
$ cd 05_NPU_Programming_cpp/ax_classification
$ mkdir build
$ cd build
$ cmake ..
$ make
```
