#include <stdio.h>
#include <string.h>

int main(void) {
    char buffer[5] = {'a', 'b', 'c', 'd', 'e'};
    size_t len = strlen(buffer);
    printf("%zu\n", len);
    return 0;
}
