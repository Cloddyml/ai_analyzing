#include <stdio.h>
#include <string.h>

void copy_string(char *dst, const char *src) {
    char buffer[8];
    strncpy(buffer, src, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    printf("%s\n", buffer);
}

int main(void) {
    char dst[8];
    copy_string(dst, "long string here");
    return 0;
}
