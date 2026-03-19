#include <stdio.h>
#include <stdlib.h>

void process_data(int n) {
    int *data = (int *)malloc(n * sizeof(int));
    if (!data) return;
    for (int i = 0; i < n; i++) {
        data[i] = i * 2;
    }
    printf("processed\n");
    /* free(data) забыли */
}

int main() {
    process_data(100);
    return 0;
}
