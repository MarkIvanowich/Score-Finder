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
ONE_SCORE = 10
ZERO_SCORE = 11


def find_score(distri):
    #Calculates a score of a given distribution
    score = 0
    score += distri[X_SCORE]*10
        #X-Count is also worth 10
    for n in range(TEN_SCORE,ZERO_SCORE):
        score +=distri[n]*(11-n)
        '''
        A distribution which each element is indexed from left-to-right as
        the value decreases left-to-right would be

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
    #Main Function. Increments permutations left to right.
    random_pass = 0
        #Number of failed distributions since last successful: supplementary, resets every 1Mil
    random_count = 0
        #Number of million failed distributions, successfully: supplementary, never resets
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
        #We will stop once the Zero element of the distribution increases. There is other logic for distributions with missed shots.
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
            [0,3,3,0,0] #=> A total of 6 out of 5 possible shots. Invalid.
            Then we should ignore the rest of the [0,3,3,0,0] branch as we know
            [0,3,3,1,0] through [0,3,3,5,5] are invalid.

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
        for n in range(ONE_SCORE,X_SCORE,-1):
            #Basic left-to-right counting.
            if distri[n] > possible: #overflow
                distri[n] = 0
                distri[n+1] +=1
                    #range(x,y) stops before y. [n+1] will be within bounds of list if y is one less than upper limit
                overflow_column = n
                    #latest column to CARRY from, useful for when we force carry
        #END CARRY

#TODO: COMMENTS FROM HERE ON

        dist_sum = sum(distri)
        this_score = find_score(distri)

        backtick("Working...")

        if this_score > biggest_score:
            biggest_score = this_score
        if dist_sum > biggest_sum:
            biggest_sum = dist_sum

        if random_pass == 1000000:
            random_pass = 0
            random_count += 1
            print "I'm still working... NOP-"+str(random_count)+"Mil-BiggestSum:"+str(biggest_sum)+"-BiggestScore:"+str(biggest_score)+"-SKIPS:"+str(fcarry_count)+"--"+str(distri)+" SC:"+str(this_score)+" SUM:"+str(dist_sum)

        #check results.
        if find_score(distri)==score:
            if dist_sum==shot_count:
                print str(distri)+" SC:"+str(score)+" SUM:"+str(dist_sum)
                random_count = 0
            elif dist_sum<shot_count:
                distri2 = [0,0,0,0,0,0,0,0,0,0,0,0]
                for n in range(0,12):
                    distri2[n]=distri[n]
                distri2[ZERO_SCORE] = (shot_count-dist_sum)
                bad_distris.append(distri2)
    if(show_possible):
        for n in bad_distris:
            this_sum = sum(n)
            this_zero = n[ZERO_SCORE]
            print "P:"+str(n)+" SC:"+str( find_score(n) )+" SUM:"+str( this_sum )+" HIT/MISS:"+str(this_sum-this_zero)+"/"+str(this_zero)

find_distri(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]), show_possible)
