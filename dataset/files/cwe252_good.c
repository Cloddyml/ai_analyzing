#include <stdio.h>

int main(void) {
    FILE *f = fopen("data.txt", "r");
    if (f == NULL) return 1;
    char buffer[64];
    fread(buffer, 1, sizeof(buffer), f);
    fclose(f);
    return 0;
}
