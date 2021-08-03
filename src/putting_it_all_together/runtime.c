#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int *init_record(int size){
  int i;
  int *p, *a;
  p = a = (int *)malloc(size);
  for(i=0;i<size;i+=sizeof(int)) *p++ = 0;
  return a;
}

int char_to_num(char* str){
    if ( strlen(str) ) return (int)str[0];
    return -1;
}

void exit_program(int status){
  exit(status);
}

void flush(){
 fflush(stdout);
}

int *init_array(int size, int init){
  int i;
  int *a = (int *)malloc(size*sizeof(int));
  for(i=0;i<size;i++) a[i]=init;
  return a;
}

int not(int n){
  return n==0;
}

char* num_to_char(long long n){
  if ( n < 0 || n >= 256 ) {
    printf("Out of range char! Arguments: %d\n", n);
    exit(1);
  }

  char *result = (char*) malloc(sizeof(char) * 2);
  result[0] = (char)n;
  result[1] = '\0';
  return result;
}

void print_char(char c){
  printf("%c", c);
}

void print_num(long long n){
  printf("%lld\n", n);
}

void print_string(char *str){
  printf("%s", str);
}

char* read_char(){
  char *c = (char*) malloc(sizeof(char) * 2);
  int result = getchar();
  // Check EOF.
  if(result < 0)
    result = 0;
  c[0] = result;
  c[1] = '\0';
  return c;
}

int read_num(){
  long long n;
  scanf("%lld", &n);
  return n;
}

int string_compare(char *str1, char *str2){
  return strcmp(str1, str2);
}

char* string_concat(char *first, char *second){
  // Reserve space for both strings + '\0'.
  int combined_length = strlen(first) + strlen(second) + 1;
  char *result = (char*) malloc(combined_length * sizeof(char));
  result[0] = '\0';
  strcat(result, first);
  strcat(result, second);
  return result;
}

int string_equal(char *str1, char *str2){
  return strcmp(str1, str2) == 0;
}

int string_length(char *str){
  return strlen(str);
}

char* string_substring(char *source, int start, int length){
  if(start < 0  || start + length > strlen(source)){
    printf("Out of range substring! Arguments: \"%s\" %d %d \n", str, start, length);
    exit(1);
  }

  // Reserve space for the substring + '\0'.
  char result = (char*) malloc(sizeof(char) * (length + 1));
  strncpy(result, source + start, length);
  result[n] = '\0';
  return result;
}

int tigermain(int);
int main(){
  printf("\n");
  return tigermain(0 /*static link*/);
}