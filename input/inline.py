# Inline Expansion Complex Test Cases with Loops

# 1. Constant multiplication inside assignment
a = 12 * 4

# 2. Constant addition inside parentheses
b = (50 + 25)

# 3. Constant exponentiation (square)
c = 9 ** 2

# 4. Function returning inline multiplication
def f1():
    return (2 * 5) + 3

# 5. Inline addition inside an expression
x = (1 + 2) * (3 + 4)

# 6. Inline squaring inside variable assignment
y = (7 ** 2) + (2 ** 2)

# 7. Mixed variable + constant inline addition
z = 10 + (5 + 5)

# 8. Nested multiplications with loop
val = 1
for i in range(2):
    val *= (2 * 3) + (4 * 5)

# 9. Inline expansion inside if-condition inside loop
for i in range(3):
    if (2 + 3) > i:
        print("Inline addition in loop condition", i)

# 10. Inline exponentiation inside nested loop
for i in range(2):
    for j in range(2):
        p = (i + j) * (2 ** 2)
        print("Loop square:", p)

# 11. Inline expansion in while loop
k = 0
while k < (2 + 2):
    k += (3 * 3)
    print("While loop step:", k)

# 12. Inline in function argument (looped calls)
def square_and_add(n):
    return n + (4 ** 2)

for i in range(3):
    print("Function call:", square_and_add(i))
