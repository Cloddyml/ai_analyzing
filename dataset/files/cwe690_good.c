#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *data = (int *)malloc(100 * sizeof(int));
    if (data == NULL) return 1;
    data[0] = 42;
    printf("%d\n", data[0]);
    free(data);
    return 0;
}
