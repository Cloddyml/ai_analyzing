#include <stdio.h>
#include <string.h>

void copy_n_bytes(char *dst, char *src, int n) {
    memcpy(dst, src, n);
}

int main(void) {
    char dst[16];
    char src[] = "hello";
    int n = -1;
    copy_n_bytes(dst, src, n);
    return 0;
}
