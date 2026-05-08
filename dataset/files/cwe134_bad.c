#include <stdio.h>

void log_message(const char *msg) {
    printf(msg);
}

int main(void) {
    log_message("Hello %x %x\n");
    return 0;
}
