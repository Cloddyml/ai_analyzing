#include <stdio.h>

unsigned int subtract(unsigned int a, unsigned int b) {
    if (b > a) return 0;
    return a - b;
}

int main(void) {
    unsigned int x = 5;
    unsigned int y = 10;
    printf("%u\n", subtract(x, y));
    return 0;
}
