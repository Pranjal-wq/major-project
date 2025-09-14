# Dead Code Test Cases

# 1. Unused variable
x = 10   # dead
y = 20
print(y)

# 2. If condition always True
if True:
    print("Always runs")
else:
    print("Dead branch")

# 3. If condition always False
if False:
    print("Dead branch")
else:
    print("Always runs")

# 4. Code after return
def f1():
    return 5
    print("Dead")  # dead

# 5. Code after break
for i in range(3):
    break
    print("Dead")  # dead

# 6. Unreachable else
if True:
    print("Run")
else:
    print("Dead")

# 7. While False loop
while False:
    print("Never runs")  # dead

# 8. Constant condition (0 is False)
if 0:
    print("Dead")
else:
    print("Runs")

# 9. Constant condition (non-zero is True)
if 1:
    print("Runs")
else:
    print("Dead")

# 10. Multiple returns
def f2(x):
    if x > 0:
        return 1
        print("Dead")  # dead
    else:
        return -1
