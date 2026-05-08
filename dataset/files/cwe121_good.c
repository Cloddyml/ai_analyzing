#include <stdio.h>
#include <string.h>

void copy_to_stack(const char *src) {
    char dest[10];
    strncpy(dest, src, sizeof(dest) - 1);
    dest[sizeof(dest) - 1] = '\0';
    printf("%s\n", dest);
}

int main(void) {
    copy_to_stack("short");
    return 0;
}
