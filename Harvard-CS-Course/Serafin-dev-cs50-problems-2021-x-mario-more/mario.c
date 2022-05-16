#include <stdio.h>
#include <cs50.h>

//personalized function that creates the pyramids
void pyramid(int height)
{   
    
    int counter_3 = 1;
    int counter_2 = 1; 
    int counter_1 = height-1;
    
    //Rows
    for (int i = 0; i<height; i++)
    {   

        //Print Blank spaces from the left
        int j=counter_1;
        int counter = 0;
        while (counter < j)
        {
            char blank =' ';
    	    printf ("%c", blank);
    	    counter++;
        }
        counter_1 = counter_1 - 1;

        //print the pyramid from the left

        for (int k=1; k<=counter_2 ; k++)
        {   
            char numeral = '#';
            printf ("%c", numeral);
        }

        counter_2++;
        //Print double blank space in the middle of the pyramid
        printf("  ");

        //print the pyramid from the right
        for (int k=1; k<=counter_3 ; k++)
        {   
            char numeral = '#';
            printf ("%c", numeral);
        }

        counter_3++;

        printf("\n");
    }
}

int main (void)
{   
   //Get Height integer from the user    
   int height;
   do
   {
        height = get_int("Height: ");
   }
   while (height < 1 || height > 8);

   pyramid(height);
}
