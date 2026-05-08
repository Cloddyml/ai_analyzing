#include <stdio.h>

void log_message(const char *msg) {
    printf("%s", msg);
}

int main(void) {
    log_message("Hello world\n");
    return 0;
}
