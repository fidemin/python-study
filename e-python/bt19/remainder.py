

def remainder(number, divisor):
    return number % divisor


print(remainder(20, 7))

print(remainder(20, divisor=7)) #6
print(remainder(number=20, divisor=7)) #6
print(remainder(divisor=7, number=20)) #6

# fail case
try:
    print(remainder(20, number=7))
except Exception as e:
    print("[Error]", e)


