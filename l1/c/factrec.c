// factrec.c
#include <stdio.h>
#include <stdlib.h>

typedef unsigned long uint64;

uint64 fact(uint64 n)
{
    if (n == 0)
        return 1;
    return fact(n - 1) * n;
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Usage: %s <number>\n", argv[0]);
        return -1;
    }
    uint64 n = atoi(argv[1]);
    if (n < 0) return 1;
    printf("%lu! = %lu\n", n, fact(n));
    return 0;
}
