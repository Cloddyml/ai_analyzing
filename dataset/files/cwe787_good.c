#include <stdio.h>
#include <string.h>

void process(char *input) {
    char buffer[16];
    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    printf("%s\n", buffer);
}

int main() {
    process("Short string");
    return 0;
}
