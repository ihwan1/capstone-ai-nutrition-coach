import chromadb
from chromadb.utils import embedding_functions

# 1. 아까 DB 넣을 때 썼던 똑같은 한글 번역기 장착
ko_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jhgan/ko-sroberta-multitask")

# 2. AI 금고(Vector DB) 연결
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="nutrition_core", embedding_function=ko_ef)

print("✅ 24만 개 한글 패치 완료! 닭가슴살 헌터 준비 끝.")

while True:
    # 3. 터미널에서 사용자 입력 받기
    search_keyword = input("\n🔎 검색할 식품명 (종료하려면 'exit'): ")
    
    if search_keyword.lower() == 'exit':
        break

    # 4. AI 뇌에서 가장 비슷한 놈 5개 꺼내오기
    results = collection.query(
        query_texts=[search_keyword],
        n_results=5
    )

    print(f"\n--- 🎯 '{search_keyword}' 검색 결과 (Top 5) ---")
    for i in range(len(results['documents'][0])):
        food_name = results['documents'][0][i]
        macros = results['metadatas'][0][i]
        print(f"[{i+1}등] {food_name}")
        print(f"     👉 {macros['kcal']}kcal | 탄:{macros['carbs']}g | 단:{macros['protein']}g | 지:{macros['fat']}g")달