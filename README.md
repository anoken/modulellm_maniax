# ModuleLLM_MAniaX

「ModuleLLM_MAniaX 」のサポートページです。<br>

<img src="https://github.com/user-attachments/assets/9e422008-01ea-4382-b793-dd8e373e3483" alt="image" width="640">

## 訂正とお詫びのお知らせ
[訂正とお詫びのお知らせ](Notice_Correction.md)

## 紹介
著者 aNo研<br>
A5サイズ・156ページ (148mm×210mmx9mm)<br>

M5StackのModule-LLM(LLMモジュール)は、AXERA社のAX630Cを搭載したコンパクトなモジュールです。このモジュールは大規模言語モデル（LLM）を実行できるだけでなく、CNN（畳み込みニューラルネットワーク）やTransformerなどのAIモデルを高性能NPU（ニューラルプロセッシングユニット）で処理することができます。<br>
本書ではModule-LLMの基本的な使い方から、画像処理やモデル変換といった応用テクニックまで、幅広く解説しています。<br>

EdgeAIとEdgeLLMの可能性を、当書籍とModule-LLMを通じて体験してみませんか？<br>

・サポートページ： https://github.com/anoken/modulellm_maniax<br><br>
・電子書籍：BOOTHで取り扱っています。https://anoken.booth.pm/items/6642202<br>
・書籍：スイッチサイエンスで取り扱っています。https://www.switch-science.com/products/10307<br>

## 改定履歴
・v1.3.0版発行: 2025年4月14日 本文161ページ、誤記訂正。<br>
・v1.2.0版発行: 2025年4月13日 本文161ページ、誤記訂正、「Module-LLM Kit」に関する追記。<br>
・v1.1.0版発行: 2025年4月08日 本文161ページ、誤記訂正。<br>
・v1.0.0版発行: 2025年2月27日 本文155ページ<br>

## 目次<br>
第1 章Module-LLM の紹介<br>
   1.1 M5Stack Module-LLM とは<br>
   1.2 M5Stack LLM630 Compute Kit とは<br>
   1.3 M5Stack とは<br>
   1.4 AXERA 社とは<br>
   1.5 AXERA AX630C とは<br>

第2 章Module-LLM をつかってみよう<br>
   2.1 Module-LLM とデバッグボードを繋ぐ<br>
   2.1.1 Module-LLM とデバッグボードの接続方法<br>
   2.2 ADB ツールを使ってログインする<br>
   2.3 Module-LLM でL チカ<br>
   2.3.1 Module-LLM のLED の役割<br>
   2.3.2 L チカをしてみる<br>
   2.3.3 Python からLED を制御する<br>
   2.4 Module-LLM の起動音の消し方<br>
   2.5 Module-LLM へファイル転送<br>
   2.6 Samba で共有フォルダを作る<br>
   2.7 メモリが足りない場合の対処<br>
   2.8 ファームウェアの更新手順<br>
   2.9 WSL2 のインストール<br>
   
第3 章StackFlow を使ってみよう<br>
   3.1 StackFlow とは？<br>
   3.2 StackFlow のdeb パッケージについて<br>
   3.3 StackFlow の起動と停止<br>
   3.4 StackFlow のインストール<br>
   3.5 StackFlow をPython から使ってみよう<br>
   3.6 StackFlow のllm-sys ユニットとは？<br>
   3.7 StackFlow からリセットをかける<br>
   3.8 StackFlow からLinux コマンド実行<br>
   3.9 StackFlow でLLM の推論をする<br>
   3.10 StackFlow でMeloTTS から発音を行う<br>
   3.11 StackFlow でWhisper から音声認識<br>
   3.12 StackFlow をビルドするには<br>

第4 章Python でNPU 推論<br>
   4.1 PyAXEngine とは？<br>
   4.2 PyAXEngine のインストール<br>
   4.3 MobileNetV2 の推論<br>
   4.4 YOLO11 の推論<br>
   4.5 DepthAnything の推論<br>
   4.6 USB カメラからの動画取得<br>
   4.7 USB カメラからのDepthAnything 推論<br>

第5 章C++ でNPU 推論<br>
   5.1 C++ 開発環境の準備<br>
   5.2 ライブラリのインストール<br>
   5.3 DepthAnything の推論プログラムの作成<br>
   5.4 USB カメラの画像をストリーミング配信する<br>
   5.5 USB カメラからのDepthAnything 推論<br>
   5.6 ax-samples のCV サンプルのビルド手順<br>
   5.7 OpenCV-Mobile のビルド手順<br>

第6 章Pulsar2 でモデル変換<br>
   6.1 量子化とは？<br>
   6.2 Pulsar2 ToolChain の概要<br>
   6.3 Pulsar2 のインストール<br>
   6.4 ライブラリのインストール<br>
   6.5 サンプルデータのダウンロード<br>
   6.6 MobileNetV2 モデルの変換<br>
   6.7 YOLO11 モデルの変換<br>
   6.8 行列計算モデルの変換<br>
   6.9 Pulsar2 が対応しているONNX オペレータ<br>

第7 章Pulsar2 でLLM モデルを変換<br>
   7.1 TinySwallow-1.5B とは？<br>
   7.2 huggingface_hub のインストール<br>
   7.3 TinySwallow-1.5B モデルのダウンロード<br>
<br>
Copyright (c) 2025 aNoken<br>

