

#find better way to make a list where
#the pointer does not conflict with the instantiation of numbers
#there has to be a better way of defining crap here.

moved = False
won = False
squares = 3
board = []

for x in range(squares): board.append([0]*squares)


turn = 1
p1 = 1
p2 = 2

#draws the background
def drawBackground():
    for x in range(squares):
        xcord = x * (width / squares)
        line(xcord,0,xcord,height)
    for y in range(squares):
        ycord = y * (height / squares)
        line(0,ycord,width,ycord)
        
#draws the pices onto the screen
#probably should rename this
def drawList(arr):
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if(arr[x][y] == p1):
                rectMode(CENTER)
                rect(x * sq_size + sq_size / 2,y * sq_size + sq_size / 2, sq_width,sq_width)
            if(arr[x][y] == p2):
                circle(x * sq_size + sq_size / 2,y * sq_size + sq_size / 2,sq_width / 2)

#sees if the game is won vertically
def vertWin(arr):
    #x in this case is a list
    for x in arr:
        #goes up the list and sees if it a solid line 
        #of one number(the player).
        winner = True
        for elem in x:
            winner = winner and (elem == turn)
        if winner:
            return winner
    return False

#transposes a board
def Transpose(arr):
    new_arr =[]
    for x in range(squares): new_arr.append([0]*squares)
    
    for x in range(squares):
        for y in range(squares):
            new_arr[x][y] = arr[y][x]
    return new_arr

#flips a board on the x-axis??
def Flip(arr):
    new_arr =[]
    for x in range(squares): new_arr.append([0]*squares)

    for y in range(squares):
        new_arr[y] = arr[squares - y - 1]
    return new_arr
        
#transposes the board and feeds it into vertWin
#i got the names of the 2 mixed up
def horiWin(arr):
    #println(arr)
    new_arr = Transpose(arr)
    return vertWin(new_arr)

#detects diaganolly win. probably buggy if the size of the
#board is increased but Ion really gotta worry about that
#right now.
#bruh, i shoulda worried about it... its pretty buggy
def diagWin(arr):
    won = True
    for x in range(squares):
        for p in range(squares - x):
            won = won and turn == arr[p][p]
    return won

#copy functions, not sure if python copies stuff correctly yet
def copyList(arr):
    new_list = []
    for x in arr:
        new_list.append(x)
    return new_list

def copyBoard(arr):
    new_arr =[]
    for x in range(squares): new_arr.append([0]*squares)

    for x in range(squares):
        for y in range(squares):
            new_arr[x][y] = arr[x][y]
    return new_arr
#not checked but the code is copied from elsewhere
def winner(arr):
    w = vertWin(arr) or horiWin(arr)
    w = w or diagWin(arr)
    w = w or diagWin(Flip(arr))
    return w
#check this function
#not-won but full board -> true/false
def full(arr):
    fu = True
    for x in range(squares):
        for y in range(squares):
            fu = fu and not(arr[x][y] == 0)
    return fu

#not checked, evaluates the board
#case b4, (1) skips past evaluation for some odd reason.
#when board has extra parts it skips???
#fixed skipping but now i need to make
#this look alot better
#since winner doesn't tell who had one. 
#I need to detect win that same turn.
def evaluate(arr,t):
    global turn
    oldturn = turn
    hasWon = False

    turn = p1
    if(winner(arr)):
        hasWon = True
    turn = p2
    if(winner(arr)):
        hasWon = True
        
    turn = oldturn
    if(hasWon and (t == p1)):
        return 1
    if(hasWon and (t == p2)):
        return -1
    if(full(arr)):
        turn = oldturn
        return 0
    
    return "none"


#the board,Turn
#the first turm is always players turn.
#not placing piece.
def minMax(arr,t):
    newT = p2 if t == p1 else p1
    #newArr = copyBoard(arr)
    #println(newArr)
    #print(newArr)
    #I need this to run off shallow copies. Can't have boards being linked to each other...
    #println("{} {}".format(t,arr))
    thevals = []
    #detects if board is already won or full
    if(not(evaluate(arr,t) == "none")):
        #evaluating the turn before
        return evaluate(arr,newT)
    
    for x in range(squares):
        for y in range(squares):

            #if(not(evaluate(arr,t) == "none")):
             #return evaluate(arr,t)
            #I added stuff after the and. I aint test too much into it though
            #does this count as making it faster???????
            if(arr[x][y] == 0 and (not(p2 == t and (-1 in thevals)) and not(p1 == t and (1 in thevals)))):
                newArr = copyBoard(arr)
                newArr[x][y] = t
                thevals.append(minMax(newArr,newT))
            
            
            #this does not terminate.......
            #if(t == p2 and arr[x][y] == 0):
             #   return max(evaluate(newArr,t),minMax(newArr,newT))

            #if(t == p1 and arr[x][y] == 0):
            #    return min(evaluate(newArr,t),minMax(newArr,newT))
            
    #print("values so far {}".format(thevals))
    if(t == p2):
        return min(thevals)
    if(t == p1):
        return max(thevals)
    
def doThoughts(arr):
    #calculates best moves
    options = []
    newT = p2 if turn == p1 else p1
    for x in range(squares):
        for y in range(squares):#added this too, but i dunno if it works
            if(arr[x][y] == 0 and (not(p2 == turn and (-1 in options)) and not(p1 == turn and (1 in options)))):
                
                newArr = copyBoard(arr)
                newArr[x][y] = turn
                #println("THE STARTING TURN IS {}".format(turn))
                
                options.append(minMax(newArr,newT))
    #finds the postions of the best move
    lowVal = copyList(options)
    lowVal.sort()
    #println("ordered{} : truth{}".format(lowVal,options))
    indx = lowVal[0]
    IndxOfPiece = options.index(indx)
    counter = 0
    #println("makes it here")
    for x in range(squares):
        for y in range(squares):
            if(IndxOfPiece == counter and arr[x][y] == 0):
                newArr = copyBoard(arr)
                newArr[x][y] = turn
                return newArr
            if(arr[x][y] == 0):
                counter += 1
    
    
#sets the game up.
def setup():
    size(400,400)
    background(255)
    drawBackground()

    global sq_size
    sq_size = width / squares
    global sq_width
    sq_width = sq_size - 10
    
#resets the game using r button
def keyPressed():
    if(key == 'r'):
        global board
        global turn
        global won
        background(255)
        drawBackground()
        won = False
        board =[]
        for x in range(squares): board.append([0]*squares)

        drawList(board)
    if(key == 't'):
        b1 = [[2,2,1],
              [0,1,0],
              [2,0,1]]
        b2 = [[2,1,1],
              [1,0,0],
              [2,0,2]]
        b3 = [[0,0,0],
              [0,0,0],
              [0,0,0]]
        b4 = [[2,1,1],
              [1,2,1],
              [2,0,2]]
        b5 = [[1,0,0],[0,0,0],[0,0,0]]
        #bad, very laggy at squares = 4
        b6 = [[1,2,2,0],
              [2,2,1,0],
              [0,0,0,0],
              [0,0,0,0]]
        
        #runs the loop in the selection process.
        #does not terminate and loops to infinity.
        #println("check board {}".format(evaluate(b6,2)))
        oldturn = turn
        turn = p2
        println("answer: {}".format(doThoughts(b6)))
        #println(b6)
        turn = oldturn
#is mouse called before setup?
#that would explain why I get an error if global turn is not defined
#before the setup is called. It seems to be called before even the whitespace
#is defined. odd. I need help with that...
#possible solution to this answer
#to affect(change or use) outside varibles. You need to use (global) function. 
#otherwise it is looking locally for the variable but it does not exist
#locally
def mousePressed():
    #get access to read/write global variables
    global turn
    global won
    global board
    global moved
    #calculates which tile the mouse clickedo n
    x_click = floor(map(mouseX, 0,width,0,squares))
    y_click = floor(map(mouseY,0,height,0,squares))
    moved = False
    
    #does the game logic here
    
    if(board[x_click][y_click] == 0 and not(won) and turn == p1):
        board[x_click][y_click] = turn
        won = vertWin(board) or horiWin(board)
        won = won or diagWin(board)
        won = won or diagWin(Flip(board))
        #print(board)
        #print(Flip(board))
        #print("space")
        #print(won)
        drawList(board)
        moved = True
    
    if(not(won) and turn == p2 and not(full(board))):
        #hehe, do-u minmax-u!
    
        computer_board = doThoughts(board)
        #println("b{}, cb{}".format(board,computer_board))
        board = computer_board
        
        won = vertWin(board) or horiWin(board)
        won = won or diagWin(board)
        won = won or diagWin(Flip(board))
        
        drawList(board)
        moved = True
        
        
    if(won):
        print("{} Player Won!".format(turn))
    if(moved):
        turn = p2 if turn == p1 else p1

#needs to be here else the sketch can't run anything
#although, we won't be needing it for anything
#the majesty of turn based games, no fps
#im usin it cuzz the ai won't show up other wise
#ill find another sol later
def draw():
    if(turn == p2):
        mousePressed()

        
