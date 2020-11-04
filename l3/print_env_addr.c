#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    printf("addr %s: %p\n", argv[1], getenv(argv[1]));
    printf("%s = %s\n", argv[1], getenv(argv[1]));
}
