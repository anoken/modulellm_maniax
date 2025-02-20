import axengine as axe
import numpy as np
import time

# 入力データの準備
matrix = np.random.randn(4, 4).astype(np.float32)
points = np.random.randn(4, 1).astype(np.float32)

# ONNXセッションの初期化
session = axe.InferenceSession("onnx_matmul.axmodel")
input_name_matrix = session.get_inputs()[0].name
input_name_points = session.get_inputs()[1].name

# 推論実行と時間計測
n_iterations = 1000
times = []

print("\nMatrix:")
print(matrix)
print("\nPoints:")
print(points)

# 10回の推論実行と時間計測
for i in range(10):
    start = time.perf_counter()
    output = session.run(None, {input_name_matrix: matrix, input_name_points: points})
    inference_time = (time.perf_counter() - start) * 1000  # ミリ秒に変換
    print(f"\nInference {i+1}")
    print(f"Time: {inference_time:.3f} ms")
    print(f"Matrix x Points:")
    print(output[0])
