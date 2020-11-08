//
//  weird programming challenge I found online
//

#include <stdio.h>

int main()
{
    int n = 7;
    int rows = (n*2) - 1;
    int i, j, temp_i, temp_j, temp_n;

    for(i=0; i<rows; i++)
    {
        temp_i = (i >= n) ? (rows - 1 - i) : i;

        for(j=0; j<rows; j++)
        {
            temp_n = n;
            temp_j = (j >= n) ? (rows - 1 - j) : j;

            if(temp_i <= temp_j)
            {
                temp_n -= temp_i;
            }
            else
            {
                temp_n -= temp_j;
            }

            printf("%d ", temp_n);
        }
        
        printf("\n");
    }

    return 0;
}