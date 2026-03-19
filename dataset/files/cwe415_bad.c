#include <stdio.h>
#include <stdlib.h>

void cleanup(int *p) {
    free(p);
}

int main() {
    int *ptr = (int *)malloc(sizeof(int));
    *ptr = 10;
    cleanup(ptr);
    free(ptr);
    return 0;
}
