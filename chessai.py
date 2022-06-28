class gamestate:
    whitetomove = True
    def __init__(self):
        self.board = [
        ["br","bn","bb","bq","bk","bb","bn","br"],
        ["bp","bp","bp","bp","bp","bp","bp","bp"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["--","--","--","--","--","--","--","--"],
        ["wp","wp","wp","wp","wp","wp","wp","wp"],
        ["wr","wn","wb","wq","wk","wb","wn","wr"]]
        whitetomove = True
        self.movelog = []
        self.blackking = False
        self.whiteking  = True
        self.whitekingpositon = []
        self.blackkingposition = []
        
            
class information:
    def __init__(self):
        self.whitetomove = True
        