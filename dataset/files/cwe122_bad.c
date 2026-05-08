#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char *buffer = (char *)malloc(8);
    if (!buffer) return 1;
    strcpy(buffer, "AAAAAAAAAAAAAAAAAAAA");
    printf("%s\n", buffer);
    free(buffer);
    return 0;
}
