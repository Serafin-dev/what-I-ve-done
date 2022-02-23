#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

double coleman_index();
int main(void)
{   
    //get text from user
    string text = get_string("Text:");
    
    //calculate Coleman-Liau readability index grade 
    int index = coleman_index(text);
    
    //round index to closest integer
    //int index = round(index);
    
    //print something for each condition
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

//Coleman-Liau index function
double coleman_index(string text)
{
    char alphabet[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
    int txt_len = strlen(text);
    int letters_amount = 0;
    int words_amount = 1;
    int sentences_amount = 0;
    for (int i = 0; i < txt_len ; i++)
    {   
        //Amount of letters
        char text_digit = text[i];
        char text_digit_upper = toupper(text_digit);
        char text_digit_lower = tolower(text_digit);
        
        for (int j = 0; j < 26 ; j++) 
        {   
            char alphabet_char = alphabet [j];
      
            if (text_digit_upper == alphabet_char || text_digit_lower == alphabet_char)
            {
                letters_amount++;
                
            }
        }
        //Amount of words and sentences 
        char space_btw_words = ' ';
        if (text_digit == space_btw_words)
        {
            words_amount++;
        }
        else if (text_digit == '!' || text_digit == '.' || text_digit == '?')
        {
            sentences_amount++;
        }
        
    }

    //calculate average letters in 100 words
    float L = letters_amount * 100 / words_amount;
    //calculate average sentences in 100 words
    float S = sentences_amount * 100 / words_amount;
    //calculate index
    int index = round((0.0588 * L) - (0.296 * S) - 15.8);
    return index;
}