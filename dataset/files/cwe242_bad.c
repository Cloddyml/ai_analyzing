#include <stdio.h>

void read_input(void) {
    char buffer[64];
    gets(buffer);
    printf("%s\n", buffer);
}

int main(void) {
    read_input();
    return 0;
}
