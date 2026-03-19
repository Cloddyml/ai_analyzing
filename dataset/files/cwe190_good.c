#include <stdio.h>
#include <limits.h>

int safe_add(int a, int b, int *result) {
    if (b > 0 && a > INT_MAX - b) return -1;
    if (b < 0 && a < INT_MIN - b) return -1;
    *result = a + b;
    return 0;
}

int main() {
    int result;
    if (safe_add(1000, 2000, &result) == 0) {
        printf("%d\n", result);
    }
    return 0;
}
