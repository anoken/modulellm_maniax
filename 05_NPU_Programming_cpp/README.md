# ライブラリのインストール

Module-LLMのC++開発環境を構築します。

## クロスコンパイラのインストール

Module-LLMのax630cはArmの64Bitプロセッサを搭載しているため、aarch64用のクロスコンパイラをインストールします。

```bash
sudo apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
```

## AX620Q BSP SDKのダウンロード

AX620E BSP SDKをAXERAのGitHubリポジトリからダウンロードし、/opt/に配置します。

```bash
git clone https://github.com/AXERA-TECH/ax620e_bsp_sdk.git
sudo cp -r ax620q_bsp_sdk /opt/
```

## ax-samplesのダウンロード

AXERAのC++言語用のサンプルプログラム「ax-samples」をダウンロードし、/opt/に配置します。

```bash
git clone https://github.com/AXERA-TECH/ax-samples
sudo cp -r ax-samples /opt/
```

## OpenCV-Mobileのインストール

エッジデバイス向けに最適化された軽量版OpenCVライブラリOpenCV-Mobileをインストールします。

```bash
cd /opt/ax-samples
mkdir -p ./3rdparty
wget https://github.com/anoken/modulellm_maniax/releases/download/opencv_mobile/opencv-aarch64-linux.zip
unzip opencv-aarch64-linux.zip -d ./3rdparty
```

