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
permute an 'X'-count. As the 'X'-count is the most valuable metric, it is
more directly influenced by bias, which is why it is used strictly as an input.

### Usage

In case there's some step you have to take that publishes this project to a
server, this is the right time to state it.

```python score_finder.py 1418 48 150 f
```

And again you'd need to tell what the previous code actually does.


## Licensing

The code in this project is licensed under MIT license. Please find included LICENSE file for complete details.
