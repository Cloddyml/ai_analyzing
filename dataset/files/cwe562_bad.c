#include <stdio.h>

int *get_value(void) {
    int local = 42;
    return &local;
}

int main(void) {
    int *p = get_value();
    printf("%d\n", *p);
    return 0;
}
