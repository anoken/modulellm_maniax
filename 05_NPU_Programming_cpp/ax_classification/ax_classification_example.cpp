// Copyright (c) 2025 aNoken


#include <cstdio>
#include <vector>
#include <opencv2/opencv.hpp>
#include "base/common.hpp"
#include "middleware/io.hpp"
#include "utilities/args.hpp"
#include "utilities/cmdline.hpp"
#include "utilities/file.hpp"
#include "utilities/timer.hpp"
#include "base/score.hpp"
#include "base/topk.hpp"
#include <ax_sys_api.h>
#include <ax_engine_api.h>

// デフォルトの入力サイズを定義
const int DEFAULT_IMG_SIZE = 224;

namespace ax {
// 推論結果の後処理を行う関数
void post_process(AX_ENGINE_IO_INFO_T* io_info, AX_ENGINE_IO_T* io_data) {
    // 出力データの取得と分類スコアの計算
    auto& output = io_data->pOutputs[0];
    auto& info = io_info->pOutputs[0];
    auto ptr = (float*)output.pVirAddr;
    auto class_num = info.nSize / sizeof(float);
    
    // スコアの計算と並べ替え
    std::vector<classification::score> result(class_num);
    for (uint32_t id = 0; id < class_num; id++) {
        result[id].id = id;
        result[id].score = ptr[id];
    }
    classification::sort_score(result);
    classification::print_score(result, 5);
}

// モデル実行の本体関数
bool run_model(const std::string& model, const std::vector<uint8_t>& data) {
    // エンジンの初期化
    AX_ENGINE_NPU_ATTR_T npu_attr;
    memset(&npu_attr, 0, sizeof(npu_attr));
    npu_attr.eHardMode = AX_ENGINE_VIRTUAL_NPU_DISABLE;
    if (AX_ENGINE_Init(&npu_attr) != 0) {
        return false;
    }

    // モデルファイルの読み込み
    std::vector<char> model_buffer;
    if (!utilities::read_file(model, model_buffer)) {
        fprintf(stderr, "モデルファイルの読み込みに失敗: %s\n", model.c_str());
        return false;
    }

    // モデルハンドルとコンテキストの作成
    AX_ENGINE_HANDLE handle;
    if (AX_ENGINE_CreateHandle(&handle, model_buffer.data(), 
            model_buffer.size()) != 0) {
        AX_ENGINE_Deinit();
        return false;
    }

    if (AX_ENGINE_CreateContext(handle) != 0) {
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return false;
    }

    // 入出力情報の設定
    AX_ENGINE_IO_INFO_T* io_info;
    if (AX_ENGINE_GetIOInfo(handle, &io_info) != 0) {
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return false;
    }

    // 入出力バッファの準備
    AX_ENGINE_IO_T io_data;
    if (middleware::prepare_io(io_info, &io_data, 
            std::make_pair(AX_ENGINE_ABST_DEFAULT, AX_ENGINE_ABST_CACHED)) != 0) {
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return false;
    }

    // 入力データの設定
    if (middleware::push_input(data, &io_data, io_info) != 0) {
        middleware::free_io(&io_data);
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return false;
    }

    // 推論の実行
    if (AX_ENGINE_RunSync(handle, &io_data) != 0) {
        middleware::free_io(&io_data);
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return false;
    }

    // 結果の処理と表示
    post_process(io_info, &io_data);

    // リソースの解放
    middleware::free_io(&io_data);
    AX_ENGINE_DestroyHandle(handle);
    AX_ENGINE_Deinit();
    return true;
}
}  // namespace ax

int main(int argc, char* argv[]) {
    // コマンドライン引数の解析
    cmdline::parser cmd;
    cmd.add<std::string>("model", 'm', "モデルファイル", true, "");
    cmd.add<std::string>("image", 'i', "画像ファイル", true, "");
    cmd.add<std::string>("size", 'g', "入力サイズ (高さ,幅)", false, 
        std::to_string(DEFAULT_IMG_SIZE) + "," + 
        std::to_string(DEFAULT_IMG_SIZE));
    cmd.parse_check(argc, argv);

    // 入力ファイルの存在確認
    auto model_file = cmd.get<std::string>("model");
    auto image_file = cmd.get<std::string>("image");
    if (!utilities::file_exist(model_file) || 
            !utilities::file_exist(image_file)) {
        fprintf(stderr, "入力ファイルが見つかりません\n");
        return -1;
    }

    // 入力サイズの解析
    std::array<int, 2> input_size = {DEFAULT_IMG_SIZE, DEFAULT_IMG_SIZE};
    if (!utilities::parse_string(cmd.get<std::string>("size"), input_size)) {
        fprintf(stderr, "入力サイズの指定が不正です\n");
        return -1;
    }

    // 画像の読み込みと前処理
    std::vector<uint8_t> image(input_size[0] * input_size[1] * 3, 0);
    cv::Mat mat = cv::imread(image_file);
    if (mat.empty()) {
        fprintf(stderr, "画像の読み込みに失敗\n");
        return -1;
    }
    common::get_input_data_centercrop(mat, image, input_size[0], input_size[1]);

    // システムの初期化と推論実行
    AX_SYS_Init();
    bool result = ax::run_model(model_file, image);
    AX_SYS_Deinit();

    return result ? 0 : -1;
}