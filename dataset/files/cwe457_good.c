#include <stdio.h>

int compute(int x) {
    int result = 0;
    if (x > 0) {
        result = x * 2;
    }
    return result;
}

int main() {
    printf("%d\n", compute(-5));
    return 0;
}
