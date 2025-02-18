def greet():
    return "nihao"

for i in range(0,5):
     a = next((b for b in range(0,5) if b == 2),None)
    