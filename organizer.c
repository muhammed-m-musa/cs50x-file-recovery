#include <stdint.h>
#include "recover.h"
#include <sys/stat.h>
#include <stdbool.h>
#include <string.h>
#include <dirent.h>

int organize_files(char *source_dir, char *session_dir, char *user_id);
int move_file(char *source_dir, char *main_folder, char *filename, FILE *csv_report);
int get_folder_name(char *filename, char *ext_dest);


int move_file(char *source_dir, char *main_folder, char *filename, FILE *csv_report)
{
    char old_path[512];
    char new_path[512];
    char sub_folder[256];
    char ext[32];

    // استخراج الامتداد لتحديد المجلد الفرعي
    get_folder_name(filename, ext);

    // بناء مسار المجلد الفرعي (مثل: sorted_files/jpg)
    snprintf(sub_folder, sizeof(sub_folder), "%s/%s", main_folder, ext);

    // إنشاء المجلد الفرعي تلقائياً (On-the-fly) إذا لم يكن موجوداً
    mkdir(sub_folder, 0700);

    // 3. بناء المسار القديم والمسار الجديد للملف كما خططت في دفترك
    snprintf(old_path, sizeof(old_path), "%s/%s", source_dir, filename);
    snprintf(new_path, sizeof(new_path), "%s/%s", sub_folder, filename);

    struct stat file_info;
    if(stat(old_path, &file_info) ==0)
    {
        if(csv_report != NULL)
        {
            fprintf(csv_report, "%s,%ld\n", filename, (long)file_info.st_size);
        }
    }

    if (rename(old_path, new_path) != 0)
    {
        return -1;
    }

    return 0;

}

int organize_files(char *source_dir, char *session_dir, char *user_id)
{
    DIR *dir = opendir(source_dir);
    if (dir == NULL)
    {
        printf("Error: Cannot open source directory.\n");
        return -1;
    }
    //
    char main_destination_folder[512];
    snprintf(main_destination_folder, sizeof(main_destination_folder), "%s/sorted_files",session_dir);
    mkdir(main_destination_folder, 0700);

    char csv_filename[512];
    snprintf(csv_filename, sizeof(csv_filename), "%s/user_%s_report.csv",session_dir, user_id);

    FILE *csv = fopen(csv_filename, "w");
    if(csv!= NULL)
    {
        fprintf(csv, "Filename,Size_Bytes\n");

    }

    struct dirent *entry;

    while((entry = readdir(dir)) != NULL)
    {

        if(entry->d_name[0]=='.')
        {
            continue;
        }

        move_file(source_dir, main_destination_folder, entry->d_name, csv);

    }

    if(csv!= NULL)
    {
        fclose(csv);
    }
    closedir(dir);
    return 0;
}


int get_folder_name(char *filename, char *ext_dest)
{
    int len = strlen(filename);
    int index = -1;

    for(int i=len -1; i>=0;i--)
    {
        if(filename[i] == '.')
        {
            index = i;
            break;
        }
    }

    // إذا لم توجد نقطة (-1) أو كانت النقطة في البداية تماماً كملفات النظام (0)
    if (index == -1 || index == 0)
    {
        strcpy(ext_dest, "no_ext"); // توجيهها لمجلد آمن بدلاً من تركها فارغة
        return 0;
    }

    int  j=0;

    for(int i= index +1; i<len;i++)
    {
        ext_dest[j] = filename[i];
        j++;
    }

    ext_dest[j] = '\0'; // إغلاق الـ String بشكل صحيح

    return 0;


}
