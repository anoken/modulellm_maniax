## Copyright (c) 2025 aNoken

# 最小CMakeバージョンの指定
cmake_minimum_required(VERSION 3.13)

# クロスコンパイル設定
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)

# プロジェクト名の設定
project(ax_depth_anything_image)

# ビルド設定
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall")

# 依存ライブラリのパス設定
set(OpenCV_DIR 
    /opt/ax-samples/3rdparty/opencv-aarch64-linux/lib/cmake/opencv4/
)
set(BSP_MSP_DIR /opt/ax620e_bsp_sdk/msp/out)
set(AX_SAMPLES_DIR /opt/ax-samples/examples)

# ターゲット名の設定
set(TARGET_NAME ax_depth_anything_image)

# OpenCVの検索
find_package(OpenCV REQUIRED)

# インクルードディレクトリの設定
include_directories(
   ${OpenCV_INCLUDE_DIRS}
   ${BSP_MSP_DIR}/arm64_glibc/include
   ${AX_SAMPLES_DIR}
   ${AX_SAMPLES_DIR}/ax620e
)

# 実行ファイルの追加
add_executable(${TARGET_NAME} ax_depth_anything_image.cpp)

# リンクディレクトリの設定
target_link_directories(${TARGET_NAME} PRIVATE ${BSP_MSP_DIR}/arm64_glibc/lib)

# ライブラリのリンク設定
target_link_libraries(${TARGET_NAME} PRIVATE ${OpenCV_LIBS} 
   ax_engine ax_interpreter ax_sys)


