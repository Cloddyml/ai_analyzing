#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char *str = (char *)malloc(20);
    if (!str) return 1;
    strcpy(str, "hello world");
    char *part = str + 6;
    printf("%s\n", part);
    free(str);
    return 0;
}
