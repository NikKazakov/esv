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
    char *buf = malloc(100);
    unsigned long *f = malloc(4);
    *f = (unsigned long)prt;
    printf("addr buf: %p\n", buf);
    printf("addr f: %p\n", f);
    strcpy(buf, argv[1]);
    ((void (*)(char *))(*f))(buf);
    free(buf);
    free(f);
    return 0;
}
