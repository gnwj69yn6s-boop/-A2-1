import os
import json
from pathlib import Path

from openai import OpenAI



def load_brief(file_path):
    """브랜드 브리프 JSON 파일을 읽습니다."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
def generate_slogans(client, brief, brand_name):
    """브랜드 슬로건 3개를 생성합니다."""

    prompt = f"""
당신은 전문 브랜드 카피라이터입니다.

다음 브랜드 정보를 바탕으로 슬로건을 만들어주세요.

브랜드명: {brand_name}
업종: {brief["industry"]}
타겟: {brief["target"]}
키워드: {", ".join(brief["keywords"])}
톤앤매너: {brief.get("tone", "")}
추가 요청사항: {brief.get("notes", "")}

조건:
- 슬로건은 정확히 3개
- 짧고 기억하기 쉬운 문장
- 브랜드의 핵심 가치를 표현
- 타겟 고객에게 자연스럽게 전달
- 광고 문구처럼 과장하지 않기

반드시 다음 JSON 형식으로만 답변하세요.

{{
    "slogans": [
        "슬로건 1",
        "슬로건 2",
        "슬로건 3"
    ]
}}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    result = response.output_text.strip()

    if result.startswith("```"):
        result = result.replace("```json", "", 1)
        result = result.replace("```", "")
        result = result.strip()

    return json.loads(result)


def main():
    print()
    print("🎨 AI 브랜드 아이덴티티 생성기")
    print()

    # 브리프 파일 경로 입력
    brief_path = input(
        "브리프 파일 경로를 입력하세요: "
    ).strip()

    # 출력 폴더 입력
    output_path = input(
        "출력 폴더 경로를 입력하세요 (엔터 시 ./output): "
    ).strip()

    if not output_path:
        output_path = "./output"

    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
    return

client = OpenAI(api_key=api_key)

    # 브리프 읽기
    try:
        brief = load_brief(brief_path)
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {brief_path}")
        return
    except json.JSONDecodeError:
        print("❌ JSON 형식이 올바르지 않습니다.")
        return
print()
print("[2/5] 슬로건 생성 중...")

try:
    # 첫 번째 브랜드명을 대표 브랜드명으로 사용
    brand_name = naming_result["names"][0]["name"]

    slogan_result = generate_slogans(
        client,
        brief,
        brand_name
    )

    for slogan in slogan_result["slogans"]:
        print(f'  - "{slogan}"')

except Exception as e:
    print(f"❌ 슬로건 생성 실패: {e}")

    # 필수 항목 확인
    required_fields = [
        "industry",
        "target",
        "keywords"
    ]

    for field in required_fields:
        if field not in brief:
            print(f"❌ 필수 항목이 없습니다: {field}")
            return

    print()
    print("✅ 브랜드 브리프를 정상적으로 읽었습니다.")
    print()
    print(f"업종: {brief['industry']}")
    print(f"타겟: {brief['target']}")
    print(f"키워드: {', '.join(brief['keywords'])}")

    print()
    print("다음 단계에서 AI 브랜드 요소를 생성합니다.")


if __name__ == "__main__":
    main()
