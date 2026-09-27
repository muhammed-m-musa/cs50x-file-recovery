#ifndef RECOVER_H
#define RECOVER_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

void source_file(char *path, char *recovered_dir);
int check_file_signature(uint8_t *buffer);

#endif
