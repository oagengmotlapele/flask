start=0.5
next=24
for i in range(1,16):
    print(start, next)
    start*=2
    if start==0.5:pass
    else:
        next += start * 48

