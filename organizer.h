#ifndef ORGANIZER_H
#define ORGANIZER_H

// إعلانات الدوال الثلاث بناءً على خطتك
int organize_files(char *source_dir, char *session_dir, char *user_id);
int get_folder_name(char *filename, char *ext_dest);
int move_file(char *source_dir, char *main_folder, char *filename, FILE *csv_report);

#endif
