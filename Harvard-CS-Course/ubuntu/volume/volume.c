// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file

    // Ask for memory to point the header
    uint8_t *header = malloc(sizeof(uint8_t) * HEADER_SIZE);
    if (header != NULL)
    {
        // Store the first 44 bytes of the input file to a pointer in the heap
        fread(header, sizeof(uint8_t), HEADER_SIZE, input);

        // Write the header out to the output file
        fwrite(header, sizeof(uint8_t), HEADER_SIZE, output);
        free(header);
    }

    // TODO: Read samples from input file and write updated data to output file
    int sample_size = sizeof(int16_t);
    int16_t *sample = malloc(sample_size);
    if (sample != NULL)
    {
        while (fread(sample, sample_size, 1, input))
        {
            //multiply by factor
            *sample *= factor;
            //write to the output file
            fwrite(sample, sample_size, 1, output);
        }
        free(sample);
    }
    // Close files
    fclose(input);
    fclose(output);
}
