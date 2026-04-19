from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import sys

# -----------------------------
# LOAD MODEL
# -----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------
# LOAD RULES
# -----------------------------
with open("rules.txt", "r") as f:
    rules = f.readlines()

rules = [r.strip() for r in rules if r.strip()]

# -----------------------------
# CREATE EMBEDDINGS
# -----------------------------
rule_embeddings = model.encode(rules)

# -----------------------------
# BUILD FAISS INDEX
# -----------------------------
dimension = rule_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(rule_embeddings))

# -----------------------------
# QUERY FUNCTION
# -----------------------------
def get_explanation(query, top_k=3):
    query_embedding = model.encode([query])
    
    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []
    for idx in indices[0]:
        results.append(rules[idx])

    return results

# -----------------------------
# TEST
# -----------------------------
# if __name__ == "__main__":
#     query = "Why is this transaction high risk due to pin and amount?"
#     results = get_explanation(query)

#     print("\n🔍 Explanation:\n")
#     for r in results:
#         print("-", r)

if __name__ == "__main__":
    query = sys.argv[1]  # take input from Java
    results = get_explanation(query)

    for r in results:
        print(r)