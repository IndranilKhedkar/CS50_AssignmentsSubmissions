#include <crypt.h>
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#define UPPERCASEALPHSTARTACSII 65
#define LOWERCASEALPHSTARTACSII 97
#define TOTOALNUMBEROFALPHABETS 26

int main(int argc, string argv[])
{
    if(argc != 1)
    {
        printf("plaintext: ");
        string input = get_string();
        string k = argv[1];
        int n = atoi(k);
        if(input != NULL)
        {
            printf("ciphertext: ");
            for(int i=0;i<strlen(input); i++)
            {
                if(input[i] >= 'a' && input[i] <= 'z')
                {
                    printf("%c", LOWERCASEALPHSTARTACSII + ((input[i] -LOWERCASEALPHSTARTACSII) + n)%TOTOALNUMBEROFALPHABETS);
                }
                else if(input[i] >= 'A' && input[i] <= 'Z')
                {
                    printf("%c", UPPERCASEALPHSTARTACSII + ((input[i]-UPPERCASEALPHSTARTACSII) + n)%TOTOALNUMBEROFALPHABETS);
                }
                else
                {
                    printf("%c",  input[i]);
                }
            }
            printf("\n");
        }
        return 0;
    }
    printf("Incorrect number of arguments");
    return 1;
}