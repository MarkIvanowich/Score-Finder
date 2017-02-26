<img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Archery_Target_80cm.svg" alt="Archery Target 80cm.svg" width="145" height="145">

# Score-Finder

Simple python script to find possible permutations of a ten-ring
scorecard/target in pistol or archery competitions.

In archery and shooting sports, a ten-ring target is used as a metric for
accuracy. In the centre of the target/scorecard, there is the 'X'. A competitor
has the goal to hit the 'X' as many times as possible in their given round.
Outwards from the centre, are nine additional rings descending in score value
from 10. Both the 'X' and the 10 ring are worth 10 points. Since a score is the
summation of each hit on each ring, the 'X' count is the most valuable metric
for settling ties of equal score.

As the 'X'-count is the tie-settling metric for scores of equal value, another
question arises: what permutations of hits on the target create that score?
Along with this, we must accept the possibility that some shots on target were
a miss, with a score value of 0.

This python script, given adequate information, will output permutations of
hits on a target that equal the score. Since the 'X'-count is a metric whose
boundaries are based on a judge's discretion, (IE: Is a hit on 'X' based off
the centre or circumference of the projectile's marking?) this script does not
permute an 'X'-count.

### Usage

Within the directory of the `score_finder.py` file, the script should be used
as:

`python score_finder.py SCORE X_COUNT SHOTS SHOW_ZEROS`

#### SCORE

Type: `Integer`  
Required: `Yes`

The sum of all hits on target. Each hit is multiplied by their point value as
described above. This value's maximum is `10 * SHOTS` and has a minimum of 0.
Scores that are a maximum, minimum, or near minimum should not use this script,
as the number of permutations are too few to warrant usage.

#### X_COUNT

Type: `Integer`  
Required: `Yes`

The number of hits on the centre of the target. This is a supplementary input
and an aspect of the resulting permutation. Where this metric is not required,
this argument's value should be `0`. As the 'X'-count is the most valuable
metric, it is more directly influenced by bias than other scores. The 'X'-count
column of output permutations is not modified in any way, but is required for
score and shot count calculations.

#### SHOTS

Type: `Integer`  
Required: `Yes`

The number of shots on the target. This value is equal to the number of
projectiles fired or launched at the target for one competitor. This is the
most independent variable in the system, thus the most important.

#### SHOW_ZEROS

Type: `Char`  
Required: `false`

Set to `t`, `1`, or `y` to enable. Enabled if user desires permutations where
some shots fired missed the target, and are worth zero points.
These permutations are printed to the screen after every non-miss permutation
has been found. This also sorts results from best-to-worst case scenarios.

### Example

Numerous targets may be combined to find permutations which are physically
unfeasible: In PPC (Precision Pistol Competitions) matches there are a total
of 150 shots fired across 10 stages. If all 150 shots were on one paper target,
there will be more hole than paper. This is no obstacle for mathematics or
statistics.

```
python score_finder.py 1418 48 150 f
```
Shows all permutations of 150 shots to make a score of 1418 points, with a 48
'X'-count. Does not show permutations where hits were missed.



## Licensing
Image in this README is [CC BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/) by Alberto Barbati
1 June 2006
[Original image: Archery Target 80cm.svg](https://commons.wikimedia.org/wiki/File:Archery_Target_80cm.svg)



The code in this project is licensed under MIT license. Please find included LICENSE file for complete details.
