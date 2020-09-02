#include <stdio.h>
#include <string.h>

int main()
{
    char string[50] = "hello my name is Davis";
    char rev_string[50];

    int i, j;
    int len = strlen(string);

    j = 0;
    for(i=(len-1); i>=0; i--) {
        rev_string[j] = string[i];
        j++;
    }

    printf("Original string: %s\n", string);
    printf("Reversed string: %s\n", rev_string);

    return 0;
}