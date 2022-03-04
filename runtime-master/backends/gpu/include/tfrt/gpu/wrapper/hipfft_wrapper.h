/*
 * Copyright 2021 The TensorFlow Runtime Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Thin wrapper around the hipfft API adding llvm::Error.
#ifndef TFRT_GPU_WRAPPER_HIPFFT_WRAPPER_H_
#define TFRT_GPU_WRAPPER_HIPFFT_WRAPPER_H_

#include "tfrt/gpu/wrapper/fft_wrapper.h"
#include "tfrt/gpu/wrapper/hipfft_stub.h"

namespace tfrt {
namespace gpu {
namespace wrapper {

raw_ostream& Print(raw_ostream& os, hipfftResult_t result);

llvm::Expected<hipfftType> FftTypeToHipfftType(FftType type);

llvm::Expected<LibraryVersion> HipfftGetVersion();

// Creates an opaque handle and allocates small data for the plan. Use
// HipfftMakePlanMany to do the plan generation.
llvm::Expected<OwningFftHandle> HipfftCreate();

// Frees all GPU resources associated with the handle and destroys internal data
// structures.
llvm::Error HipfftDestroy(hipfftHandle handle);

// Sets the stream for execution of hipFFT functions. Note that these functions
// may consist of many kernel invocations.
llvm::Error HipfftSetStream(hipfftHandle handle, hipStream_t stream);

llvm::Expected<size_t> HipfftMakePlanMany(hipfftHandle handle, int rank,
                                          llvm::ArrayRef<int64_t> n,
                                          llvm::ArrayRef<int64_t> inembed,
                                          int64_t istride, int64_t idist,
                                          llvm::ArrayRef<int64_t> onembed,
                                          int64_t ostride, int64_t odist,
                                          hipfftType type, int64_t batch);

llvm::Expected<size_t> HipfftGetSize(hipfftHandle handle);

llvm::Error HipfftSetWorkArea(hipfftHandle handle, Pointer<void> work_area);

llvm::Error HipfftExecC2C(hipfftHandle handle, hipfftComplex* input_data,
                          hipfftComplex* output_data, FftDirection direction);

llvm::Error HipfftExecZ2Z(hipfftHandle handle, hipfftDoubleComplex* input_data,
                          hipfftDoubleComplex* output_data,
                          FftDirection direction);

llvm::Error HipfftExecR2C(hipfftHandle handle, hipfftReal* input_data,
                          hipfftComplex* output_data);

llvm::Error HipfftExecD2Z(hipfftHandle handle, hipfftDoubleReal* input_data,
                          hipfftDoubleComplex* output_data);

llvm::Error HipfftExecC2R(hipfftHandle handle, hipfftComplex* input_data,
                          hipfftReal* output_data);

llvm::Error HipfftExecZ2D(hipfftHandle handle, hipfftDoubleComplex* input_data,
                          hipfftDoubleReal* output_data);

llvm::Error HipfftExec(hipfftHandle handle, Pointer<void> raw_input,
                       Pointer<void> raw_output, FftType type);

}  // namespace wrapper
}  // namespace gpu
}  // namespace tfrt

#endif  // TFRT_GPU_WRAPPER_HIPFFT_WRAPPER_H_
