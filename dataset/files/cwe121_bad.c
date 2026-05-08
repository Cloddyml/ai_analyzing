#include <stdio.h>
#include <string.h>

void copy_to_stack(const char *src) {
    char dest[10];
    strcpy(dest, src);
    printf("%s\n", dest);
}

int main(void) {
    copy_to_stack("AAAAAAAAAAAAAAAAAAAAAAAA");
    return 0;
}
