import os
import json
from pathlib import Path


def load_brief(file_path):
    """브랜드 브리프 JSON 파일을 읽습니다."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


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

    # 브리프 읽기
    try:
        brief = load_brief(brief_path)
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {brief_path}")
        return
    except json.JSONDecodeError:
        print("❌ JSON 형식이 올바르지 않습니다.")
        return

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
