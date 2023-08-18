import math
import numpy as np

# Remove [space] from script
def clean_string(strin):
    split = strin.split()
    counter = 0
    ret = ""
    for i in range(split):
        if counter > 3:
            break
        if i !=" ":
            counter+=1
            ret = ret+i
        
# Enter what part of the program you want to test.

testlibrary = [
    "str",
    "fun",
    "ite",
    "arr",
    "num",
    "cla",
]
var1 = input("Testing Code:")
print("Input: "+var1)
select = -1
counter = 0
for i in testlibrary:
    if var1 == i:
        select = counter
    counter += 1



if select == -1:
    print("End Program, invalid input.")
    exit()
elif select == 0:
    #String Logic
    print("Testing Strings::")
    print("Hello There \t Hello again, \n george washington once said \"UR GOOD \" \' apostrophe.  \\ backslash")
    # CONNECTATION
    print("CONNECTATION"+" : "+str(select))

    v_1 = "a"
    v_2 = "r"
    v_3 = "t" 
    v_4 = "s"
    tab = [v_1,v_2,v_3,v_4]
    for i in range( math.factorial(len(tab)) ):
        print(tab[0]+tab[1]+tab[2]+tab[3])

elif select ==1:
    #function logic
    print("Testing Numbers::")
    print(0.01231%1)    # % keyword rounds numbers
    qfunc = lambda a,b : a*b #Lambda is a quick function
    #raise("This user is a idiot") #raise creates an error, and halts execution
    def rawruwuboy(): #Function
        yield "First u say u are dumb" #Yields return a generator data type and loop through the function until all yields are complete?
        yield qfunc(1,2) 
        yield "UwU ily sm uwu uwu uwu"
    
    for i in rawruwuboy():
        print(str(i))

    def filter_odd(numbers):
        for number in range(numbers):
            if(number%2!=0):
                yield number 
    odd_numbers = filter_odd(20)
    single_string = ""
    for i in odd_numbers:
        single_string = single_string+str(i)+", "
    print(single_string)
    
    class uwuboy:
        def __init__(self,Name,Type):
            self.Name = "Name"; self.Type = Type

    myuwuboy = uwuboy
elif select ==2:
    #iteration logic
    print("Testing Iteration::")
elif select ==3:
    #array/library logic
    print("Testing Arrays::")
elif select==4:
    #number logic
    print("Testingo numbers")
    v = 1
    v = v+1 #addition
    v = v-1 #subtraction
    v = v*1 #multiplication
    v = v/0.5 #division
    v = v**2 #exponents
    v = math.sqrt(v) #square root
    v = -v
    v = math.abs(v) #absolute value (Positive)
    v = v%2 # modulus - returns remainder post division


    print("Finished Testing number logic")
