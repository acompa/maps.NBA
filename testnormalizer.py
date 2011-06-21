from normalizer import DataNormalizer
for s in ['game1', 'game2', 'game4', 'game6']:
    norm = DataNormalizer(s)
    norm.check_corpus()
    #norm.adjust_time()
