import time
print(time.localtime().tm_hour)
if time.localtime().tm_hour > 12:
    print("LOL")