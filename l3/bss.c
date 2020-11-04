#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void prt(char *v)
{
    printf("v: %s\n", v);
}

int main(int argc, char *argv[])
{
    if (argc != 2) exit(1);
    static char buf[100];
    static void (*f)(char *);
    printf("addr buf: %p\n", buf);
    printf("addr &f : %p\n", &f);
    f = prt;
    strcpy(buf, argv[1]);
    f(buf);
    return 0;
}
