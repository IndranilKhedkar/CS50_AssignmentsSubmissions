#include <stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>
int main(void)
{
    string username = get_string();
    bool flag = true;
    if(username != NULL)
    {
        for(int i=0;i<strlen(username); i++)
        {
            if((char)username[i] == ' ')
            {
                flag = true;
                continue;
            }

            if(flag)
            {
                printf("%c",toupper(username[i]));
                flag = false;
            }
        }
        printf("\n");
    }
}