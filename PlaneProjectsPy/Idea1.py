'''
Calculate Primes between Y and X, non-inclusive of X

Luyu Wu - I'm so bored rn 
'''

def FindAmount(num):
    primes = [2]
    counter = 3
    while counter < num:
        pass_t = True
        for i in primes:
           # print(i,counter,counter//i)
            if counter-((counter // i)*i) == 0:
                pass_t = False
        if pass_t:
            primes.append(counter)
        counter += 1
    return primes


def FindBetween(x,y):
    yprimes = FindAmount(y)

    while x >= yprimes[0]:
        yprimes.remove(yprimes[0])
    print(yprimes)

FindBetween(3,13)
