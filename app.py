import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. API 열쇠 꺼내서 제미나이 무기 장착 (LLM 세팅)
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# 웹 화면 타이틀 세팅
st.set_page_config(page_title="샤코 전용 AI 코치", page_icon="💪")
st.title("💪 24만 개 팩트 기반! AI 벌크업 코치")

# 2. 24만 개 한글 뇌(Vector DB) 연결
@st.cache_resource
def load_db():
    ko_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="jhgan/ko-sroberta-multitask")
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_collection(name="nutrition_core", embedding_function=ko_ef)

collection = load_db()

# 3. 대화창 (UI)
user_input = st.text_input("💬 오늘 식단이나 궁금한 음식 물어봐 (예: 닭가슴살 물리는데 단백질 높은 다른 거 추천해줘)")

if st.button("코치에게 물어보기"):
    if user_input:
        with st.spinner("24만 개 DB 스캔 및 분석 중..."):
            
            # (1) 검색기(DB)가 네 질문에 맞는 식품 팩트를 5개 찾아옴
            results = collection.query(
                query_texts=[user_input],
                n_results=5
            )
            
            # (2) 찾아온 팩트를 텍스트로 깔끔하게 정리
            context_data = ""
            for i in range(len(results['documents'][0])):
                name = results['documents'][0][i]
                macros = results['metadatas'][0][i]
                context_data += f"- {name} (칼로리:{macros['kcal']}kcal, 단백질:{macros['protein']}g, 탄수화물:{macros['carbs']}g, 지방:{macros['fat']}g)\n"
            
            # (3) 제미나이한테 팩트 쥐여주고 코칭 지시 (프롬프트 엔지니어링)
            prompt = f"""
            너는 27살, 166cm, 53kg에서 체중을 늘리려고(벌크업) 하는 남자를 돕는 영양 코치야.
            다정한 친형처럼 반말로 대답해주고, 과도하게 걱정하거나 불필요한 잔소리는 절대 하지 마.
            아래 24만 개 영양성분 DB에서 찾은 팩트 데이터만을 무기로 사용자의 질문에 객관적이고 정확하게 답해줘.
            
            [DB 검색 결과 (팩트)]
            {context_data}
            
            [사용자 질문]
            {user_input}
            """
            
            # (4) 제미나이 답변 생성
            response = model.generate_content(prompt)
            
            # 화면에 렌더링
            st.subheader("🤖 AI 코치의 분석 결과")
            st.write(response.text)
            
            # 팩트 체크용 DB 원본 데이터 (접었다 펴기)
            with st.expander("🔍 AI가 참고한 DB 원본 데이터 보기"):
                st.text(context_data)
    else:
        st.warning("질문을 입력해라.")