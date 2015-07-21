from lib import vectorloader

# all of our data - mostly for reference
subjects = ['nick', 'john']
electrodePositions = ['erb', 'erh', 'normal']
tasks = ['auditory', 'baseline', 'color count', 'eye move', 'eye open move', 'eye open static', 'imagine rotating a cube', 'imagined auditory', 'motor imagery', 'pass', 'videoclip']

vectorloader.allVectors('john', 'erh', tasks[0])