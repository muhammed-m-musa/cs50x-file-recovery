
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "recover.h"
#include <sys/stat.h>
#include <stdbool.h>

int check_file_signature(uint8_t *buffer);
typedef struct{

    char *extension;
    uint8_t signature[8];
    int sig_length;

}FileType;

FileType supported_types[] = {{"jpg", {0xff, 0xd8, 0xff, 0xe0},4},
{"png", {0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a}, 8},
{"gif", {0x47, 0x49, 0x46, 0x38, 0x37, 0x61}, 6},
{"zip", {0x50, 0x4b, 0x03, 0x04}, 4}

};

void source_file(char *path, char *recovered_dir)
{
    FILE *source = fopen(path,"rb");

    if(source == NULL)
    {
        printf("this file is not exist\n");
        return;
    }

    uint8_t buffer[512];

    FILE *output = NULL;
    char filename[512];
    int count=0;

    mkdir(recovered_dir, 0700);

    size_t bytes_read;

    while((bytes_read = fread(buffer,1,512,source)) >0)
    {
        int index = check_file_signature(buffer);

        if(index != -1)
        {

            if(output !=NULL)
            {
                fclose(output);
            }

            snprintf(filename,sizeof(filename), "%s/%03i.%s",recovered_dir, count, supported_types[index].extension);

            output = fopen(filename, "wb");

             if (output == NULL)
            {
                printf("cannot create output file");
                break;
            }
            count++;
        }

        if(output != NULL)
        {

            fwrite(buffer,1,bytes_read, output);
        }
    }

    if(output != NULL)
    {
        fclose(output);
    }
    fclose(source);



}


int check_file_signature(uint8_t *buffer)
{

    int num_types =4;

    for(int i=0;i<num_types;i++)
    {
        bool match = true;
        for(int j=0;j<supported_types[i].sig_length; j++)
        {

            if(i==0 && j==3)
            {
                if((buffer[3] & 0xf0) != 0xe0)
                {
                    match = false;
                    break;
                }
            }
            else if(i==2 && j==4)
            {
                if(buffer[4] != 0x37 && buffer[4] != 0x39)
                {
                    match = false;
                    break;
                }
            }

            else
            {
                if(buffer[j] != supported_types[i].signature[j])
                {
                    match = false;
                    break;
                }
            }
        }
        if(match)
        {
            return i;
        }
    }
    return -1;


}
