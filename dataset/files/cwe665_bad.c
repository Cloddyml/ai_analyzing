#include <stdio.h>

struct Point {
    int x;
    int y;
};

int main(void) {
    struct Point p;
    p.x = 10;
    printf("x=%d y=%d\n", p.x, p.y);
    return 0;
}
