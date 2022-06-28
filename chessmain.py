import pygame as p
import chessai
import random
import copy
width = height = 512
dimensions = 8
images = {}
sqsize = height//dimensions

def loadpictures():
    pieces = ["br","bn","bb","bq","bk","wr","wn","wb","wq","wk","bp","wp"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("chesspieces2/"+ piece + ".png"),(sqsize,sqsize))

    ## this is to load the images of the chess pieces onto the game.

def main():
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessai.gamestate()
    loadpictures() # once before thw while loop
    running  = True
    sqselected = ()
    playerclicks = []
    while running:
        moves = []
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if (chessai.gamestate.whitetomove == False):

                #ai.smartmove(gs)
                chessai.gamestate.whitetomove = True
                print(ai.minmaxing(gs, "b", 0, 1, "w"))
                continue
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//sqsize
                row = location[1]//sqsize
                if sqselected == (row,col):
                    sqselected = ()
                    playerclicks = []
                else :
                    sqselected = (row,col)
                    playerclicks.append(sqselected)

                if len(playerclicks) == 2:
                    moves = possibilities(playerclicks[0], gs, screen)


                    if playerclicks[1] in moves:
                        if (valid(gs,playerclicks)):
                            chessai.gamestate.whitetomove = False


                    sqselected = ()
                    playerclicks = []



        drawgamestat(screen,gs)
        if(iswon(gs,"w")):
            break;
        if(iswon(gs,"b")):
            break;
        print(points(gs,"w"))
        print(chessai.gamestate.whitetomove)

        if len(playerclicks) == 1:
            possibilities(sqselected, gs, screen)
        clock.tick(60)
        p.display.flip()




                    

def drawgamestat(screen,gs):
        drawboard(screen)
        drawpieces(screen,gs.board)


def drawboard(screen): 
    colors = [p.Color("white"),p.Color("DarkSeaGreen")]
    for r in range(dimensions):
        for c in range(dimensions):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*sqsize,r*sqsize,sqsize,sqsize))

def drawpieces(screen,board):
    for r in range(dimensions):
        for c in range (dimensions):
            piece = board[r][c]
            if (piece != '--'):
                screen.blit(images[piece],p.Rect(c*sqsize,r*sqsize,sqsize,sqsize))



def points(gs,color):
    positions = []
    count = 0
    for i in range(dimensions):
        for k in range(dimensions):
            if (gs.board[i][k][0] == color):

                piece1 = gs.board[i][k]
                if piece1[1] == "q":
                    count+=120
                if piece1[1] == "r":
                    count+=90
                if piece1[1] == 'b':
                    count+=40
                if piece1[1] == 'p':
                    count+=10
                if piece1[1] == 'n':
                    count+=40
                if piece1[1] == "k":
                    count+=200
                positions.append((i, k))

            if (gs.board[i][k][0] != color):

                piece1 = gs.board[i][k]
                if piece1[1] == "q":
                    count-=120
                if piece1[1] == "r":
                    count-=90
                if piece1[1] == 'b':
                    count-=40
                if piece1[1] == 'p':
                    count-=10
                if piece1[1] == 'n':
                    count-=40
                if piece1[1] == "k":
                    count-=200
                positions.append((i, k))
    return count



def possibilities(playerclicks,gs,screen):
    piece1 = gs.board[playerclicks[0]][playerclicks[1]]
    moves=[]
    if piece1[1] == "q":
        moves = queen.getmovespossible(playerclicks, gs, piece1[0])
    if piece1[1] == "r":
        moves = rook.getmovespossible(playerclicks, gs, piece1[0])
    if piece1[1] == 'b':
        moves = bishop.getmovespossible(playerclicks,gs,piece1[0])
    if piece1[1] == 'p':
        moves = pawn.getmovespossible(playerclicks,gs,piece1[0])
    if piece1[1] == 'n':
        moves = knight.getmovespossible(playerclicks,gs,piece1[0])
    if piece1[1]=="k":
        moves = king.getmovespossible(playerclicks,gs,piece1[0])
    for i in moves:
        c= i[1]
        r= i[0]
        p.draw.rect(screen, "Purple", p.Rect(c * sqsize - 3, r * sqsize - 3, sqsize + 3, sqsize + 3), 2)
    return moves



##  need to add a post move checker to check for check, checkmate, promotion, stalemate, castling



def valid(gs,playerclicks):
    piece1 = gs.board[playerclicks[0][0]][playerclicks[0][1]]
    piece2 = gs.board[playerclicks[1][0]][playerclicks[1][1]]
    if piece1 == piece2 :
        return False
    elif (piece1[0] == piece2 [0]):
        return False
    elif(piece1 == "--" or piece2 == "--"):
        temp = gs.board[playerclicks[0][0]][playerclicks[0][1]]
        gs.board[playerclicks[0][0]][playerclicks[0][1]] = gs.board[playerclicks[1][0]][playerclicks[1][1]]
        gs.board[playerclicks[1][0]][playerclicks[1][1]] = temp
        return True

    else:
        temp = gs.board[playerclicks[0][0]][playerclicks[0][1]]
        gs.board[playerclicks[0][0]][playerclicks[0][1]] = "--"
        gs.board[playerclicks[1][0]][playerclicks[1][1]] = temp
        return True


def iswon(gs,color):
    for i in range(dimensions):
        for k in range(dimensions):
            if (gs.board[i][k][0] != color):
                if(gs.board[i][k][1] == "k"):
                    return 0

    return 1



class queen():
    def getmovespossible(position,gs,color):
        moves= []
        temp0 = position[0]
        temp1 = position[1]
        check1=0
        check2=0
        ##horizontal moves:
        for r in range (temp0-1,-1,-1):
            if gs.board[r][temp1] != "--":
                if (gs.board[r][temp1][0] != color):
                    moves.append((r, temp1))
                break
            moves.append((r,temp1))
        for r in range(temp0+1,8):
            if gs.board[r][temp1] != "--":
                if (gs.board[r][temp1][0] != color):
                    moves.append((r, temp1))
                break
            moves.append((r,temp1))

        ##vertical moves:
        for c in range(temp1-1,-1,-1):
            if gs.board[temp0][c] != "--":
                if(gs.board[temp0][c][0] != color ):
                    moves.append((temp0, c))
                break
            moves.append((temp0,c))

        for c in range(temp1+1,8):
            if gs.board[temp0][c] != "--":
                if (gs.board[temp0][c][0] != color):
                    moves.append((temp0, c))
                break
            moves.append((temp0,c))


        #cross moves
        for r in range(7):
            if temp0+1+r >7 :
                break
            if temp1+1+r>7:
                break
            if gs.board[temp0+1+r][temp1+r+1] != "--":
                if gs.board[temp0+r+1][temp1+r+1][0] != color :
                    moves.append((temp0+r+1,temp1+r+1))
                break
            moves.append((temp0+r+1,temp1+r+1))

        for r in range(7):
            if temp0-1-r <0 :
                break
            if temp1-1-r<0:
                break
            if gs.board[temp0-1-r][temp1-r-1] != "--":
                if gs.board[temp0-r-1][temp1-r-1][0] != color :
                    moves.append((temp0-r-1,temp1-r-1))
                break
            moves.append((temp0-r-1,temp1-r-1))

        for r in range(7):
            if temp0-1-r <0 :
                break
            if temp1+1+r>7:
                break
            if gs.board[temp0-1-r][temp1+r+1] != "--":
                if gs.board[temp0-r-1][temp1+r+1][0] != color :
                    moves.append((temp0-r-1,temp1+r+1))
                break
            moves.append((temp0-r-1,temp1+r+1))

        for r in range(7):
            if temp0+1+r > 7:
                break
            if temp1-1-r<0:
                break
            if gs.board[temp0+1+r][temp1-r-1] != "--":
                if gs.board[temp0+r+1][temp1-r-1][0] != color :
                    moves.append((temp0+r+1,temp1-r-1))
                break
            moves.append((temp0+r+1,temp1-r-1))

        return moves



class rook():
    def getmovespossible(position,gs,color):
        moves = []
        temp0 = position[0]
        temp1 = position[1]
        check1 = 0
        check2 = 0
        ##horizontal moves:
        for r in range(temp0 - 1, -1, -1):
            if gs.board[r][temp1] != "--":
                if (gs.board[r][temp1][0] != color):
                    moves.append((r, temp1))
                break
            moves.append((r, temp1))
        for r in range(temp0 + 1, 8):
            if gs.board[r][temp1] != "--":
                if (gs.board[r][temp1][0] != color):
                    moves.append((r, temp1))
                break
            moves.append((r, temp1))
        ##vertical moves:
        for c in range(temp1 - 1, -1, -1):
                if gs.board[temp0][c] != "--":
                    if (gs.board[temp0][c][0] != color):
                        moves.append((temp0, c))
                    break
                moves.append((temp0, c))

        for c in range(temp1 + 1, 8):
            if gs.board[temp0][c] != "--":
                if (gs.board[temp0][c][0] != color):
                        moves.append((temp0, c))
                break
            moves.append((temp0, c))

        return moves


class bishop():
    def getmovespossible(position, gs, color):
        moves = []
        temp0 = position[0]
        temp1 = position[1]
        check1 = 0
        check2 = 0

        # cross moves
        for r in range(7):
            if temp0 + 1 + r > 7:
                break
            if temp1 + 1 + r > 7:
                break
            if gs.board[temp0 + 1 + r][temp1 + r + 1] != "--":
                if gs.board[temp0 + r + 1][temp1 + r + 1][0] != color:
                    moves.append((temp0 + r + 1, temp1 + r + 1))
                break
            moves.append((temp0 + r + 1, temp1 + r + 1))

        for r in range(7):
            if temp0 - 1 - r < 0:
                break
            if temp1 - 1 - r < 0:
                break
            if gs.board[temp0 - 1 - r][temp1 - r - 1] != "--":
                if gs.board[temp0 - r - 1][temp1 - r - 1][0] != color:
                    moves.append((temp0 - r - 1, temp1 - r - 1))
                break
            moves.append((temp0 - r - 1, temp1 - r - 1))

        for r in range(7):
            if temp0 - 1 - r < 0:
                break
            if temp1 + 1 + r > 7:
                break
            if gs.board[temp0 - 1 - r][temp1 + r + 1] != "--":
                if gs.board[temp0 - r - 1][temp1 + r + 1][0] != color:
                    moves.append((temp0 - r - 1, temp1 + r + 1))
                break
            moves.append((temp0 - r - 1, temp1 + r + 1))

        for r in range(7):
            if temp0 + 1 + r > 7:
                break
            if temp1 - 1 - r < 0:
                break
            if gs.board[temp0 + 1 + r][temp1 - r - 1] != "--":
                if gs.board[temp0 + r + 1][temp1 - r - 1][0] != color:
                    moves.append((temp0 + r + 1, temp1 - r - 1))
                break
            moves.append((temp0 + r + 1, temp1 - r - 1))

        return moves




class pawn():

    def getmovespossible(position, gs, color):
        moves = []
        temp0 = position[0]
        temp1 = position[1]
        check1 = 0
        check2 = 0
        if color == 'w' and temp0 == 6:
            if gs.board[temp0 - 1][temp1][0] == "-":
                moves.append((temp0 - 1, temp1))
                if temp1 <7 :
                    if gs.board[temp0 - 1][temp1 + 1][0] == "b":
                        moves.append((temp0 - 1, temp1 + 1))
                if temp1 >0 :
                    if gs.board[temp0 - 1][temp1 - 1][0] == "b":
                        moves.append((temp0 - 1, temp1 - 1))
                if gs.board[temp0 - 2][temp1][0] == "-":
                    moves.append((temp0 - 2, temp1))

            return moves
                     


            return moves
        if color == 'b' and temp0 == 1:
            if gs.board[temp0+1][temp1][0] == "-":
                moves.append((temp0 + 1, temp1))
                if gs.board[temp0 + 1][temp1][0] != "b":
                    moves.append((temp0 + 1, temp1))
                if temp1<7 :
                    if gs.board[temp0 + 1][temp1 + 1][0] == "w":
                        moves.append((temp0 + 1, temp1 + 1))
                if temp1>0 :
                    if gs.board[temp0 + 1][temp1 - 1][0] == "w":
                        moves.append((temp0 + 1, temp1 - 1))
                if gs.board[temp0+2][temp1][0] == "-":
                    moves.append((temp0 + 2, temp1))

            return moves
        if color == "b" :
            if temp0 <7 :
                if gs.board[temp0 + 1][temp1][0] != "b" :
                    moves.append((temp0 + 1, temp1))
            if temp1 < 7 & temp0 < 7:
                if gs.board[temp0 + 1][temp1+1][0] == "w":
                    moves.append((temp0 + 1, temp1+1))
            if temp1 >  0 and temp0 <7 :
                if gs.board[temp0 + 1][temp1-1][0] == "w":
                    moves.append((temp0 + 1, temp1-1))
        if color == 'w' :
            if temp0 > 0 :
                if gs.board[temp0 - 1][temp1][0] != "w":
                    moves.append((temp0 - 1, temp1))
            if temp1 < 7 :
                if gs.board[temp0 - 1][temp1+1][0] == "b":
                    moves.append((temp0 - 1, temp1+1))
            if temp1 > 0 :
                if gs.board[temp0 - 1][temp1-1][0] == "b":
                    moves.append((temp0 - 1, temp1-1))
        for i in moves :
            if (i[1] - temp1 == 0):
                if gs.board[i[0]][i[1]] != "--":
                    moves.remove(i)

        return moves


class knight():
    def getmovespossible(position, gs, color):
        moves = []
        temp0 = position[0]
        temp1 = position[1]
        check1 = 0
        check2 = 0
        pos1 = [+1,+2,-1,-2]
        neg1 = [-1,-2,+1,+2]

        for i in pos1:
            for m in neg1:
                if abs(i) == abs(m):
                    continue
                if temp0+i > 7 or temp1+m >7 or temp1+m <0 or temp0+i<0 :
                    continue
                if gs.board[temp0 + i][temp1+m][0] != color:
                    moves.append((temp0 + i, temp1 + m))


        return moves

class king():
    def getmovespossible(position, gs, color):
        moves = []
        temp0 = position[0]
        temp1 = position[1]
        check1 = 0
        check2 = 0
        pos1 = [+1, +2, -1, -2]
        neg1 = [-1, -2, +1, +2]
        pos1 = [+1, -1,0]
        neg1 = [-1, +1,0]

        for i in pos1:
            for m in neg1:
                if i == m == 0:
                    continue
                if temp0 + i > 7 or temp1 + m > 7 or temp1 + m < 0 or temp0 + i < 0:
                    continue
                if gs.board[temp0 + i][temp1 + m][0] != color:
                    moves.append((temp0 + i, temp1 + m))

        return moves


class ai():
    def getallpossiblemoves(gs):
        positions = []
        for i in range(dimensions):
            for k in range(dimensions):
                if (gs.board[i][k][0] == "b"):
                    positions.append((i,k))
        moves = []
        while (True) :
            g = random.choice(positions)
            print(g )
            print("random postion ")


            piece1 = gs.board[g[0]][g[1]]
            if piece1[1] == "q":
                    moves.extend(queen.getmovespossible(g, gs, piece1[0]))
            if piece1[1] == "r":
                    moves.extend(rook.getmovespossible(g, gs, piece1[0]))
            if piece1[1] == 'b':
                        moves.extend(bishop.getmovespossible(g, gs, piece1[0]))
            if piece1[1] == 'p':
                            moves.extend(pawn.getmovespossible(g, gs, piece1[0]))
            if piece1[1] == 'n':
                            moves.extend(knight.getmovespossible(g, gs, piece1[0]))
            if piece1[1] == "k":
                            moves.extend(king.getmovespossible(g, gs, piece1[0]))
            if(len(moves) == 0):
                continue;
            aimove = random.choice(moves)

            main = [g,aimove]
            if(valid(gs,main) == False):
                continue
            print(moves)
            print("done")
            break

    def smartmove(gs):
        positions = []
        data2 = []
        data = []
        data4=[]
        temp.list = copy.deepcopy(gs.board)

        for i in range(dimensions):
            for k in range(dimensions):
                if (gs.board[i][k][0] == "b"):
                    positions.append((i, k))
        moves = []
        dict ={}
        while (True):

            print("random postion ")
            for i in positions:
                g = i
                piece1 = gs.board[g[0]][g[1]]
                moves = []
                if piece1[1] == "q":
                    moves.extend(queen.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == "r":
                    moves.extend(rook.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'b':
                    moves.extend(bishop.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'p':
                    moves.extend(pawn.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'n':
                    moves.extend(knight.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == "k":
                    moves.extend(king.getmovespossible(g, gs, piece1[0]))
                tally = []
                if (len(moves) == 0):
                    continue;
                data3= []
                for i in moves:
                    if (valid(gs,[g,i])):

                        b = points(gs,"b")
                        valid(gs, [i, g])
                        tally.append(b)
                        data3.append(i)
                        gs.board = copy.deepcopy(temp.list)
                z = max(tally)

                data2.append(data3[tally.index(z)])
                print(data3)
                print(tally)
                data.append(g)
                data4.append(z)

            gs.board = copy.deepcopy(temp.list)
            print(data2)
            print(data)
            print(data4)
            print("done")
            smartpoint = max(data4)
            smartposition = data[data4.index(smartpoint)]
            smartmove = data2[data4.index(smartpoint)]

            print(smartpoint,smartposition,smartmove)
            print("computed Ai move")
            output = [[smartposition[0],smartposition[1]],[smartmove[0],smartmove[1]]]
            print(output)
            valid(gs,output)
            break
    def dumbmove(gs):
        positions = []
        data2 = []
        data = []
        data4=[]
        temp.list = copy.deepcopy(gs.board)

        for i in range(dimensions):
            for k in range(dimensions):
                if (gs.board[i][k][0] == "w"):
                    positions.append((i, k))
        moves = []
        dict ={}
        while (True):

            print("random postion ")
            for i in positions:
                g = i
                piece1 = gs.board[g[0]][g[1]]
                moves = []
                if piece1[1] == "q":
                    moves.extend(queen.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == "r":
                    moves.extend(rook.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'b':
                    moves.extend(bishop.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'p':
                    moves.extend(pawn.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'n':
                    moves.extend(knight.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == "k":
                    moves.extend(king.getmovespossible(g, gs, piece1[0]))
                tally = []
                if (len(moves) == 0):
                    continue;
                data3= []
                for i in moves:
                    if (valid(gs,[g,i])):

                        b = points(gs,"w")
                        valid(gs, [i, g])
                        tally.append(b)
                        data3.append(i)
                        gs.board = copy.deepcopy(temp.list)
                z = min(tally)

                data2.append(data3[tally.index(z)])
                print(data3)
                print(tally)
                data.append(g)
                data4.append(z)

            gs.board = copy.deepcopy(temp.list)
            print(data2)
            print(data)
            print(data4)
            print("done")
            smartpoint = min(data4)
            smartposition = data[data4.index(smartpoint)]
            smartmove = data2[data4.index(smartpoint)]

            print(smartpoint,smartposition,smartmove)
            print("computed Ai move")
            output = [[smartposition[0],smartposition[1]],[smartmove[0],smartmove[1]]]
            valid(gs,output)
            return smartpoint,output
    def smartmove2(gs):
        positions = []
        data2 = []
        data = []
        data4=[]
        temp.list = copy.deepcopy(gs.board)

        for i in range(dimensions):
            for k in range(dimensions):
                if (gs.board[i][k][0] == "b"):
                    positions.append((i, k))
        moves = []
        dict ={}
        while (True):

            for i in positions:
                g = i
                piece1 = gs.board[g[0]][g[1]]
                moves = []
                if piece1[1] == "q":
                    moves.extend(queen.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == "r":
                    moves.extend(rook.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'b':
                    moves.extend(bishop.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'p':
                    moves.extend(pawn.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'n':
                    moves.extend(knight.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == "k":
                    moves.extend(king.getmovespossible(g, gs, piece1[0]))
                tally = []
                if (len(moves) == 0):
                    continue;
                data3= []
                for i in moves:
                    if (valid(gs,[g,i])):

                        b = points(gs,"b")
                        valid(gs, [i, g])
                        tally.append(b)
                        data3.append(i)
                        gs.board = copy.deepcopy(temp.list)
                z = max(tally)

                data2.append(data3[tally.index(z)])

                data.append(g)
                data4.append(z)

            gs.board = copy.deepcopy(temp.list)


            smartpoint = max(data4)
            smartposition = data[data4.index(smartpoint)]
            smartmove = data2[data4.index(smartpoint)]


            output = [[smartposition[0],smartposition[1]],[smartmove[0],smartmove[1]]]
            valid(gs,output)
            f = points(gs,output)
            gs.board = copy.deepcopy(temp.list)
            return f
            break

    def minmaxing(gs,color,depth,ismax,ocolor):
        print("startyt==")
        if iswon(gs,color) :
            print("e")
            return 1000;
        if iswon(gs,ocolor) :
            print("f")
            return -1000;
        if depth == 2 :
            print("as")
            return ai.smartmove2(gs)
        positions = []
        temp.list = copy.deepcopy(gs.board)

        for i in range(dimensions):
            for k in range(dimensions):
                if (gs.board[i][k][0] == color):
                    positions.append((i, k))
        data2 = []
        data1 = []
        data4 = []
        list = copy.deepcopy(gs.board)
        while (True):

            print("random postion ")
            for i in positions:
                g = i
                piece1 = gs.board[g[0]][g[1]]
                moves = []
                if piece1[1] == "q":
                    moves.extend(queen.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == "r":
                    moves.extend(rook.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'b':
                    moves.extend(bishop.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'p':
                    moves.extend(pawn.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == 'n':
                    moves.extend(knight.getmovespossible(g, gs, piece1[0]))
                if piece1[1] == "k":
                    moves.extend(king.getmovespossible(g, gs, piece1[0]))
                tally = []
                if (len(moves) == 0):
                    continue;
                data3= []
                print(i)
                print(moves)
                for m in moves:
                    valid(gs,[m,g])
                    if (ismax ):
                        z = ai.minmaxing(gs,ocolor,depth+1,0,color)
                        print(z)
                        gs.board = copy.deepcopy(list)
                        data3.append(z)
                        data1.append(m)
                    else :
                        z = ai.minmaxing(gs,ocolor,depth+1,1,color)
                        print(z)
                        gs.board = copy.deepcopy(list)
                        data3.append(z)
                        data1.append(m)

                print(moves)
                if (ismax ):
                    data2.append(max(data3))
                    smartposition = data1[data3.index(max(data3))]
                    data4.append(g)

                else :
                    data2.append(min(data3))
                    data4.append(g)

            if (ismax ) :
                smartpoint = m(data2)
                smartmove = data4[data2.index(smartpoint)]
            else :
                smartpoint = min(data2)
                smartmove = data4[data2.index(min(data2))]
            print(depth)
            if depth == 0:
                print("smart")
                print(smartposition,smartmove)
                print(smartpoint )
                print("en2")
                valid(gs,[smartposition,smartmove])
                return smartmove,smartposition

            else :
                print(smartpoint)
                print("end")

                return smartpoint




class temp():
    list= []

if __name__ == '__main__':
    main()