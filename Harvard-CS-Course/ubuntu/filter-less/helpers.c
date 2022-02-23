#include "helpers.h"
#include "math.h"
#include "stdlib.h"
#include "stdio.h"
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j=0;j<width;j++)
        {
            // Pixel
            RGBTRIPLE p = image[i][j];

            // calculate the average rgb value
            int avg = round((p.rgbtRed + p.rgbtGreen + p.rgbtBlue) / 3.00);

            // modify pixel
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
int adjust(int rgb)
{
    if (rgb > 255)
    {
        rgb = 255;
    }
    return rgb;
}
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j=0;j<width;j++)
        {
            // Pixel
            RGBTRIPLE p = image[i][j];

            // get the values for each color of the pixel
            int sepiaRed = adjust(round(p.rgbtRed * 0.393 + p.rgbtGreen * 0.769 + p.rgbtBlue * 0.189));
            int sepiaGreen = adjust(round(p.rgbtRed * 0.349 + p.rgbtGreen * 0.686 + p.rgbtBlue * 0.168));
            int sepiaBlue = adjust(round(p.rgbtRed * 0.272 + p.rgbtGreen * 0.534 + p.rgbtBlue * 0.131));

            // modify pixel
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;

        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //temp image
    RGBTRIPLE temp[height][width];

        // get every row
        for (int i = 0; i < height; i++)
        {
            // check if there are odd number of pixels in that row
            if (width % 2 != 0)
            {
                // reflect pixels
                for (int j = 0; j < (width - 1) / 2; j++)
                {
                    temp[i][j] = image[i][j];
                    image[i][j] = image[i][width - (j + 1)];
                    image[i][width - (j + 1)] = temp[i][j];
                }
                return;
            }
            // if the number of pixels is % 2 == 0
            for (int j = 0; j < width / 2; j++)
            {
                // reflect pixels
                temp[i][j] = image[i][j];
                image[i][j] = image[i][width - (j + 1)];
                image[i][width - (j + 1)] = temp[i][j];
            }
        }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sumBlue = 0;
            float sumGreen = 0;
            float sumRed = 0;
            float counter = 0;

            for (int r = -1; r < 2; r++)
            {
                for (int c = -1; c < 2; c++)
                {
                    if (i + r < 0 || i + r > height - 1)
                    {
                        continue;
                    }

                    if (j + c < 0 || j + c > width - 1)
                    {
                        continue;
                    }

                    sumBlue += image[i + r][j + c].rgbtBlue;
                    sumGreen += image[i + r][j + c].rgbtGreen;
                    sumRed += image[i + r][j + c].rgbtRed;
                    counter++;
                }
            }

            temp[i][j].rgbtBlue = round(sumBlue / counter);
            temp[i][j].rgbtGreen = round(sumGreen / counter);
            temp[i][j].rgbtRed = round(sumRed / counter);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }

    }

    return;
}
