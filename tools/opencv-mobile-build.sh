#!/bin/bash

# OpenCV version to build
OPENCV_VERSION="4.10.0"

# Function to print progress with timestamp
log_progress() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_progress "Starting OpenCV mobile build process for version ${OPENCV_VERSION}"

# Download and extract OpenCV source
log_progress "Downloading OpenCV source code..."
wget -q https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip -O opencv-${OPENCV_VERSION}.zip
log_progress "Extracting source code..."
unzip -q opencv-${OPENCV_VERSION}.zip
rm opencv-${OPENCV_VERSION}.zip

# Enter OpenCV directory
cd opencv-${OPENCV_VERSION}
log_progress "Entered OpenCV source directory"

# Clear existing GPU/CUDA related files and configurations
log_progress "Clearing GPU configurations..."
truncate -s 0 cmake/OpenCVFindLibsGrfmt.cmake
rm -rf modules/gapi

# Remove CUDA, DirectX, OpenGL, Intel GPU, OpenCL, and VA related files
log_progress "Removing GPU-related files from core module..."
# Core module cleanup - source files
log_progress "Cleaning up core module source files..."
rm -v modules/core/src/cuda_*
rm -v modules/core/src/direct*
rm -v modules/core/src/gl_*
rm -v modules/core/src/intel_gpu_*
rm -v modules/core/src/ocl*
rm -v modules/core/src/opengl.cpp
rm -v modules/core/src/ovx.cpp
rm -v modules/core/src/umatrix.hpp
rm -v modules/core/src/va_intel.cpp
rm -v modules/core/src/va_wrapper.impl.hpp

# Core module cleanup - include files
log_progress "Cleaning up core module include files..."
rm -v modules/core/include/opencv2/core/cuda*.hpp
rm -v modules/core/include/opencv2/core/directx.hpp
rm -v modules/core/include/opencv2/core/ocl*.hpp
rm -v modules/core/include/opencv2/core/opengl.hpp
rm -v modules/core/include/opencv2/core/ovx.hpp
rm -v modules/core/include/opencv2/core/private.cuda.hpp
rm -v modules/core/include/opencv2/core/va_*.hpp

# Core module cleanup - directories
log_progress "Cleaning up core module directories..."
rm -rfv modules/core/include/opencv2/core/cuda
rm -rfv modules/core/include/opencv2/core/opencl
rm -rfv modules/core/include/opencv2/core/openvx

# Photo module cleanup
log_progress "Cleaning up photo module..."
rm -v modules/photo/src/denoising.cuda.cpp
rm -v modules/photo/include/opencv2/photo/cuda.hpp

# Remove CUDA and OpenCL directories from all modules
log_progress "Removing CUDA and OpenCL files from all modules..."
find modules -type d | xargs -i rm -rfv {}/src/cuda
find modules -type d | xargs -i rm -rfv {}/src/opencl
find modules -type d | xargs -i rm -rfv {}/perf/cuda
find modules -type d | xargs -i rm -rfv {}/perf/opencl

# Remove GPU-related includes from source files
log_progress "Removing GPU-related includes from source files..."
for pattern in \
    'opencl_kernels' \
    'cuda.hpp' \
    'opengl.hpp' \
    'ocl_defs.hpp' \
    'ocl.hpp' \
    'ovx_defs.hpp' \
    'ovx.hpp' \
    'va_intel.hpp'; do
    log_progress "Removing ${pattern} references..."
    find modules -type f -exec sed -i "/${pattern}/d" {} +
done

# Apply patches
log_progress "Applying patches..."
patch -p1 -i ../patches/opencv-${OPENCV_VERSION}-no-gpu.patch
patch -p1 -i ../patches/opencv-${OPENCV_VERSION}-no-rtti.patch
patch -p1 -i ../patches/opencv-${OPENCV_VERSION}-no-zlib.patch
patch -p1 -i ../patches/opencv-${OPENCV_VERSION}-link-openmp.patch
patch -p1 -i ../patches/opencv-${OPENCV_VERSION}-fix-windows-arm-arch.patch
patch -p1 -i ../patches/opencv-${OPENCV_VERSION}-minimal-install.patch

# Copy custom drawing files
log_progress "Setting up custom drawing functionality..."
cp ../patches/draw_text.h ../patches/mono_font_data.h modules/imgproc/src/
cp ../patches/fontface.html ./
patch -p1 -i ../patches/opencv-${OPENCV_VERSION}-drawing-mono-font.patch

# Replace highgui module with custom version
log_progress "Replacing highgui module with custom version..."
rm -rf modules/highgui
cp -r ../highgui modules/

# Remove unnecessary components
log_progress "Removing unnecessary components..."
rm -rfv 3rdparty
rm -rfv apps
rm -rfv data
rm -rfv doc
rm -rfv samples
rm -rfv platforms

log_progress "Removing unnecessary modules..."
rm -rfv modules/java
rm -rfv modules/js
rm -rfv modules/python
rm -rfv modules/ts
rm -rfv modules/dnn

# Configure for mobile build
log_progress "Configuring for mobile build..."
sed -e "s/__VERSION__/${OPENCV_VERSION}/g" ../patches/Info.plist > ./Info.plist
cp ../opencv4_cmake_options.txt ./options.txt

# Create final package
cd ..
log_progress "Creating final package..."
mv opencv-${OPENCV_VERSION} opencv-mobile-${OPENCV_VERSION}
log_progress "Creating ZIP archive..."
zip -9 -r opencv-mobile-${OPENCV_VERSION}.zip opencv-mobile-${OPENCV_VERSION}

log_progress "Build process completed successfully!"
log_progress "Output file: opencv-mobile-${OPENCV_VERSION}.zip"