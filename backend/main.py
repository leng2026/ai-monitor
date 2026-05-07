from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_deepseek_client():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("API key 未设置")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/monitor")
async def monitor(data: dict):
    brand = data.get("brand", "").strip()
    if not brand:
        return {"error": "品牌名不能为空"}

    prompt = f"""请分析品牌「{brand}」在各大中文内容平台（如DeepSeek、豆包、Kimi、文心一言等）上的提及热度。
仅返回一个严格的 JSON 对象，格式如下，不要包含其他文字：
{{
  "brand": "{brand}",
  "status": "热门" | "正常" | "冷淡",
  "platforms": {{
    "DeepSeek": true/false,
    "豆包": true/false,
    "Kimi": true/false,
    "文心一言": true/false
    
  }},
  "summary": "一句话总结"
}}
根据你的知识合理填充。"""

    try:
        client = get_deepseek_client()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw = response.choices[0].message.content.strip()
        # 清理可能包裹的 markdown 代码块
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1]
            if raw.endswith("```"):
                raw = raw[:-4]
        info = json.loads(raw)
        return info
    except Exception as e:
        return {"error": str(e)}

@app.post("/generate")
async def generate(data: dict):
    prompt = data.get("prompt", "")
    try:
        client = get_deepseek_client()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"content": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
