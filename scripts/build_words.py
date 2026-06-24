"""원본 TSV에서 웹페이지용 한글 포함 단어 목록을 생성한다."""

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = REPO_ROOT / "kor_news_2022_100K" / "kor_news_2022_100K-words.txt"
OUTPUT_PATH = REPO_ROOT / "data" / "words.json"


def read_korean_words(source_path: Path) -> list[str]:
    """두 번째 열에 한글 음절이 하나라도 있는 단어만 원본 순서로 반환한다."""
    words: list[str] = []

    with source_path.open("r", encoding="utf-8") as source_file:
        for line_number, line in enumerate(source_file, start=1):
            columns = line.rstrip("\n").split("\t")
            if len(columns) != 3:
                raise ValueError(
                    f"{line_number}행: 탭으로 구분된 열이 3개가 아닙니다."
                )

            word = columns[1]
            if any("가" <= character <= "힣" for character in word):
                words.append(word)

    return words


def main() -> int:
    if not SOURCE_PATH.is_file():
        print(f"원본 단어 파일을 찾을 수 없습니다: {SOURCE_PATH}")
        return 1

    try:
        words = read_korean_words(SOURCE_PATH)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"단어 파일을 처리하지 못했습니다: {error}")
        return 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as output_file:
        json.dump(words, output_file, ensure_ascii=False, separators=(",", ":"))
        output_file.write("\n")

    print(f"{len(words):,}개 단어를 생성했습니다: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    main()
