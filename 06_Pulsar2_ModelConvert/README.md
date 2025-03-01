

## Docker のPulsar2 イメージロード

```bash
$ sudo docker load -i ax_pulsar2_3.3.tar.gz
```

Pulsar2 の入手ページ：<br>
https://huggingface.co/AXERA-TECH/Pulsar2/tree/main<br>

### Pulsar2 の起動手順

```bash
$ sudo docker run -it --net host --rm -v $PWD:/data pulsar2:3.3
```

### Pulsar2 でのモデル変換

- MobileNetV2の変換

```bash
$ python mobilenet_v2_onnx_export.py

#Pulsar2 の起動
$ sudo docker run -it --net host --rm -v $PWD:/data pulsar2:3.3

$ pulsar2 build --config mobilenetv2_config.json
```

- YOLO11の変換

```bash
$ python 02_yolo11_onnx_export.py
$ python 02_yolo11_cut_onnx.py

#Pulsar2 の起動
$ sudo docker run -it --net host --rm -v $PWD:/data pulsar2:3.3

$ pulsar2 build --config config/yolo11_config.json
```

- 行列計算モデルの変換

```
$ python 03_matmul_model_export.py
$ python 03_calibdata_gen.py

#Pulsar2 の起動
$ sudo docker run -it --net host -v $PWD:/data pulsar2:3.3

$ pulsar2 build --config config/matmul_model.json
```
