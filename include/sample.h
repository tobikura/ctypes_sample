#ifndef __SAMPLE_H__
#define __SAMPLE_H__

struct sample_struct
{
    int a;
    int b;
    float c;
    float d;
};

int add_scaler(int a, int b);
void copy_int(int *dst, int *src, int len);
void add_int(int *dst, int *a, int *b, int len);
void mul_int(int *dst, int *a, int *b, int len);
int sum_int(int *a, int len);
void copy_float(float *dst, float *src, int len);
void add_float(float *dst, float *a, float *b, int len);
void mul_float(float *dst, float *a, float *b, int len);
float sum_float(float *a, int len);

void init_struct(struct sample_struct *s);
void print_struct(struct sample_struct *s);

#endif
