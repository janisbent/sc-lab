'''
The critical region for this trace is easiest to see if you crop to around x=[900, 1000] and the
y-axis cropped to the traces in that window.

Trace divergencies outside of this windown aren't important to this attack.
'''
%matplotlib widget
pump.enter('0000', 50, (900, 1000))
pump.enter('0000', 50, (900, 1000))
pump.enter('0000', 50, (900, 1000))
pump.enter('9999', 50, (900, 1000))
pump.enter('9999', 50, (900, 1000))
pump.enter('9999', 50, (900, 1000))
