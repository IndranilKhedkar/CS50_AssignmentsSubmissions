import cs50

def getDigitSum(num):
    if num < 10:
        return num;
    else:
        sum = 0
        while num != 0:
            sum = sum + num % 10;
            num = num / 10;
        return sum

def main():
    sum=0
    i=1
    while True:
        print("Number: ",end="")
        cc_number = cs50.get_int()
        if cc_number > 0:
            break

    cc_num = cc_number;

    while cc_num != 0:
        mod = cc_num%10
        if i%2 == 0:
            sum = sum + getDigitSum(mod*2)
        else:
            sum+= mod
        cc_num=cc_num/10
        i = i+1

    if (sum % 10) == 0:
        twoDigits = (cc_number / pow(10,(i-3)))
        if ((i - 1) == 15 or twoDigits==34 or twoDigits==37):
            print("AMEX");
        elif (((i - 1) == 13 or (i - 1) == 16) and twoDigits/10 == 4):
            print("VISA")
        elif ((i - 1) == 16 and (twoDigits == 51 or twoDigits == 52 or twoDigits == 53 or twoDigits == 54 or twoDigits == 55)):
            print("MASTERCARD")
    else:
        print("INVALID")

if __name__ == "__main__":
    main()