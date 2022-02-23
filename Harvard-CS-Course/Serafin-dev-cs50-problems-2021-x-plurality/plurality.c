#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for (int i = 0 ; i < candidate_count ; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes ++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    int swapCounter = -1;
    string winner;
    int winnerVotes;
    int unsortedArrayLen = candidate_count -1;
    //bubble sort the candidate's array
    while (swapCounter != 0)
    {
        swapCounter = 0;

        //go through all the pairs and compare them.
        for (int i = 0 ; i < unsortedArrayLen ; i++)
        {
            candidate actualCandidate = candidates[i];
            candidate nextCandidate = candidates[i + 1];

            //swap
            if (actualCandidate.votes > nextCandidate.votes)
            {
                candidates[i] = nextCandidate;
                candidates[i + 1] = actualCandidate;
                swapCounter += 1 ;
            }
        }

        unsortedArrayLen -= 1;
    }
    int arraylen = candidate_count-1;
    winner = candidates[arraylen].name;
    winnerVotes = candidates[arraylen].votes;
    //print winner
    printf("%s\n", winner);

    //print all the candidates that have as many votes as the winner.
    for (int i = arraylen ; i >= 0 ; i--)
    {
        int otherCandidateVotes = candidates[i - 1].votes;
        string otherCandidateName = candidates[i - 1].name;

        if (otherCandidateVotes == winnerVotes)
        {
            winner = otherCandidateName;
            printf("%s\n", winner);
        }
    }


    // TODO
    return;


}

