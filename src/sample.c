#include <stdio.h>
#include "sample.h"

int add_scaler(int a, int b)
{
    return a + b;
}

void copy_int(int *dst, int *src, int len)
{
    int i;

    for (i = 0; i < len; i++)
        dst[i] = src[i];
}

void add_int(int *dst, int *a, int *b, int len)
{
    int i;

    for (i = 0; i < len; i++)
        dst[i] = a[i] + b[i];
}

void mul_int(int *dst, int *a, int *b, int len)
{
    int i;

    for (i = 0; i < len; i++)
        dst[i] = a[i] * b[i];
}

int sum_int(int *a, int len)
{
    int i, acc = 0;

    for (i = 0; i < len; i++)
        acc += a[i];
    return acc;
}

void copy_float(float *dst, float *src, int len)
{
    int i;

    for (i = 0; i < len; i++)
        dst[i] = src[i];
}

void add_float(float *dst, float *a, float *b, int len)
{
    int i;

    for (i = 0; i < len; i++)
        dst[i] = a[i] + b[i];
}

void mul_float(float *dst, float *a, float *b, int len)
{
    int i;

    for (i = 0; i < len; i++)
        dst[i] = a[i] * b[i];
}

float sum_float(float *a, int len)
{
    int i;
    float acc = 0.0f;

    for (i = 0; i < len; i++)
        acc += a[i];
    return acc;
}

void init_struct(struct sample_struct *s)
{
    s->a = 0x12345678;
    s->b = 6;
    s->c = 1.23;
    s->d = 4.56;
}

void print_struct(struct sample_struct *s)
{
    printf("a=0x%08x, b=0x%08x, c=%f, d=%f\n", s->a, s->b, s->c, s->d);
}
