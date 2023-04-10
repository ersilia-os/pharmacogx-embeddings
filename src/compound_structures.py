
class CompoundStructureEmbedding(object):
    def __init__(self, embedding_type="ersilia"):
        assert embedding_type in self.available()

    def available(self):
        return ["ersilia", "signaturizer"]

    def get(self):
        pass