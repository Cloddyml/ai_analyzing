#include <stdio.h>
#include <stdlib.h>

void cleanup(int **p) {
    if (*p) {
        free(*p);
        *p = NULL;
    }
}

int main() {
    int *ptr = (int *)malloc(sizeof(int));
    *ptr = 10;
    cleanup(&ptr);
    return 0;
}
