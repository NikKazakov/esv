#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void foo(const char *v)
{
    size_t l = 1;
    char buf[100];
    printf("* &l: %lX, l: %zu\n", &l, l);
    snprintf(buf, sizeof(buf), v);
    printf("^ &l: %lX, l: %zu\n", &l, l);
    printf("buf: %s\n", buf);
}
int main(int argc, char *argv[])
{
    if (argc !=2) exit(1);
    foo(argv[1]);
    return 0;
}
