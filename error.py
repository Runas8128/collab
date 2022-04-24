class NotExistPart(Exception):
    def __init__(self, partNo: int):
        self.msg = f'Invalid partNo: {partNo}'
        super().__init__(self.msg)
    
    def __str__(self):
        return self.msg
