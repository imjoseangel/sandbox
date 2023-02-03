10 value$ = cint(rnd * 100) + 1
20 input "enter guess"; guess$
30 guess$ = val(guess$)
40 if guess$ < value$ then print "Too low"
50 if guess$ > value$ then print "Too high"
60 if guess$ = value$ then 80
70 goto 20
80 print "That's right"
