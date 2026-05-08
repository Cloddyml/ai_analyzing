#include <stdio.h>

int main(void) {
    FILE *f;
    char buffer[64];
    fread(buffer, 1, sizeof(buffer), f);
    return 0;
}
