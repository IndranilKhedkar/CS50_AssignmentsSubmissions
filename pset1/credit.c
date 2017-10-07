#include<stdio.h>
#include<cs50.h>
#include<math.h>

int getDigitSum(int num)
{
    if(num<10)
        return num;
    else
        {
            int sum=0;
            while(num!=0)
            {
                sum=sum+num%10;
                num=num/10;
            }
            return sum;
        }
}

int main(void)
{
    long long cc_number, cc_num;
    long long sum=0, i=1, mod;
    do
    {
        printf("Number: ");
        cc_number= get_long_long();
    }while(cc_number <= 0);
    cc_num = cc_number;
    while(cc_num!=0)
    {
        mod = cc_num%10;
        if(i%2==0)
        {
            sum+= getDigitSum((int)mod*2);
        }
        else
        {
            sum+= mod;
        }
        cc_num=cc_num/10;
        i++;
    }
    if ((sum % 10) == 0)
    {
        int twoDigits = (int)(cc_number / pow(10,(i-3)));
        if ((i - 1) == 15 || twoDigits==34 || twoDigits==37)
            printf("AMEX\n");
        else if (((i - 1) == 13 || (i - 1) == 16) && twoDigits/10 == 4)
            printf("VISA\n");
        else if ((i - 1) == 16 && (twoDigits == 51 || twoDigits == 52 || twoDigits == 53 || twoDigits == 54 || twoDigits == 55))
            printf("MASTERCARD\n");
    }
    else
        printf("INVALID\n");
}
