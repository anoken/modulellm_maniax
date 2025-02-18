// Copyright (c) 2025 aNoken


#include <cstdio>
#include <vector>
#include <opencv2/opencv.hpp>
#include "base/common.hpp"
#include "middleware/io.hpp"
#include "utilities/cmdline.hpp"
#include "utilities/file.hpp"
#include <ax_sys_api.h>
#include <ax_engine_api.h>
#include <unistd.h>

const int DEFAULT_H = 256;
const int DEFAULT_W = 384;
const int STREAM_PORT = 8888;
const int FRAME_WAIT = 10000;  // 10ms
const char* DEFAULT_MODEL = 
    "/opt/m5stack/data/depth-anything-ax630c/depth_anything.axmodel";

namespace ax {
// 深度マップの計算
cv::Mat process_depth(
    AX_ENGINE_IO_INFO_T* io_info,
    AX_ENGINE_IO_T* io_data,
    const cv::Mat& frame
) {
    auto& output = io_data->pOutputs[0];
    auto& info = io_info->pOutputs[0];
    
    cv::Mat depth(info.pShape[2], info.pShape[3], CV_32FC1, output.pVirAddr);
    double min_val, max_val;
    cv::minMaxLoc(depth, &min_val, &max_val);
    
    depth = (depth - min_val) * 255.0 / (max_val - min_val);
    depth.convertTo(depth, CV_8UC1);
    
    cv::Mat result;
    cv::applyColorMap(depth, result, cv::COLORMAP_MAGMA);
    cv::resize(result, result, frame.size());
    
    cv::Mat combined;
    cv::hconcat(std::vector<cv::Mat>{frame, result}, combined);
    return combined;
}

// 推論実行
bool run_inference(
    AX_ENGINE_HANDLE handle,
    AX_ENGINE_IO_INFO_T* io_info,
    AX_ENGINE_IO_T* io_data,
    const cv::Mat& frame,
    cv::Mat& result
) {
    std::vector<uint8_t> img_data(DEFAULT_H * DEFAULT_W * 3);
    common::get_input_data_no_letterbox(
        frame,
        img_data,
        DEFAULT_H,
        DEFAULT_W,
        true
    );
    
    if (middleware::push_input(img_data, io_data, io_info) != 0) return false;
    if (AX_ENGINE_RunSync(handle, io_data) != 0) return false;
    
    result = process_depth(io_info, io_data, frame);
    return true;
}
}  // namespace ax

int main(int argc, char* argv[]) {
    cmdline::parser cmd;
    cmd.add<std::string>("model", 'm', "Model file", false, DEFAULT_MODEL);
    cmd.parse_check(argc, argv);
    
    auto model_path = cmd.get<std::string>("model");
    if (!utilities::file_exist(model_path)) {
        fprintf(stderr, "Model file not found: %s\n", model_path.c_str());
        return -1;
    }
    
    // カメラとストリーミングの初期化
    cv::VideoCapture cap;
    cap.open(0);
    cv::VideoWriter stream;
    stream.open("httpjpg", STREAM_PORT);
    
    if (!cap.isOpened()) {
        fprintf(stderr, "Failed to open camera\n");
        return -1;
    }
    
    // NPUの初期化
    AX_SYS_Init();

    AX_ENGINE_NPU_ATTR_T npu_attr;
    memset(&npu_attr, 0, sizeof(npu_attr));
    npu_attr.eHardMode = AX_ENGINE_VIRTUAL_NPU_DISABLE;
    if (AX_ENGINE_Init(&npu_attr) != 0) {
        fprintf(stderr, "Failed to initialize NPU\n");
        return -1;
    }
    
    // モデルの読み込み
    std::vector<char> model_data;
    if (!utilities::read_file(model_path, model_data)) {
        fprintf(stderr, "Failed to load model: %s\n", model_path.c_str());
        return -1;
    }
    
    // 推論エンジンの設定
    AX_ENGINE_HANDLE handle;
    if (AX_ENGINE_CreateHandle(
        &handle,
        model_data.data(),
        model_data.size()
    ) != 0) {
        AX_ENGINE_Deinit();
        return -1;
    }
    
    AX_ENGINE_IO_INFO_T* io_info;
    if (AX_ENGINE_GetIOInfo(handle, &io_info) != 0) {
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return -1;
    }
    
    AX_ENGINE_IO_T io_data;
    if (middleware::prepare_io(
        io_info,
        &io_data,
        std::make_pair(AX_ENGINE_ABST_DEFAULT, AX_ENGINE_ABST_CACHED)
    ) != 0) {
        AX_ENGINE_DestroyHandle(handle);
        AX_ENGINE_Deinit();
        return -1;
    }
    
    fprintf(stdout, "Model: %s\n", model_path.c_str());
    fprintf(stdout, "Streaming started: http://<server-ip>:%d\n", STREAM_PORT);
    
    // メインループ
    cv::Mat frame, result;
    while (true) {
        cap >> frame;
        if (frame.empty()) continue;
        
        if (!ax::run_inference(handle, io_info, &io_data, frame, result)) {
            fprintf(stderr, "Inference execution error\n");
            break;
        }
        stream << result;

        usleep(FRAME_WAIT);
    }
    
    // リソースの解放
    middleware::free_io(&io_data);
    AX_ENGINE_DestroyHandle(handle);
    AX_ENGINE_Deinit();
    AX_SYS_Deinit();
    
    return 0;
}