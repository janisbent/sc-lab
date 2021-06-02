'''
The critical region for this trace is easiest to see if you zoom to around x=[900, 1000] and the
y-axis cropped to the traces in that window.

Trace divergencies outside of this windown aren't particularly important to this attack.
'''
%matplotlib widget
plot_trace(dc.fetch('0000'), 50)
plot_trace(dc.fetch('9999'), 50)