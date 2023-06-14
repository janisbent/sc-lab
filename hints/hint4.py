'''
There are two important features the implementation of `strcmp`.

First, the loop that compares the strings aborts as soon as a difference is found. This will result in the comparison of strings whose first two characters match to take longer than it would have if only the first character matched. If this happens, you should see a delay in the features more correct string after a certain point in the trace.

Second, if the strings do not match, they return a negative value if the first string is smaller than the second and a positive value the other way around. The differences in these values (and the code that may rely on the sign of its return) should cause the trace to have no offset in time like above, but should cause it to have a different feature if the test password was greater than the correct password than it would if it was lesser than the correct password.
'''
