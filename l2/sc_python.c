#include <unistd.h>
int main(int argc, char *argv[])
{
    execve("/usr/bin/python", 0, 0);
    return 0;
}
