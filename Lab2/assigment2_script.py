#Question 1
#Multiply all list items together
part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
result = 1    
 # ^^^ Have to have a valid start to multiply the numbers in the list
for item in part1:
    result = result * item
    # ^^^ Start multiplying the first number in the list by 1, then multipky the quotient by next number in list
print('Answer to question 1 is: ',result)

#Question 2
#Add all list items together
part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]
answer = 0
for num in part2:
    answer = answer + num
print('Answer to question 2 is: ',answer)

#Question 3
#Only add the even numbers together
part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 
sum=0
 # ^^^ Have to have a valid start to begin adding the numbers in the list
for nums in part3:
    if nums % 2 == 0:
        sum = sum + nums
# If the numbers in the list are divided by 2 and leave a quotient of zero,
#Then only those numbers will be summed together
print('The anser to question 3 is: ',sum)

