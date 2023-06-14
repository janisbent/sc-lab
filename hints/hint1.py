'''
Let's assume that the structure of the power trace is primarily dependent on the code being run and
the data being operated on (and for this exercise, that is the case, although you may notice some
minor noise between individual traces, which smoothing can help iron out).

If this is true, then two identical runs (identical inputs to identical code) should look similar.
You can see that's the case by running this cell again.

NOTE: You might occasionally get a trace that looks significantly different, but this can be assumed
to be noise.

Given that, there's two primary variables that could vary in the trace.

First, if the same code path is taken, but different values are operated on, the spacing of features
(spikes) over time (horizontally) should be similar across runs, but certain features may vary in
amplitude (height) and shape. For example, where input of `0000` resulted in a spike around `x=90`,
a different input may result in a shorter spike or even a dip.

Second, if different inputs push the computation down different code paths, one of which takes
longer than the other (e.g., one trace went down the longer branch of an `if` or one trace stayed
in a loop for longer), you may the features of one trace get delayed (occuring further to the right)
after a certain point in time.
'''


%matplotlib widget
pump.enter("0000", 25)
pump.enter("0000", 25)
pump.enter("0000", 25)
pump.enter("0000", 25)
