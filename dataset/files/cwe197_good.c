#include <stdio.h>
#include <limits.h>

char truncate_value(int x) {
    if (x > CHAR_MAX || x < CHAR_MIN) return 0;
    char result = x;
    return result;
}

int main(void) {
    int big = 300;
    printf("%d\n", truncate_value(big));
    return 0;
}
