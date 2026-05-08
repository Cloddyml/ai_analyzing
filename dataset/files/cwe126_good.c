#include <stdio.h>
#include <string.h>

int main(void) {
    char buffer[6] = {'a', 'b', 'c', 'd', 'e', '\0'};
    size_t len = strlen(buffer);
    printf("%zu\n", len);
    return 0;
}
