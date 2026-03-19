#include <stdio.h>
#include <string.h>

void process(char *input) {
    char buffer[16];
    strcpy(buffer, input);
    printf("%s\n", buffer);
}

int main() {
    process("This string is definitely too long!");
    return 0;
}
