
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "recover.h"
#include <sys/stat.h>
#include <stdbool.h>
#include "organizer.h"

int main(int argc, char *argv[])
{
    if (argc != 5)
    {
        printf("Usage: ../project raw_file recovered_dir sorted_dir csv_report_path\n");
        return 1;
    }
    source_file(argv[1], argv[2]);

    if (organize_files(argv[2], argv[3], argv[4]) == 0)
    {
        printf("تم تنظيم الملفات بنجاح!\n");
    }
    else
    {
        printf("حدث خطأ أثناء تنظيم الملفات.\n");
    }
    return 0;
}
