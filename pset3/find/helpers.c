/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    int l, r, m;
    if(n<0)
        return false;
    else
    {
        l = 0;
        r = n-1;
        while (l <= r)
        {
            m = (l + r)/2;

            if (values[m] == value)
                return true;

            if (values[m] < value)
                l = m + 1;
            else
                r = m - 1;
        }
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    int val[65536];
    int i,k=0;
    for(i = 0; i < 65536; i++)
    {
        val[i] = 0;
    }

    for(i = 0; i < n; i++)
    {
        val[values[i]]++;
    }

    for(i=0;i<=65536;i++)
    {
        if(val[i]==0)
            continue;
        else
        {
            for(int j=0;j<val[i];j++)
            {
                values[k++] = i;
            }
        }
    }

    return;
}
