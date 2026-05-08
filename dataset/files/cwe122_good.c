#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char *buffer = (char *)malloc(32);
    if (!buffer) return 1;
    strncpy(buffer, "AAAAAAAAAAAAAAAAAAAA", 31);
    buffer[31] = '\0';
    printf("%s\n", buffer);
    free(buffer);
    return 0;
}
