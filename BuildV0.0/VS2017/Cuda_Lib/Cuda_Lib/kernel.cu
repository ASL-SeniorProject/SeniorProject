
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include <time.h>

#include <stdio.h>
#include <stdlib.h>
//#include <atlimage.h>


enum color_transform_t
{
	grayscale,
	sRGB,
	LAB
};

enum transform_t
{
	Gaussian
};

#define SIZE 1000

//typedef struct
//{
//	int r;
//	int g;
//	int b;
//} rgb_t;
//
//typedef rgb_t* rgb_ptr;
//typedef rgb_ptr* rgb_list;
//typedef rgb_list* rgb_mat;
//

cudaError_t transform(uchar3 *dst_img, uchar3 *src_img, int img_size, int block_size, int grid_size, color_transform_t type);
cudaError_t transform();

// convert one scanline to grayscale in parallel
__global__ void grayscale_transform(uchar3 *dst_img, uchar3 *src_img, int img_size)
{
	unsigned int y = blockIdx.y * blockDim.y + threadIdx.y;
	unsigned int x = blockIdx.x * blockDim.x + threadIdx.x;
	unsigned int idx = y * SIZE + x;

	uchar3 rgb = src_img[idx];
	int average = (rgb.x + rgb.y + rgb.z) / 3;

	dst_img[idx].x = average;
	dst_img[idx].y = average;
	dst_img[idx].z = average;
}

void host_grayscale(uchar3 *dst_img, uchar3 *src_img, int img_size)
{
	for (int i = 0; i < SIZE * SIZE; i++)
	{
		uchar3 rgb = src_img[i];
		int average = (rgb.x + rgb.y + rgb.z) / 3;
		dst_img[i].x = average;
		dst_img[i].y = average;
		dst_img[i].z = average;
	}
}

int main()
{
	// genreate a dummy image
	int size = SIZE * SIZE;
	int img_size = size * sizeof(uchar3);
	int block_size = size / SIZE;
	int grid_size = size / block_size;

	//CImage img;
	uchar3 *src_img, *gray_img, srgb;

	src_img = (uchar3*)malloc(img_size);
	gray_img = (uchar3*)malloc(img_size);

	for (int i = 0; i < SIZE * SIZE; i++)
	{
		uchar3 src, gray;
		
		src.x = 128;
		src.y = 64;
		src.x = 256;

		gray.x = 0;
		gray.y = 0;
		gray.z = 0;

		src_img[i] = src;
		gray_img[i] = gray;
	}

	cudaError_t cudaStatus = transform(gray_img, src_img, img_size, block_size, grid_size, grayscale);
	if (cudaStatus != cudaSuccess) 
	{
		fprintf(stderr, "addWithCuda failed!");
		return 1;
	}
	cudaStatus = cudaDeviceReset();
	if (cudaStatus != cudaSuccess)
	{
	    fprintf(stderr, "cudadevicereset failed!");
	    return 1;
	}

	clock_t begin = clock();
	host_grayscale(gray_img, src_img, img_size);
	clock_t end = clock();
	double time_spent = 1000 * (double)(end - begin) / CLOCKS_PER_SEC;
	printf("CPU Execution Time: %32fms", time_spent);
	
	free(gray_img);
	free(src_img);
		
	return 0;
	system("pause");
	
	return 0;
	system("pause");
}

// transform an image
cudaError_t transform(uchar3 *dst_img, uchar3 *src_img, int img_size, int block_size, int grid_size, color_transform_t type)
{
	cudaError_t cudaStatus;
	uchar3 *t_src, *gpu_output;

	cudaStatus = cudaMalloc((void**)&t_src, img_size);
	if (cudaStatus != cudaSuccess)
		fprintf(stderr, "cudaMalloc failed!");

	cudaStatus = cudaMalloc((void**)&gpu_output, img_size);
	if (cudaStatus != cudaSuccess)
		fprintf(stderr, "cudaMalloc failed!");

	cudaStatus = cudaMemcpy(t_src, src_img, img_size, cudaMemcpyHostToDevice);
	if (cudaStatus != cudaSuccess)
		fprintf(stderr, "cudaMemcpy failed!");

	float et;
	cudaEvent_t start, stop;
	cudaEventCreate(&start);
	cudaEventCreate(&stop);
	cudaEventRecord(start);
	if (type == grayscale)
		grayscale_transform<<<grid_size, block_size>>>(gpu_output, t_src, img_size);
	cudaEventRecord(stop);
	cudaEventSynchronize(stop);
	cudaEventElapsedTime(&et, start, stop);
	printf("GPU Execution Time: %32fms\n", et);
	//// Check for any errors launching the kernel
    cudaStatus = cudaGetLastError();
    if (cudaStatus != cudaSuccess)
        fprintf(stderr, "addKernel launch failed: %s\n", cudaGetErrorString(cudaStatus));
    
    // cudaDeviceSynchronize waits for the kernel to finish, and returns
    // any errors encountered during the launch.
    cudaStatus = cudaDeviceSynchronize();
    if (cudaStatus != cudaSuccess)
        fprintf(stderr, "cudaDeviceSynchronize returned error code %d after launching addKernel!\n", cudaStatus);

    //// Copy output vector from GPU buffer to host memory.
    cudaStatus = cudaMemcpy(dst_img, gpu_output, img_size, cudaMemcpyDeviceToHost);
    if (cudaStatus != cudaSuccess)
        fprintf(stderr, "cudaMemcpy failed!");

	return cudaStatus;
}

//cudaError_t transform(rgb_mat dst_img, rgb_mat src_img, unsigned int img_size,  color_transform_t type);
//cudaError_t transform(rgb_t ***image, unsigned int line,  transform_t type);
//
//// convert one scanline to grayscale in parallel
//__global__ void grayscale_transform(rgb_list gpu_output, rgb_mat t_src, unsigned int line)
//{
//	unsigned int y = blockIdx.y * blockDim.y + threadIdx.y;
//	unsigned int x = blockIdx.x * blockDim.x + threadIdx.x;
//	unsigned int idx = y * 100 + x;
//
//	rgb_ptr src_rgb = t_src[y][x];
//
//	rgb_ptr gpu_rgb = nullptr;
//	gpu_rgb->r = 0;
//	gpu_rgb->g = 0;
//	gpu_rgb->b = 0;
//
//	double average = (src_rgb->r + src_rgb->g + src_rgb->b) / 3;
//
//	gpu_rgb->r = average;
//	gpu_rgb->g = average;
//	gpu_rgb->b = average;
//
//	gpu_output[idx] = gpu_rgb;
//}
//
//int main()
//{
//	// genreate a dummy image
//	int img_size = 100 * 100 * sizeof(rgb_ptr);
//	int block_size = 4;
//	int grid_size = 100000 / block_size;
//
//	rgb_mat src_img = (rgb_list*)malloc(100 * sizeof(rgb_list));
//	rgb_mat gray_img = (rgb_list*)malloc(100 * sizeof(rgb_list));
//
//	for (int y = 0; y < 100; y++)
//	{
//		src_img[y] = (rgb_list)malloc(100 * sizeof(rgb_ptr));
//		gray_img[y] = (rgb_list)malloc(100 * sizeof(rgb_ptr));
//		for (int x = 0; x < 100; x++)
//		{
//			src_img[y][x] = (rgb_ptr)malloc(sizeof(rgb_ptr));
//			gray_img[y][x] = (rgb_ptr)malloc(sizeof(rgb_ptr));
//		}
//	}
//
//
//	int i, j;
//	for (i = 0; i < 100; i++)
//	{
//		for (j = 0; j < 100; j++)
//		{
//			rgb_ptr s_p = src_img[i][j];
//			s_p->r = 128.0;
//			s_p->g = 76.0;
//			s_p->b = 256.0;
//			src_img[i][j] = s_p;
//
//			rgb_ptr g_p = gray_img[i][j];
//			g_p->r = 0.0;
//			g_p->g = 0.0;
//			g_p->b = 0.0;
//			gray_img[i][j] = g_p;
//		}
//	}
//
//	cudaError_t cudaStatus = transform(gray_img, src_img, img_size, block_size, grid_size, grayscale);
//	if (cudaStatus != cudaSuccess) 
//	{
//	    fprintf(stderr, "addWithCuda failed!");
//	    return 1;
//	}
//
//	//cudaStatus = cudaDeviceReset();
//	//if (cudaStatus != cudaSuccess)
//	//{
//	//    fprintf(stderr, "cudadevicereset failed!");
//	//    return 1;
//	//}
//
//	for (i = 0; i < 100; i++)
//	{
//		for (int j = 0; j < 100; j++)
//		{
//			rgb_ptr rgb = gray_img[i][j];
//			printf("%.3f : %.3f : %.3f\n", rgb->r, rgb->g, rgb->b);
//		}
//	}
//
//	free(gray_img);
//	free(src_img);
//	
//	return 0;
//	system("pause");
//}
//
//// transform an image
//cudaError_t transform(rgb_mat dst_img, rgb_mat src_img, unsigned int img_size, int block_size, int grid_size, color_transform_t type)
//{
//	rgb_mat t_src;
//	rgb_list gpu_output;
//	
//	cudaError_t cudaStatus;
//
//	cudaStatus = cudaMalloc((void**)&t_src, img_size);
//	if (cudaStatus != cudaSuccess)
//		fprintf(stderr, "cudaMalloc failed!");
//
//	cudaStatus = cudaMalloc((void**)&gpu_output, img_size);
//	if (cudaStatus != cudaSuccess)
//		fprintf(stderr, "cudaMalloc failed!");
//
//	cudaStatus = cudaMemcpy(t_src, src_img, img_size, cudaMemcpyHostToDevice);
//	if (cudaStatus != cudaSuccess)
//		fprintf(stderr, "cudaMemcpy failed!");
//
//	if (type == grayscale)
//		grayscale_transform<<<grid_size, block_size>>>(gpu_output, t_src, img_size);
//
//	//// Check for any errors launching the kernel
//    cudaStatus = cudaGetLastError();
//    if (cudaStatus != cudaSuccess)
//        fprintf(stderr, "addKernel launch failed: %s\n", cudaGetErrorString(cudaStatus));
//    
//    // cudaDeviceSynchronize waits for the kernel to finish, and returns
//    // any errors encountered during the launch.
//    cudaStatus = cudaDeviceSynchronize();
//    if (cudaStatus != cudaSuccess)
//        fprintf(stderr, "cudaDeviceSynchronize returned error code %d after launching addKernel!\n", cudaStatus);
//
//    //// Copy output vector from GPU buffer to host memory.
//    cudaStatus = cudaMemcpy(dst_img, gpu_output, img_size, cudaMemcpyDeviceToHost);
//    if (cudaStatus != cudaSuccess)
//        fprintf(stderr, "cudaMemcpy failed!");
//
//	//cudaStatus = cudaFree(gpu_output);
//	//if (cudaStatus != cudaSuccess)
//	//	fprintf(stderr, "cudaFree failed!");
//
//	return cudaStatus;
//}

/// HERE IS A WORKING EXAMPLE
//cudaError_t addWithCuda(int *c, const int *a, const int *b, unsigned int size);
//
//__global__ void addKernel(int *c, const int *a, const int *b)
//{
//    int i = threadIdx.x;
//    c[i] = a[i] + b[i];
//}
//
//int main()
//{
//    const int arraySize = 5;
//    const int a[arraySize] = { 1, 2, 3, 4, 5 };
//    const int b[arraySize] = { 10, 20, 30, 40, 50 };
//    int c[arraySize] = { 0 };
//
//    // Add vectors in parallel.
//    cudaError_t cudaStatus = addWithCuda(c, a, b, arraySize);
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "addWithCuda failed!");
//        return 1;
//    }
//
//    printf("{1,2,3,4,5} + {10,20,30,40,50} = {%d,%d,%d,%d,%d}\n",
//        c[0], c[1], c[2], c[3], c[4]);
//
//    // cudaDeviceReset must be called before exiting in order for profiling and
//    // tracing tools such as Nsight and Visual Profiler to show complete traces.
//    cudaStatus = cudaDeviceReset();
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaDeviceReset failed!");
//        return 1;
//    }
//
//    return 0;
//}
//
//// Helper function for using CUDA to add vectors in parallel.
//cudaError_t addWithCuda(int *c, const int *a, const int *b, unsigned int size)
//{
//    int *dev_a = 0;
//    int *dev_b = 0;
//    int *dev_c = 0;
//    cudaError_t cudaStatus;
//
//    // Choose which GPU to run on, change this on a multi-GPU system.
//    cudaStatus = cudaSetDevice(0);
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaSetDevice failed!  Do you have a CUDA-capable GPU installed?");
//        goto Error;
//    }
//
//    // Allocate GPU buffers for three vectors (two input, one output)    .
//    cudaStatus = cudaMalloc((void**)&dev_c, size * sizeof(int));
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaMalloc failed!");
//        goto Error;
//    }
//
//    cudaStatus = cudaMalloc((void**)&dev_a, size * sizeof(int));
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaMalloc failed!");
//        goto Error;
//    }
//
//    cudaStatus = cudaMalloc((void**)&dev_b, size * sizeof(int));
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaMalloc failed!");
//        goto Error;
//    }
//
//    // Copy input vectors from host memory to GPU buffers.
//    cudaStatus = cudaMemcpy(dev_a, a, size * sizeof(int), cudaMemcpyHostToDevice);
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaMemcpy failed!");
//        goto Error;
//    }
//
//    cudaStatus = cudaMemcpy(dev_b, b, size * sizeof(int), cudaMemcpyHostToDevice);
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaMemcpy failed!");
//        goto Error;
//    }
//
//    // Launch a kernel on the GPU with one thread for each element.
//    addKernel<<<1, size>>>(dev_c, dev_a, dev_b);
//
//    // Check for any errors launching the kernel
//    cudaStatus = cudaGetLastError();
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "addKernel launch failed: %s\n", cudaGetErrorString(cudaStatus));
//        goto Error;
//    }
//    
//    // cudaDeviceSynchronize waits for the kernel to finish, and returns
//    // any errors encountered during the launch.
//    cudaStatus = cudaDeviceSynchronize();
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaDeviceSynchronize returned error code %d after launching addKernel!\n", cudaStatus);
//        goto Error;
//    }
//
//    // Copy output vector from GPU buffer to host memory.
//    cudaStatus = cudaMemcpy(c, dev_c, size * sizeof(int), cudaMemcpyDeviceToHost);
//    if (cudaStatus != cudaSuccess) {
//        fprintf(stderr, "cudaMemcpy failed!");
//        goto Error;
//    }
//
//Error:
//    cudaFree(dev_c);
//    cudaFree(dev_a);
//    cudaFree(dev_b);
//    
//    return cudaStatus;
//}
