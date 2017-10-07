/**
 * Copies a BMP piece by piece, just because.
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>
typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    BYTE buffer[512];
    //buffer = malloc(sizeof(BYTE)*512);
    // open input file
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    char filename[10];
    bool flag = false;
    int i=0;
    FILE *img = NULL;
    while(fread(buffer,512, 1, inptr) == 1)
    {
        if(buffer[0] == 0xff &&
        buffer[1] == 0xd8 &&
        buffer[2] == 0xff &&
        (buffer[3] & 0xf0) == 0xe0)
        {
            flag=true;
            if(img != NULL)
                fclose(img);

            sprintf(filename,"%03i.jpg",i);
            img = fopen(filename,"a");
            fwrite((char*)&buffer, 512, 1, img);
            i++;
        }
        else
        {
            if(flag)
                fwrite(&buffer, 512, 1, img);
        }
    }
    fclose(img);
}