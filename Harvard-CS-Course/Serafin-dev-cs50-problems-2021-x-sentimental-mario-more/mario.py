def pyramid(height):
    counter_3 = 1
    counter_2 = 1 
    counter_1 = height - 1
    
    #Rows
    for i in range(height):
       
        #Print Blank spaces from the left
        counter = 0
        j = counter_1
        while counter < j:
    	    counter += 1
    	    print(" ", end="")

        
        counter_1 = counter_1 - 1

        # print the pyramid from the left
        k = 1
        while k <= counter_2: 
            numeral = '#'
            print (numeral, end="")
            k += 1
        
        counter_2 += 1
        
        # Print double blank space in the middle of the pyramid
        print("  ", end="")
        
        # print the pyramid from the right
        k=1
        while k <= counter_3 :
            numeral = '#'
            print (numeral, end="")
            k += 1
        
        counter_3 += 1
        print("")
    

def main():
    # Get Height integer from the user 
    height = input("Height: ")
    height = int(height)
    while height < 1 or height > 8:
        heigth = input("Height: ")
    
    pyramid(height)
    
main()