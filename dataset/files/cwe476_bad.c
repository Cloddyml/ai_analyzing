#include <stdio.h>
#include <stdlib.h>

int get_value(int *ptr) {
    return *ptr;
}

int main() {
    int *p = NULL;
    printf("%d\n", get_value(p));
    return 0;
}
