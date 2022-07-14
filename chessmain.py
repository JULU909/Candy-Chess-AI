import pygame as p
import chessai
import random
import copy
width = height = 512
dimensions = 8
images = {}
sqsize = height//dimensions
p.init()
loose=[1,2,3]
win = [ 1,2]
def loadpictures():
    pieces = ["br","bn","bb","bq","bk","wr","wn","wb","wq","wk","bp","wp"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("chesspieces2/"+ piece + ".png"),(sqsize,sqsize))
    loose[0] = p.transform.scale(p.image.load("chesspieces2/" + "loss" + ".png"), (sqsize*3, sqsize*3))
    loose[1] = p.transform.scale(p.image.load("chesspieces2/" + "blackwon" + ".JPEG"), (sqsize*3, sqsize*3))
    loose[2] = p.transform.scale(p.image.load("chesspieces2/" + "blackwon2" + ".JPG"), (sqsize * 3, sqsize * 3))
    win[0] = p.transform.scale(p.image.load("chesspieces2/" + "whitewon" + ".JPG"), (sqsize * 3, sqsize * 3))
    win[1] = p.transform.scale(p.image.load("chesspieces2/" + "won" + ".JPG"), (sqsize * 3, sqsize * 3))

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
                #chessai.gamestate.whitetomove = True


                ai.minmaxing(gs, "b", 0, 1, "w",-10000,100000)
                #move , pieces = ai.getallpossiblemoves(gs,"b")
                #ai.bestmove(pieces,move,gs,"b")

                chessai.gamestate.whitetomove = True
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

        print(chessai.gamestate.castlingw)
        if (iswon(gs, "b")):

            winninscreen(screen, gs)
            p.display.flip()
            clock.tick(60)
            continue
        drawgamestat(screen,gs)
        if(iswon(gs,"w")):
            winninscreen2(screen, gs)
            p.display.flip()
            clock.tick(60)
            continue




        if len(playerclicks) == 1:
            possibilities(sqselected, gs, screen)
        clock.tick(60)
        p.display.flip()


def winninscreen(screen,gs):
    colors = [p.Color("white"), p.Color("DarkSeaGreen")]
    font = p.font.Font('freesansbold.ttf', 32)
    text = font.render('Black Victory', True, colors[0])
    screen.fill(colors[1])
    screen.blit(text, p.Rect(0 * sqsize, 2* sqsize, sqsize * 5, sqsize * 5))
    screen.blit(loose[0],p.Rect(0*sqsize,5*sqsize,sqsize*5,sqsize*5))
    screen.blit(loose[1], p.Rect(5 * sqsize, 0 * sqsize, sqsize * 5, sqsize * 5))
    screen.blit(loose[2], p.Rect(0 * sqsize, 5 * sqsize, sqsize * 5, sqsize * 5))


def winninscreen2(screen,gs):
    colors = [p.Color("white"), p.Color("DarkSeaGreen")]
    font = p.font.Font('freesansbold.ttf', 32)
    text = font.render('White Victory!', True, colors[0])
    screen.fill(colors[1])
    screen.blit(text, p.Rect(0 * sqsize, 2* sqsize, sqsize * 5, sqsize * 5))
    screen.blit(win[0],p.Rect(5*sqsize,0*sqsize,sqsize*5,sqsize*5))
    screen.blit(win[1], p.Rect(0 * sqsize, 5* sqsize, sqsize * 10, sqsize * 10))


                    

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
                playerclicks = [i,k]
                piece1 = gs.board[i][k]


                if piece1[1] == "q":
                    moves = queen.getmovespossible(playerclicks, gs, piece1[0])
                if piece1[1] == "r":
                    moves = rook.getmovespossible(playerclicks, gs, piece1[0])
                if piece1[1] == 'b':
                    moves = bishop.getmovespossible(playerclicks, gs, piece1[0])
                if piece1[1] == 'p':
                    moves = pawn.getmovespossible(playerclicks, gs, piece1[0])
                if piece1[1] == 'n':
                    moves = knight.getmovespossible(playerclicks, gs, piece1[0])
                if piece1[1] == "k":
                    moves = king.getmovespossible(playerclicks, gs, piece1[0])

                if piece1[1] == "q":
                    count += chessai.heuristics.queen[7-i][k]
                    count += 900
                    count += len(moves) / 100
                if piece1[1] == "r":
                    count += chessai.heuristics.rook[7-i][k]
                    count += 500
                    count += len(moves) / 100
                if piece1[1] == 'b':
                    count += chessai.heuristics.bishop[7-i][k]
                    count +=330
                    count += len(moves) / 100
                if piece1[1] == 'p':
                    count += chessai.heuristics.pawn[7-i][k]
                    count+= 100
                    count += len(moves) / 100

                if piece1[1] == 'n':
                    count += chessai.heuristics.knight[7-i][k]
                    count += 330
                    count += len(moves) / 100
                if piece1[1] == "k":
                    count += chessai.heuristics.king[7-i][k]
                    count += 20000
                    count += len(moves) / 100
                positions.append((i, k))

            if (gs.board[i][k][0] != color):

                piece1 = gs.board[i][k]
                if piece1[1] == "q":
                    count -= chessai.heuristics.queen[i][k]
                    count -= 900
                if piece1[1] == "r":
                    count -= chessai.heuristics.rook[i][k]
                    count -= 500
                if piece1[1] == 'b':
                    count -= chessai.heuristics.bishop[i][k]
                    count -= 330
                if piece1[1] == 'p':
                    count -= chessai.heuristics.pawn[i][k]
                    count -= 100
                if piece1[1] == 'n':
                    count += chessai.heuristics.knight[i][k]
                    count -=330
                if piece1[1] == "k":
                    count -= chessai.heuristics.king[i][k]
                    count -= 20000
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
        if piece1[1] == "k" :
            gs.board[playerclicks[0][0]][playerclicks[0][1]+2] = piece1
            gs.board[playerclicks[1][0]][playerclicks[1][1]-2] = piece2
            gs.board[playerclicks[0][0]][playerclicks[0][1]] = "--"
            gs.board[playerclicks[1][0]][playerclicks[1][1]] = "--"
            if piece1[0] == "b":
                chessai.gamestate.castlingb = True
            else :
                chessai.gamestate.castlingw = True
            return True
        return False
    elif(piece1 == "--" or piece2 == "--"):
        temp = gs.board[playerclicks[0][0]][playerclicks[0][1]]
        gs.board[playerclicks[0][0]][playerclicks[0][1]] = gs.board[playerclicks[1][0]][playerclicks[1][1]]
        gs.board[playerclicks[1][0]][playerclicks[1][1]] = temp
        if piece1[1] == "k" and piece1[0] == "b" or piece1[1] == "r" and piece1[0] == "b":
            chessai.gamestate.castlingb = True;
        if piece1[1] == "k" and piece1[0] == "w" or piece1[1] == "r" and piece1[0] == "w":
            chessai.gamestate.castlingw = True;
        return True

    else:
        temp = gs.board[playerclicks[0][0]][playerclicks[0][1]]
        gs.board[playerclicks[0][0]][playerclicks[0][1]] = "--"
        gs.board[playerclicks[1][0]][playerclicks[1][1]] = temp
        if piece1[1] == "k" and piece1[0] == "b" or piece1[1] == "r" and piece1[0] == "b":
            chessai.gamestate.castlingb = True;
        if piece1[1] == "k" and piece1[0] == "w" or piece1[1] == "r" and piece1[0] == "w":
            chessai.gamestate.castlingw = True;
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

    ismoved = 0

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

        if temp0 == 7 and temp1 == 4:
            if gs.board[7][5][0] == "-" and gs.board[7][6][0] == "-" and chessai.gamestate.castlingw == False:
                moves.append((7,7))

        if temp0 == 0 and temp1 == 4:
            if gs.board[0][5][0] == "-" and gs.board[0][6][0] == "-" and chessai.gamestate.castlingb == False:
                moves.append((0,7))
        return moves


class ai():
    def getallpossiblemoves(gs,color):
        positions = []
        for i in range(dimensions):
            for k in range(dimensions):
                if (gs.board[7-i][7-k][0] == color and gs.board[7-i][7-k][1] != "p" ):
                    positions.append((7-i,7-k))

        for i in range(dimensions):
            for k in range(dimensions):
                if (gs.board[7-i][7-k][0] == color and gs.board[7-i][7-k][1] == "p" ):
                    positions.append((7-i,7-k))

                    
        moves = []
        piece = []
        temp = []
        while (True) :
            for g in positions:

                piece1 = gs.board[g[0]][g[1]]
                if piece1[1] == "q":
                    temp = (queen.getmovespossible(g, gs, piece1[0]))
                    if len(temp) == 0 :
                        continue
                    moves.extend(temp)
                    piece.append(g)
                    piece.append(len(temp))
                    temp = []
                if piece1[1] == "r":
                    temp = (rook.getmovespossible(g, gs, piece1[0]))
                    if len(temp) == 0 :
                        continue
                    moves.extend(temp)
                    piece.append(g)
                    piece.append(len(temp))
                temp = []
                if piece1[1] == 'b':
                    temp = (bishop.getmovespossible(g, gs, piece1[0]))
                    if len(temp) == 0 :
                        continue
                    moves.extend(temp)
                    piece.append(g)
                    piece.append(len(temp))
                temp = []
                if piece1[1] == 'p':
                    temp = (pawn.getmovespossible(g, gs, piece1[0]))
                    if len(temp) == 0 :
                        continue
                    moves.extend(temp)
                    piece.append(g)
                    piece.append(len(temp))
                temp = []
                if piece1[1] == 'n':
                    temp = knight.getmovespossible(g, gs, piece1[0])
                    if len(temp) == 0 :
                        continue
                    moves.extend(temp)
                    piece.append(g)
                    piece.append(len(temp))
                temp = []
                if piece1[1] == "k":
                    temp = (king.getmovespossible(g, gs, piece1[0]))
                    if len(temp) == 0 :
                        continue
                    moves.extend(temp)
                    piece.append(g)
                    piece.append(len(temp))
                    temp = []
                if(len(moves) == 0):
                    continue;

            return moves,piece
            break











    dep2max  = -20000
    def minmaxing(gs,color,depth,ismax,ocolor,alpha,beta):

        temp.list = copy.deepcopy(gs.board)
        if depth == 4 :
            list = copy.deepcopy(gs.board)

            point = points(gs,"b")
            gs.board = copy.deepcopy(list)


            return point


        moves, pieces = ai.getallpossiblemoves(gs, color)
        list = copy.deepcopy(gs.board)
        temppoints = []
        tempmoves = []
        max = 0
        pointmax = -10000000
        pointmin = 100000000
        indc = 0
        for i in range(len(pieces)):
            if indc == 1:
                break
            if i%2 == 0 :
                piece = pieces[i]
            else :
                count = pieces[i]
                for i in range(count) :
                    move = moves[i+max]
                    t1 , t2 = chessai.gamestate.castlingw , chessai.gamestate.castlingb
                    if valid(gs,[piece,move]):

                        point = ai.minmaxing(gs,ocolor,depth+1,ismax+1,color,alpha,beta)

                        if depth == 0 :
                            print(point,piece,move)

                        chessai.gamestate.castlingw, chessai.gamestate.castlingb = t1, t2
                        gs.board = copy.deepcopy(list)

                        if(ismax%2 == 1) :
                            if point > pointmax :
                                pointmax = point
                                if point > alpha :
                                    alpha = point

                                bestmove = move
                                bestpiece = piece
                                if beta <= alpha :
                                    indc = 1
                                    break
                        else :
                            if point < pointmin :
                                pointmin = point
                                if point < beta :
                                    beta = point
                                bestmove = move
                                bestpiece = piece
                                if beta <= alpha :
                                    indc =1
                                    break


                max+= count


        if depth == 0 :
            print(depth, ismax, bestpiece, bestmove, pointmax)
            valid(gs,[bestpiece,bestmove])

        if (ismax % 2 == 1):
            if pointmax == -10000000 :
                pointmax == 0
            return pointmax
        else:
            if pointmin == 10000000 :
                pointmin == 0
            return pointmin



    def bestmove(piece,moves,gs,color):
        score = []
        temp.list = copy.deepcopy(gs.board)
        max = 0
        bestmove=[]
        x  = 0
        best = -200000
        temppoint = 0

        tempadder = 0
        for i in piece:
           if x%2 == 0:
            piece1 = i
           else:
               for g in range(i):
                   if( valid(gs,[piece1,moves[g+tempadder]])):
                       temppoint = points(gs,color)
                       gs.board = copy.deepcopy(temp.list)
                       if temppoint >best :
                           best = temppoint
                           bestmove = [piece1,moves[g+tempadder]]
               tempadder+=i
           x += 1

        valid(gs, bestmove)
        gs.board = copy.deepcopy(temp.list)



        return bestmove


class temp():
    list= []
    depth1 =0
    depth3 =0
    movesdepth =[]

if __name__ == '__main__':
    main()