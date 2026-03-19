#include <stdio.h>
#include <limits.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(INT_MAX, 1);
    printf("%d\n", result);
    return 0;
}
