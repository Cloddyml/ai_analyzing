#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *duplicate(const char *s) {
    char *copy = (char *)malloc(strlen(s));
    strcpy(copy, s);
    return copy;
}

int main(void) {
    char *d = duplicate("hello");
    printf("%s\n", d);
    free(d);
    return 0;
}
