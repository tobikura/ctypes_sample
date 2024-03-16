#ifndef __SAMPLE_H__
#define __SAMPLE_H__

#ifdef WIN32
#define DllExport __declspec(dllexport)
#else
#define DllExport
#endif

struct sample_struct
{
    int a;
    int b;
    float c;
    float d;
};

DllExport int add_scaler(int a, int b);
DllExport void copy_int(int *dst, int *src, int len);
DllExport void add_int(int *dst, int *a, int *b, int len);
DllExport void mul_int(int *dst, int *a, int *b, int len);
DllExport int sum_int(int *a, int len);
DllExport void copy_float(float *dst, float *src, int len);
DllExport void add_float(float *dst, float *a, float *b, int len);
DllExport void mul_float(float *dst, float *a, float *b, int len);
DllExport float sum_float(float *a, int len);

DllExport void init_struct(struct sample_struct *s);
DllExport void print_struct(struct sample_struct *s);

#endif
