import time, datetime
import sys

show_possible = False

if(len(sys.argv)<=3):
    sys.exit("INVALID ARGUMENTS "+str(sys.argv))
        #At minimum we require 4 arguments: 'score_finder.py', SCORE, X_COUNT, and SHOTS
else:
    if(len(sys.argv)>4):
        #Optional fifth argument shows permutations containing missed shots
        if str(sys.argv[4]).lower()=="y" or str(sys.argv[4]).lower()=="t" or str(sys.argv[4])=="1":
            show_possible= True

#Constants to help with code coherence
X_SCORE = 0
TEN_SCORE = 1
NINE_SCORE = 2
ONE_SCORE = 10
ZERO_SCORE = 11


def find_score(distri):
    '''
    Calculates a score of a given distribution
    In our distributions, each column/element is weighted differently. Two
    elements are worth 10 points each, and all others descend. Some simple
    math can create scalars that make this weighting.
    '''

    score = 0
    score += distri[X_SCORE]*10
        #X-Count is also worth 10
    for n in range(TEN_SCORE,ZERO_SCORE):
        score +=distri[n]*(11-n)
        '''
        A distribution which each element is indexed (numbered) from
        left-to-right as the value decreases left-to-right would be:

        this_element_scalar = (maximum_scalar - this_element_index)
        element = this_element_value * this_element_scalar

        However our distribution includes 11 elements and has a maximum
        scalar of 10. This would mean the scalars to equate to:

        first_scalar = (10 - 0) # => 10 (Correct)
        second_scalar = (10 - 1) # => 9 (Incorrect)
        ...
        last_scalar = (10 - 11) # => -1 (Incorrect)

        Only the first scalar is correct.
        The error here is that we have two elements with a scalar of 10. (X and 10 ring)
        If we complete the formula as if there were a maximum scalar of 11 and
        skip the first element, the scalars align:

        ignored_first_scalar = (11 - 0) # ignored
        second_scalar = (11 - 1) # => 10 (Correct)
        third_scalar = (11 - 1) # => 9 (Correct)
        ...
        last_scalar = (11 - 11) # => 0 (Correct)
        '''
    return score

def backtick(s):
    #Prints time to the screen, only occupying bottom line. Proves code is still running.
    print str(datetime.datetime.now().time())+"-: "+ s,
    sys.stdout.flush()
    print "\r",

bad_distris=[]
    #Distributions with missed shots.

def find_distri(score, x, shot_count, show_possible):
    '''
    Main Function. Increments permutations left to right.

    With each distribution represented as an 11-element list/array,
    (One element/column per ring and centre X) we will literate through
    distributions just like how you would count the decimal number 0 to 200:
    Each 'digit' has a value. As you exaust one of these digits, you reset it
    to 0 and increase its neighbour. (9 increases to 10)

    As a competitor has the centre of the target as goal, they would hit
    the bullsye or 'X' exponentially more likely than the outer rings.
    With our distributions organised with the 'X' as the first element in our
    list, it makes more sense to iterate or 'count up' through our distributions
    from centre to the outer rings. Given a score, this also would present
    results more likely of an experienced competitor first. For inexperienced
    competitors, the assumption of perfection is observed as boost to morale.
    This works around the fact that inaccurate scores would take longer to
    find as we iterate.
    (Thankfully, I have data from a Grand Master PPC shooter to test from.)

    We will iterate from [X,0,0,0,0,0,0,0,0,0,0,0] to
    [X,MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX,0] where MAX is the number of
    shots on target minus the 'X'-count. The last element is the
    number of missed shots and will not be iterated through. Our logic satisfies
    distributions with missed shots early on. If we did iterate through the
    missed shots, our code would take somewhere around
    (SHOT_COUNT - X_COUNT) times as long to find.
    '''
    random_pass = 0
        #Number of failed distributions since last successful: supplementary, resets every 1Mil
    fcarry_count = 0
        #Number of branches of permutations we skipped: supplementary, intriguing statistic, never resets
    biggest_score = 0
        #Largest score found in a permutation: supplementary, interesting statistic
    biggest_sum = 0
        #Largest number of shots found in a permutation, before a branch skip: supplementary, interesting statistic

    distri = [0,0,0,0,0,0,0,0,0,0,0,0]
        #Present list/distribution/permutation. 11 elements: X,10-1, and 'miss'/zero
    distri[X_SCORE] = x
        #Set distribution with provided input. Will never change past this point.
    possible = shot_count-x
        #If we know n shots were X_SCORE, that leaves n-X possible other shots.
    print "There is a possible "+str(possible)+" shots left."


    overflow_column = 0
        #Last column where we had a carry.
    while distri[ZERO_SCORE]<=0:
        #We will stop once the Zero element of the distribution increases. Logic for distributions with missed shots are nested further.
        # Our main loop.

        random_pass += 1
        skip_flag = False
        this_shot_sum = 0

        for n in range(TEN_SCORE,ONE_SCORE):
            #Count number of shots in present distribution, left to right, starting at 10-ring.
            this_shot_sum += distri[n]
            if this_shot_sum>possible:
                skip_flag = True
                break
                    #Break the for loop: If we are greater than 'possible' for the first three rings, there is no need to count the other 8.

        #FORCE CARRY
        if skip_flag and overflow_column:
            '''
            We learned the number number of shots was too high for this
            distribution, due to skip_flag.

            If possible = 5
            [0,3,3] #=> A total of 6 out of 5 possible shots. Invalid.
            Then we should ignore the rest of the [X,X,3] branch as we know
            [0,3,3] through [5,5,3] are invalid. Jump to [0,0,4] as if we just
            finished counting [5,5,3].

            To ignore, we perform a 'force carry'. As the decimal number 199
            counts up to 200, the leftmost digit increases, and all digits to
            the right are reset to 0.

            We perform the same action, except digits are our distribution
            elements and we count up from left-to-right.
            '''
            for s in range(TEN_SCORE,overflow_column+1):
                #Reset all to left of overflow_column to zero
                distri[s]=0
            distri[overflow_column+1]+=1

            fcarry_count+=1
                #Increase our supplementary statistic
        #END FORCE CARRY
        else:
            #In all cases where we are not forcibly carrying, we are counting up left-to-right from the 10-ring.
            distri[TEN_SCORE] += 1

        #CARRY
        for n in range(TEN_SCORE,ZERO_SCORE):
            '''
            Basic left-to-right carrying.

            After careful study of this context, carrying does not need to be
            recursive, as both the forced and unforced carries are conditional
            that columns (individually or collectively) must not ever surpass
            the possible number of shots.
            Thus there will only ever be maximum of one forced and one unforced
            carry per pass of our main loop.

            Example:
            If possible = 3
            [1,4,0,4,0] would never reach [1,0,1,4,0]
            as forced carry would have already changed to [0,0,0,0,1].
            Additionally, the existence of [1,4,0,4,0] would be paradoxical, as
            a previous forced or unforced carry would have caught any
            distribution of [X,X,X,4,0].
            '''
            if distri[n] > possible: #overflow
                distri[n] = 0
                    #we only need to change the current column to 0, for the same reason as above.
                distri[n+1] +=1
                    #range(x,y) stops before y. [n+1] will be within bounds of list if y is equal upper bounds of our list. "for n in range(1,10): print n" will never say "10"
                overflow_column = n
                    #latest column to CARRY from, useful for when we force carry.
        #END CARRY

        #TESTING LOGIC
        dist_sum = sum(distri)
            #This distribution's total number of shots.
        this_score = find_score(distri)
            #This distribution's score, as defined by find_score function.

        backtick("Working...")
            #Print out to the bottom of the screen the time and a message. Proves the script hasn't froze.

        if this_score > biggest_score:
            #Store our supplementary statistic of greatest score
            biggest_score = this_score
        if dist_sum > biggest_sum:
            #Store our supplementary statistic of greatest sum
            biggest_sum = dist_sum

        if random_pass == 1000000:
            #Every 1 Million failed distributions, print out some statistics to keep us busy.
            random_pass = 0
                #Random_pass is the counter for each individual distributions
            print "I'm still working... Mil-BiggestSum:"+str(biggest_sum)+"-BiggestScore:"+str(biggest_score)+"-SKIPS:"+str(fcarry_count)+"--"+str(distri)+" SC:"+str(this_score)+" SUM:"+str(dist_sum)
            '''
            Prints as follows:
            - "I'm still working..."
            - "Mil-"        : One million distributions have failed our tests
            - BiggestSum    : The tested distribution that had the most number of shots on target, however invalid
            - BiggestScore  : The tested distribution that had the greatest score, however invalid
            - SKIPS         : The number of times our code hs forced carried, avoiding entire invalid branches
            - --            : The present distribution being tested, however invalid
            - SC            : The score of present distribution, however invalid
            - SUM            : The number of shots of present distribution, however invalid
            '''

        #check results.
        if this_score==score:
            #This distribution's score is a match with our request
            if dist_sum==shot_count:
                #Even the number of shots match up. This is possibly the distribution that made the score
                print str(distri)+" SC:"+str(score)+" SUM:"+str(dist_sum)
            elif dist_sum<shot_count:
                '''
                There is a possibility that an experienced competitor has missed
                or lost shots on target. A misfire, hits on other competitors
                targets are awarded zero points.

                If the present distribution has fewer number of shots as hits,
                but has an equal score, it is possible that the remaining shots
                were all misses. Since a miss is zero points, we can put that
                back into our results.
                '''
                distri2 = [0,0,0,0,0,0,0,0,0,0,0,0]
                    #Creating a second distribution as not to alter the distribution we are iterating through
                for n in range(0,12):
                    distri2[n]=distri[n]
                    #Copy all the data from the first distribution into the second.
                distri2[ZERO_SCORE] = (shot_count-dist_sum)
                    #The difference between this distribution's shot count and the requested is equal to the number of missed shots. Place that into the ZERO_SCORE column.
                bad_distris.append(distri2)
                    #Take the distribution with missed shots and put it into the collection called bad_distris
        #END TESTING LOGIC

    if(show_possible):
        #If the user requested distributions with missed shots, print them out now, since we have iterated through all other possibilities.
        for n in bad_distris:
            this_sum = sum(n)
            this_zero = n[ZERO_SCORE]
            print "P:"+str(n)+" SC:"+str( find_score(n) )+" SUM:"+str( this_sum )+" HIT/MISS:"+str(this_sum-this_zero)+"/"+str(this_zero)
                #Print out the missed shot distributions differently than those which are a 100% match, as these are not as desireable.


find_distri(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]), show_possible)
    #Point of entry, pulls command line arguments and starts the main function.
