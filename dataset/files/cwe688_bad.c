#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int x = 42;
    int *p = &x;
    free(p);
    return 0;
}
