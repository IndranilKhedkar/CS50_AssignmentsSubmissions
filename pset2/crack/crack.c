#include <crypt.h>
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>

#define _GNU_SOURCE

int main(int argc, string argv[]){
    //checks if k was passed in
    if (argc != 2) {
        printf("Usage: ./crack hash\n");
        return 1;
    }

    string hash = argv[1];
    char* salt = "50";

    char begin = ' ';
    char end = '~';

    printf("Trying");

    for (char first = begin; first <= end; first++) {
        char compare[5];
        compare[0] = first;
        compare[1] = '\0';

        printf(".");

        if (!strcmp(crypt(compare, salt), hash)) {
            printf("\nPassword found: %s\n", compare);
            return 0;
        }
        for (char second = begin; second <= end; second++) {
            compare[0] = first;
            compare[1] = second;
            compare[2] = '\0';

            if (!strcmp(crypt(compare, salt), hash)) {
                printf("\nPassword found: %s\n", compare);
                return 0;
            }
            for (char third = begin; third <= end; third++) {
                compare[0] = first;
                compare[1] = second;
                compare[3] = third;
                compare[4] = '\0';

                if (!strcmp(crypt(compare, salt), hash)) {
                    printf("\nPassword found: %s\n", compare);
                    return 0;
                }
                for (char fourth = begin; fourth <= end; fourth++) {
                    compare[0] = first;
                    compare[1] = second;
                    compare[2] = third;
                    compare[3] = fourth;
                    compare[0] = first;

                    if (!strcmp(crypt(compare, salt), hash)) {
                        printf("\nPassword found: %s\n", compare);
                        return 0;
                    }
                }
            }
        }
    }
    printf("\nPassword not found!\n");
    return 1;
}