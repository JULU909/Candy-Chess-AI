class AI : 
    
    width = height = 512
    dimensions = 8
    images = {}
    sqsize = height//dimensions
   
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