# Pulsar2 でLLM モデルを変換

## TinySwallow-1.5Bモデルの変換


```bash
UbuntuPC$ git clone https://github.com/AXERA-TECH/ax-llm-build.git
UbuntuPC$ mkdir -p TinySwallow-1.5B-Instruct

# TinySwallow-1.5B-Instructのダウンロード
UbuntuPC$ huggingface-cli download --resume-download SakanaAI/TinySwallow-1.5B-Instruct --local-dir TinySwallow-1.5B-Instruct

# Pulsar2の起動
UbuntuPC$ sudo docker run -it --net host -v $PWD:/data pulsar2:3.3

# LLMモデルの変換
root@pulsar2:/data# pulsar2 llm_build --input_path TinySwallow-1.5B-Instruct --output_path TinySwallow-1.5B-Instruct-AX620E --kv_cache_len 1023 --hidden_state_type bf16 --prefill_len 128 --chip AX620E

# embedding(埋め込み)処理の実行
root@pulsar2:/data# chmod +x ./tools/fp32_to_bf16
root@pulsar2:/data# chmod +x ./tools/embed_process.sh
root@pulsar2:/data# ./tools/embed_process.sh TinySwallow-1.5B-Instruct TinySwallow-1.5B-Instruct-AX620E

# axmodelが生成されていることの確認
root@pulsar2:/data# ls TinySwallow-1.5B-Instruct-AX620E
qwen2_p128_l0_together.axmodel       qwen2_p128_l22_together.axmodel 
qwen2_p128_l10_together.axmodel      qwen2_p128_l23_together.axmodel
qwen2_p128_l11_together.axmodel      qwen2_p128_l24_together.axmodel
qwen2_p128_l12_together.axmodel      qwen2_p128_l25_together.axmodel
qwen2_p128_l13_together.axmodel      qwen2_p128_l26_together.axmodel
qwen2_p128_l14_together.axmodel      qwen2_p128_l27_together.axmodel
qwen2_p128_l15_together.axmodel      qwen2_p128_l2_together.axmodel
qwen2_p128_l16_together.axmodel      qwen2_p128_l3_together.axmodel
qwen2_p128_l17_together.axmodel      qwen2_p128_l4_together.axmodel
qwen2_p128_l18_together.axmodel      qwen2_p128_l5_together.axmodel
qwen2_p128_l19_together.axmodel      qwen2_p128_l6_together.axmodel
qwen2_p128_l1_together.axmodel       qwen2_p128_l7_together.axmodel
qwen2_p128_l20_together.axmodel      qwen2_p128_l8_together.axmodel
qwen2_p128_l21_together.axmodel      qwen2_p128_l9_together.axmodel
qwen2_post.axmodel
model.embed_tokens.weight.bfloat16.bin 
model.embed_tokens.weight.float32.bin    #一時ファイルのため削除可
model.embed_tokens.weight.npy            #一時ファイルのため削除可
```

