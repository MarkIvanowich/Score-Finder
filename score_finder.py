import time, datetime
import sys

show_possible = False

if(len(sys.argv)<=3):
    sys.exit("INVALID ARGUMENTS "+str(sys.argv))
else:
    if(len(sys.argv)>4):
        show_possible = False
        if str(sys.argv[4]).lower()=="y" or str(sys.argv[4]).lower()=="t" or str(sys.argv[4])=="1":
            show_possible= True

X_SCORE = 0
TEN_SCORE = 1
ONE_SCORE = 10
ZERO_SCORE = 11


def find_score(distri):
    score = 0
    score += distri[X_SCORE]*10
    for n in range(1,11):
        score +=distri[n]*(11-n)
    return score

def backtick(s):
        print str(datetime.datetime.now().time())+"-: "+ s,
        sys.stdout.flush()
        print "\r",

bad_distris=[]

def find_distri(score, x, shot_count, show_possible):


    random_pass = 0
    random_count = 0
    fcarry_count = 0
    biggest_score = 0
    biggest_sum = 0

    distri = [0,0,0,0,0,0,0,0,0,0,0,0]
    distri[X_SCORE] = x
    possible = shot_count-x # if we know n shots were X_SCORE, that leaves n-x possible other shots.
    print "There is a possible "+str(possible)+" shots left."


    overflow_column = 0
    while distri[ZERO_SCORE]<=0:
        random_pass += 1
        skip_flag = False
        this_shot_sum = 0

        for n in range(TEN_SCORE,ONE_SCORE): #count shots in present distribution, left to right.
            this_shot_sum += distri[n]
            if this_shot_sum>possible: #number of shots too high,
                skip_flag = True #callback flag
                break #we have what we need. break for loop.

        #FORCE CARRY
        if skip_flag and overflow_column: #number of shots was too high. we don't to continue this while loop iteration, go to the next one
            for s in range(TEN_SCORE,overflow_column+1):
                distri[s]=0 #ALL LEFT ZERO ON CARRY
            distri[overflow_column+1]+=1 # FORCEIBLY CARRY

            fcarry_count+=1; #count the forced carries
        #END FORCE CARRY
        else:
            distri[TEN_SCORE] += 1

        #CARRY
        for n in range(ONE_SCORE,X_SCORE,-1):
            if distri[n] > possible: #overflow
                distri[n] = 0
                distri[n+1] +=1 #range(x,y) stops before y
                overflow_column = n #latest column to CARRY from
        #END CARRY


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
