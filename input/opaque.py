# Opaque Predicate Complex Test Cases

# 1. Always true with redundant check inside loop
for i in range(2):
    if (2 + 2 == 4) and (3 > 1):
        print("Loop always true:", i)

# 2. Always false predicate (never executes)
for j in range(3):
    if (5 < 2) or (10 < 3):
        print("This will never print", j)

# 3. Constant comparison with while loop
k = 0
while k < 2:
    if (100 == 100):
        print("While loop always true", k)
    k += 1

# 4. Arithmetic inside comparison
if (2 * 3 == 6) and (4 - 1 == 3):
    print("Inline arithmetic always true")

# 5. Complex but always true condition in function
def check_predicate():
    if (50 - 25 == 25) and (4**2 == 16):
        return "Function always true"
    return "Unreachable"

print(check_predicate())

# 6. Complex but false inside loop
for i in range(2):
    if (9 % 2 == 0) or (7 < 3):
        print("Never executes")

# 7. Nested opaque predicates
if ((10/2) == 5):
    if ((3*3) == 9):
        print("Nested always true")

# 8. Redundant always true inside loop
for i in range(2):
    if (8 > 3) and (2 < 5):
        print("Redundant always true", i)

# 9. Impossible opaque condition
if (1 == 2) or (0 > 10):
    print("Impossible branch")

# 10. Hidden constant compare inside function + loop
def hidden_check(x):
    if (x * 2 == 8) and (16/4 == 4):
        return True
    return False

for val in [4, 5]:
    if hidden_check(val):
        print("Hidden opaque true for", val)
