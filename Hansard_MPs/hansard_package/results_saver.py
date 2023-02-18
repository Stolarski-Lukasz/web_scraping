import pickle
import pandas as pd

class ResultsSaver:
    def __init__(self, source):
        self.source = source
        self.data_frame = pd.DataFrame(self.source)

    def save_as_pickle(self, target):
        with open(target, "wb") as save_object:
            pickle.dump(self.source, save_object)

    def save_as_tsv(self, target):
        self.data_frame.to_csv(target, sep="\t", index=False)

