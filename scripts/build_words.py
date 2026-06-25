"""Okt로 원본 문장에서 명사·동사·형용사 형태소 목록을 생성한다."""

import json
from pathlib import Path

from konlpy.tag import Okt


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = REPO_ROOT / "kor_news_2022_100K" / "kor_news_2022_100K-sentences.txt"
OUTPUT_PATH = REPO_ROOT / "data" / "words.json"
CONTENT_TAGS = {"Noun", "Verb", "Adjective"}
BATCH_SIZE = 100


def read_sentences(source_path: Path) -> list[str]:
    """TSV의 두 번째 열에서 문장을 읽고 형식을 검증한다."""
    sentences: list[str] = []
    with source_path.open("r", encoding="utf-8") as source_file:
        for line_number, line in enumerate(source_file, start=1):
            columns = line.rstrip("\n").split("\t", 1)
            if len(columns) != 2:
                raise ValueError(f"{line_number}행: 문장 열을 찾을 수 없습니다.")
            sentences.append(columns[1])
    return sentences


def extract_content_morphemes(sentences: list[str], okt: Okt) -> list[str]:
    """문맥에서 명사·동사·형용사를 기본형으로 추출하고 중복을 제거한다."""
    morphemes: list[str] = []
    seen: set[str] = set()

    for start in range(0, len(sentences), BATCH_SIZE):
        batch = "\n".join(sentences[start : start + BATCH_SIZE])
        for morpheme, tag in okt.pos(batch, norm=True, stem=True):
            has_hangul = any("가" <= character <= "힣" for character in morpheme)
            if tag in CONTENT_TAGS and has_hangul and morpheme not in seen:
                seen.add(morpheme)
                morphemes.append(morpheme)

        processed = min(start + BATCH_SIZE, len(sentences))
        if processed % 5_000 == 0 or processed == len(sentences):
            print(f"형태소 분석: {processed:,}/{len(sentences):,}문장")

    return morphemes


def main() -> int:
    if not SOURCE_PATH.is_file():
        print(f"원본 문장 파일을 찾을 수 없습니다: {SOURCE_PATH}")
        return 1

    try:
        sentences = read_sentences(SOURCE_PATH)
        morphemes = extract_content_morphemes(sentences, Okt())
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as output_file:
            json.dump(morphemes, output_file, ensure_ascii=False, separators=(",", ":"))
            output_file.write("\n")
    except (OSError, UnicodeError, ValueError, RuntimeError) as error:
        print(f"형태소 목록을 생성하지 못했습니다: {error}")
        return 1

    print(f"{len(morphemes):,}개 실질 형태소를 생성했습니다: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    main()
