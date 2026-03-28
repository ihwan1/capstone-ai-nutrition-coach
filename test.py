import google.generativeai as genai
import os
from dotenv import load_dotenv

# 열쇠 장착
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

print("🔥 내 열쇠로 쓸 수 있는 구글 AI 모델 리스트 🔥")
print("-" * 40)

# 쓸 수 있는 모델 이름 다 가져와서 출력
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        
print("-" * 40)