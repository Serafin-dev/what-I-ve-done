#include <stdio.h>
#include <cs50.h>

int main(void)
{
  // TODO: Prompt for start size
 int starting_population;
 do
 {
      starting_population = get_int("Starting population integer: ");
 }
 while (starting_population <9);
  // TODO: Prompt for end size  

 int ending_population;
 do
 {
      ending_population = get_int("Ending population Integer: ");
 }
 while (ending_population < starting_population);
     
 
  //TODO: Calculate number of years until we reach threshold
 

 int actual_year=0;


 //TODO: Calculate number of years until we reach threshold
 for (int actual_population=starting_population;actual_population < ending_population; actual_year++)
 {
     int borned = (actual_population / 3);
     int died = (actual_population /4);
     actual_population = actual_population + borned - died;
 }
  // TODO: Print number of years
 printf("Years: %i\n", actual_year); 
}




    // TODO: Prompt for end size

    // TODO: Calculate number of years until we reach threshold

    // TODO: Print number of years
