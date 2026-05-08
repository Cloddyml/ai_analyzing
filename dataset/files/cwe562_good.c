#include <stdio.h>
#include <stdlib.h>

int *get_value(void) {
    int *p = (int *)malloc(sizeof(int));
    if (p) *p = 42;
    return p;
}

int main(void) {
    int *p = get_value();
    if (p) {
        printf("%d\n", *p);
        free(p);
    }
    return 0;
}
