#include <stdio.h>

int divide(int a, int b) {
    if (b == 0) return 0;
    return a / b;
}

int main(void) {
    int x = 10;
    int y = 0;
    printf("%d\n", divide(x, y));
    return 0;
}
