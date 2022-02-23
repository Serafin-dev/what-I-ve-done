#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{   
    
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");
    
    
    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);
    // TODO: Print the winner
    if (score1 > score2)
    {   
        printf("Player 1 wins!");
    }
    else if ( score1 == score2 )
    {   
        printf("Tie!");
    }
    else
    { 
        printf("Player 2 wins!");
    }

}

int compute_score(string word)
{   
    //letters of the alphabet
    char alphabet[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
    int score;
    int previous_score = 0;
    for (int j = 0; j < 26 ; j++)
    {   
        //get the actual letter from the alphabet, and the value of each letter.
        char alphabet_char = alphabet [j];
        int letter_value;
        //Get each letter value and then add them. Store the result in a variable called score
        char word_char;
        int word_len = strlen(word);
        for (int i = 0; i < word_len; i++)
        {   
            word_char = word [i];
            char word_char_upper = toupper(word_char);
            char word_char_lower = tolower(word_char);
            
            if (alphabet_char == word_char_upper || alphabet_char == word_char_lower)
            {
                letter_value = POINTS[j];
                score = previous_score + letter_value;
                previous_score = score;
            }
        }
    }
    //return the result
    return score;
}
