#include <stdio.h>

void format_message(int id, const char *name) {
    char buffer[16];
    snprintf(buffer, sizeof(buffer), "id=%d name=%s", id, name);
    printf("%s\n", buffer);
}

int main(void) {
    format_message(100, "a_very_long_user_name");
    return 0;
}
