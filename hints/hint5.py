'''
The critical region for this trace is easiest to see if you crop to around x=[900, 1000] and the
y-axis cropped to the traces in that window.

Trace divergencies outside of this windown aren't important to this attack.
'''
%matplotlib widget
dc.fetch_and_plot('0000', 50, (900, 1000))
dc.fetch_and_plot('0000', 50, (900, 1000))
dc.fetch_and_plot('0000', 50, (900, 1000))
dc.fetch_and_plot('9999', 50, (900, 1000))
dc.fetch_and_plot('9999', 50, (900, 1000))
dc.fetch_and_plot('9999', 50, (900, 1000))