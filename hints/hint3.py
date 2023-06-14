'''
Check out the implementation of `strcmp` (simplified for readability):
    
```
int strcmp(const char* s1, const char* s2) {
    while(*s1 && (*s1 == *s2)) {
        s1++;
        s2++;
    }
    return *s1 - *s2;
}
```

If `s1` is the input you send and `s2` is the correct password, what behaviors of `strcmp` might cause different structures in the power?
'''
