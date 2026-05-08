#include <stdio.h>

char truncate_value(int x) {
    char result = x;
    return result;
}

int main(void) {
    int big = 300;
    printf("%d\n", truncate_value(big));
    return 0;
}
