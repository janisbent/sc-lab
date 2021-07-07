'''
The critical region for this trace is easiest to see if you crop to around x=[900, 1000] and the
y-axis cropped to the traces in that window.

Trace divergencies outside of this windown aren't particularly important to this attack.
'''
%matplotlib widget
plot_trace(dc.fetch('0000'), 50, (900, 1000))
plot_trace(dc.fetch('9999'), 50, (900, 1000))