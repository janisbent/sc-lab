'''
Run this cell to see the result of all possible first digits of the pin.

Zoom to the critical area of x=[900, 1000]

We should see three groupings of traces, which each have different behaviors around about x=[925, 970]:
 1. Traces that dip with a nadir at around x=975 (roughly following green dashed line)
 2. Traces that go up to around x=970 and then continue even further (roughly following blue dashed line)
 3. A single trace that doesn't seem to fit either group (roughly following red dashed line)

Due to the behavior of strcmp, the first character of the pin is guaranteed to be checked, so we
can be certain that the behavior of every correct and incorrect first character is captured in the
trace.

Which first digit do you think is correct? What does group 1 of traces have in common? Group 3?
How does this help us decipher future pin guesses?
'''
%matplotlib widget
# group 1
plt.plot([925, 975], [.0199, .0145], 'go:', linewidth=10)
# group 2
plt.plot([925, 970], [.0189, .0205], 'bo:', linewidth=10)
# group 3
plt.plot([925, 940, 972, 990], [.0199, .0205, .015, .0138], 'ro:', linewidth=10)

# key guesses
for i in range(10):
    plot_trace(dc.fetch(f'{i}000'), 25)

