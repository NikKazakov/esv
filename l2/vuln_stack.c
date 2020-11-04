#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void foo(const char *v)
{
    char buf[100];
    printf("addr buf: %p\n", buf);
    printf("addr &v : %p\n", &v);
    strcpy(buf, v);
    printf("buf: %s\n", buf);
}

int main(int argc, char *argv[])
{
    if (argc != 2) exit(1);
    foo(argv[1]);
    printf("returned to main, exiting...");
    return 0;
}
