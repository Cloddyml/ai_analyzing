#include <stdio.h>
#include <string.h>

void copy_data(char *dst, char *src, size_t n) {
    memcpy(dst, src, n);
}

int main(void) {
    char buffer[100];
    char source[] = "long source data here";
    copy_data(buffer, source, strlen(source) + 1);
    return 0;
}
