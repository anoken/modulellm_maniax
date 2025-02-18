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
#include <ax_sys_api.h>
#include <ax_engine_api.h>

// 基本設定
const int DEFAULT_SIZE[] = {256, 384};  // 高さ, 幅

namespace ax {
// 深度マップの後処理と可視化
void visualize_depth(
    AX_ENGINE_IO_INFO_T* io_info,
    AX_ENGINE_IO_T* io_data,
    const cv::Mat& orig_img,
    float process_time
) {
    auto& output = io_data->pOutputs[0];
    auto& info = io_info->pOutputs[0];
    
    // 深度マップの正規化と可視化
    cv::Mat depth(info.pShape[2], info.pShape[3], CV_32FC1, output.pVirAddr);
    double min_val, max_val;
    cv::minMaxLoc(depth, &min_val, &max_val);
    
    depth = (depth - min_val) * 255.0 / (max_val - min_val);
    depth.convertTo(depth, CV_8UC1);
    
    // カラーマップの適用
    cv::Mat result;
    cv::applyColorMap(depth, result, cv::COLORMAP_MAGMA);
    cv::resize(result, result, orig_img.size());
    
    // 結果の保存
    cv::Mat combined;
    cv::hconcat(std::vector<cv::Mat>{orig_img, result}, combined);
    cv::imwrite("depth_result.png", combined);
    
    fprintf(stdout, "Processing time: %.2f ms\n", process_time);
}

// モデル実行の主要処理
bool run_inference(
    const std::string& model_path,
    const std::vector<uint8_t>& img_data,
    const cv::Mat& orig_img
) {
    // エンジンの初期化
    AX_ENGINE_NPU_ATTR_T npu_attr;
    memset(&npu_attr, 0, sizeof(npu_attr));
    npu_attr.eHardMode = AX_ENGINE_VIRTUAL_NPU_DISABLE;
    if (AX_ENGINE_Init(&npu_attr) != 0) {
        fprintf(stderr, "Failed to initialize NPU\n");
        return false;
    }
    
    // モデルの読み込みと設定
    std::vector<char> model_data;
    if (!utilities::read_file(model_path, model_data)) {
        fprintf(stderr, "Failed to load model: %s\n", model_path.c_str());
        return -1;
    }

    // 推論エンジンの設定
    AX_ENGINE_HANDLE handle;
    if (AX_ENGINE_CreateHandle(&handle, model_data.data(), model_data.size()) != 0) {
        AX_ENGINE_Deinit();
        return false;
    }
    
    // 入出力の設定
    AX_ENGINE_IO_INFO_T* io_info;
    AX_ENGINE_IO_T io_data;
    if (AX_ENGINE_GetIOInfo(handle, &io_info) != 0 ||
        middleware::prepare_io(
            io_info,
            &io_data,
            std::make_pair(AX_ENGINE_ABST_DEFAULT, AX_ENGINE_ABST_CACHED)
        ) != 0
    ) {
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return false;
    }
    
    // 入力データの設定
    if (middleware::push_input(img_data, &io_data, io_info) != 0) {
        middleware::free_io(&io_data);
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return false;
    }
    
    // 推論実行と時間計測
    timer t;
    if (AX_ENGINE_RunSync(handle, &io_data) != 0) {
        middleware::free_io(&io_data);
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return false;
    }
    float process_time = t.cost();
    
    // 結果の後処理
    visualize_depth(io_info, &io_data, orig_img, process_time);
    
    // リソースの解放
    middleware::free_io(&io_data);
    AX_ENGINE_DestroyHandle(handle);
    AX_ENGINE_Deinit();
    return true;
}
}  // namespace ax

int main(int argc, char* argv[]) {
    // コマンドライン引数の処理
    cmdline::parser cmd;
    cmd.add<std::string>("model", 'm', "モデルファイル", true, "");
    cmd.add<std::string>("image", 'i', "画像ファイル", true, "");
    cmd.add<std::string>(
        "size",
        'g',
        "入力サイズ (H,W)",
        false,
        std::to_string(DEFAULT_SIZE[0]) + "," + std::to_string(DEFAULT_SIZE[1])
    );
    cmd.parse_check(argc, argv);
    
    // 入力ファイルの確認
    if (!utilities::file_exist(cmd.get<std::string>("model")) ||
        !utilities::file_exist(cmd.get<std::string>("image"))
    ) {
        fprintf(stderr, "Input files not found\n");
        return -1;
    }
    
    // 画像の読み込みと前処理
    cv::Mat orig_img = cv::imread(cmd.get<std::string>("image"));
    if (orig_img.empty()) return -1;
    
    std::array<int, 2> size = {DEFAULT_SIZE[0], DEFAULT_SIZE[1]};
    if (!utilities::parse_string(cmd.get<std::string>("size"), size)) return -1;
    
    std::vector<uint8_t> img_data(size[0] * size[1] * 3);
    common::get_input_data_no_letterbox(
        orig_img,
        img_data,
        size[0],
        size[1],
        true
    );
    
    // 推論実行
    AX_SYS_Init();
    bool result = ax::run_inference(
        cmd.get<std::string>("model"),
        img_data,
        orig_img
    );
    AX_SYS_Deinit();
    
    return result ? 0 : -1;
}