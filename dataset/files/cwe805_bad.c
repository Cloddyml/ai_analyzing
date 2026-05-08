#include <stdio.h>
#include <string.h>

void copy_data(char *dst, char *src) {
    memcpy(dst, src, sizeof(src));
}

int main(void) {
    char buffer[100];
    char source[] = "long source data here";
    copy_data(buffer, source);
    return 0;
}
