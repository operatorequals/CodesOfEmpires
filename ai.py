def go_random():
    x = random.randint(0,600)
    y = random.randint(0,600)
    move(x,y)
    return x,y

def timber_n(n, a):
    start = team.WOOD
    timber(a)
    while team.WOOD < start+n:
        print (team.WOOD)
        sleep(0.1)
    return team.WOOD - start

go_random()
sleep(1)
while not explored:
    go_random()
    sleep(0.5)

a = explored[-1]
if a.isWood:
    if team.WOOD < 200:
        print('Timbering')
        print(timber_n(200, a))
        print('timbered')

sleep(2)

