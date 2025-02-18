## Copyright (c) 2025 aNoken

import axengine as axe
import numpy as np 
import cv2          
import argparse   
import time    

# 画像を前処理する関数
def process_image(image_path, size=(224, 224)):
    # 画像を読み込んでBGRからRGBに変換
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 画像を正方形にクロップ
    h, w = img.shape[:2]
    crop = min(w, h)
    x = (w - crop) // 2
    y = (h - crop) // 2
    img = img[y:y+crop, x:x+crop]
    
    # 指定サイズにリサイズし、バッチ次元を追加
    img = cv2.resize(img, size)
    img = np.expand_dims(img, 0)
    
    return img

# 上位k個の予測結果を取得する関数
def get_top_k_predictions(output, k=5):
    # 出力を1次元に変換
    output_flat = output[0].flatten()
    # スコアの高い順にk個のインデックスを取得
    idx = np.argsort(output_flat)[-k:][::-1]
    scores = output_flat[idx]
    
    return idx, scores

# メインの推論実行関数
def run_inference(model_path, image_path):
    # モデルをロードして推論セッションを作成
    session = axe.InferenceSession(model_path)
    # 画像を前処理
    input_tensor = process_image(image_path)
    # モデルの入力名を取得
    input_name = session.get_inputs()[0].name
    
    # 推論時間の計測開始
    start = time.perf_counter()
    # 推論を実行
    output = session.run(None, {input_name: input_tensor})
    # 推論時間の計算（ミリ秒単位）
    infer_time = (time.perf_counter() - start) * 1000
    
    # 上位の予測結果を取得
    indices, scores = get_top_k_predictions(output[0])
    
    # 結果の表示
    print(f"\n推論時間: {infer_time:.2f} ms")
    for i, (idx, score) in enumerate(zip(indices, scores), 1):
        print(f"Top {i}: クラス {idx} (確率: {score:.4f})")
    
    return output

# メインエントリーポイント
if __name__ == "__main__":
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description='分類推論')
    parser.add_argument('--model', default='/opt/data/npu/models/mobilenetv2.axmodel')
    parser.add_argument('--image', default='/opt/data/npu/images/cat.jpg')
    
    # 引数をパース
    args = parser.parse_args()
    # 推論を実行
    run_inference(args.model, args.image)

