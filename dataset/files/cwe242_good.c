#include <stdio.h>

void read_input(void) {
    char buffer[64];
    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        printf("%s\n", buffer);
    }
}

int main(void) {
    read_input();
    return 0;
}
