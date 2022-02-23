#include <stdio.h>
#include <cs50.h>

int checksum();

int main(void)
{

    // Ask for input
    long card_number = get_long("Number: ");
    //cheksum
    int check = checksum(card_number);
    //Count the amount of digits
    int digits_amount;
    long i = card_number;
    for (digits_amount = 0; i > 0 ; digits_amount++)
    {
        i = i / 10;
    }

    //Get the first_digit and the first_two_digits of the card_number
    long first_digit;
    long first_two_digits;
    long second_digit = card_number % 10;
    for (long j = card_number; j > 0; j = j / 10)
    {
        first_digit = j % 10;
        first_two_digits = first_digit * 10 + second_digit;
        second_digit = first_digit;
    }
    
    //print VISA
    if ((digits_amount == 13 && first_digit == 4 && check == 1) || (digits_amount == 16 && first_digit == 4 && check == 1))
    {
        printf("VISA\n");
    }
    //print MASTERCARD
    else if ((digits_amount == 16 && first_two_digits == 51 && check == 1) || (digits_amount == 16 && first_two_digits == 52 && check == 1) || (digits_amount == 16 && first_two_digits == 53 && check == 1) || (digits_amount == 16 && first_two_digits == 54 && check == 1) || (digits_amount == 16 && first_two_digits == 55 && check == 1))
    {
        printf("MASTERCARD\n");
    }

    //print AMERICAN EXPRESS
    else if ((digits_amount == 15 && first_two_digits == 34 && check == 1)||(digits_amount == 15 && first_two_digits == 37 && check == 1))
    {
        printf("AMEX\n");
    }

    //Print INVALID
    else
    {
        printf("INVALID\n");
    }

}

int checksum(long card_number)
{

    long new_card_number = 1;
    long new_card_number2 = card_number * 10;
    long before_digit = 0;
    long summed_products;
    for (long counter = 10 ; new_card_number > 0 ; counter = counter * 100)
    {
        new_card_number2 = (card_number * 10) / counter;
        new_card_number = card_number / counter;
        long every_other_digit = new_card_number % 10;
        long every_other_digit2 = new_card_number2 % 10;
        long multiplied_digit = every_other_digit * 2;
        long product_digit_1;
        long product_digit_2;


        if (multiplied_digit  != 0 && multiplied_digit >= 10)
        {
            product_digit_1 = 1;
            product_digit_2 = multiplied_digit - 10;
            multiplied_digit = product_digit_1 + product_digit_2;
        }
        summed_products = multiplied_digit + before_digit + every_other_digit2;
        before_digit = summed_products;
    }

    if ((summed_products % 10) == 0)
    {
        return 1;
    }

    else
    {
        return 0;
    }
}

//378282246310005