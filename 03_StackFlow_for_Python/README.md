## overview
Module-LLMのStackFlowサービスのAPIを使って、PCのPythonからStackFlowサービスにアクセスするサンプル。<br>



## preparation

```
# 必要なパッケージのインストール
pip install -r requirements.txt
```

## StackFlow Python一覧

```
python llm-qwen2.5-0.5B.py  
# LLMのサンプルプログラムです。モデル：qwen2.5-0.5B

python llm-qwen2.5-1.5B.py  
# LLMのサンプルプログラムです。モデル：qwen2.5-1.5B

python llm-llama3.2-1B.py  
# LLMのサンプルプログラムです。モデル：llama3.2-1B

python openbuddy-llama3.2-1B.py  
# LLMのサンプルプログラムです。モデル：openbuddy-llama3.2-1B.py

python sys-ping.py  
# Module-LLMの情報です。

python sys-hwinfo.py  
# Module-LLMのハードウェア情報です。

python sys-lsmode.py  
# LLMサービスのモデルが一覧で取得できます。

python  sys-reboot.py
# Module-LLMが再起動します。

python  sys-reset.py
# LLMサービスがリセットされます。

python melotts-script.py  
# melottsで音声合成します。

python tts-ip-script.py
# ttsで音声合成します。

```




## Version情報
LLM Module Firmware Upgrade https://docs.m5stack.com/en/guide/llm/llm/image
からdebをダウンロードしてインストールする。
インストールしてある,LLMのサービスは以下で確認します。
```
root@m5stack-LLM:~# dpkg -l | grep llm
ii  lib-llm                                                   1.4                                     arm64        llm-module
ii  llm-asr                                                   1.3                                     arm64        llm-module
ii  llm-audio                                                 1.3                                     arm64        llm-module
ii  llm-audio-en-us                                           0.2                                     arm64        llm-module
ii  llm-audio-zh-cn                                           0.2                                     arm64        llm-module
ii  llm-camera                                                1.3                                     arm64        llm-module
ii  llm-depth-anything                                        1.3                                     arm64        llm-module
ii  llm-kws                                                   1.3                                     arm64        llm-module
ii  llm-llama3.2-1b-prefill-ax630c                            0.2                                     arm64        llm-module
ii  llm-llm                                                   1.4                                     arm64        llm-module
ii  llm-melotts                                               1.3                                     arm64        llm-module
ii  llm-melotts-zh-cn                                         0.2                                     arm64        llm-module
ii  llm-openbuddy-llama3.2-1b-ax630c                          0.2                                     arm64        llm-module
ii  llm-qwen2.5-0.5b-prefill-20e                              0.2                                     arm64        llm-module
ii  llm-qwen2.5-1.5b-ax630c                                   0.3                                     arm64        llm-module
ii  llm-qwen2.5-coder-0.5b-ax630c                             0.2                                     arm64        llm-module
ii  llm-sherpa-ncnn-streaming-zipformer-20m-2023-02-17        0.2                                     arm64        llm-module
ii  llm-sherpa-ncnn-streaming-zipformer-zh-14m-2023-02-23     0.2                                     arm64        llm-module
ii  llm-sherpa-onnx-kws-zipformer-gigaspeech-3.3m-2024-01-01  0.3                                     arm64        llm-module
ii  llm-sherpa-onnx-kws-zipformer-wenetspeech-3.3m-2024-01-01 0.3                                     arm64        llm-module
ii  llm-single-speaker-english-fast                           0.2                                     arm64        llm-module
ii  llm-single-speaker-fast                                   0.2                                     arm64        llm-module
ii  llm-skel                                                  1.3                                     arm64        llm-module
ii  llm-sys                                                   1.3                                     arm64        llm-module
ii  llm-tts                                                   1.3                                     arm64        llm-module
ii  llm-vlm                                                   1.4                                     arm64        llm-module
ii  llm-yolo                                                  1.4                                     arm64        llm-module
ii  llm-yolo11n                                               0.2                                     arm64        llm-module
ii  llm-yolo11n-hand-pose                                     0.3                                     arm64        llm-module
ii  llm-yolo11n-pose                                          0.3                                     arm64        llm-module
ii  llm-yolo11n-seg                                           0.2                                     arm64        llm-module
```

