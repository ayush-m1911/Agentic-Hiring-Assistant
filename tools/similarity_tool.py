from sklearn.metrics.pairwise import cosine_similarity
from tools.embedding_tool import get_embedding

def calculate_similarity(text1, text2):
    emb1 = get_embedding(text1).reshape(1, -1)
    emb2 = get_embedding(text2).reshape(1, -1)
    score = cosine_similarity(emb1, emb2)[0][0]
    return round(score * 100, 2)
