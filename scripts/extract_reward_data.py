"""Extract the 2025 Japan Federation reward survey into app data.

The source PDF is intentionally processed at build/update time. The deployed app
never downloads or scrapes the PDF at runtime.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber


HEADER_RE = re.compile(
    r"^([0-9]{1,3})(.*?)\s*<(?:前回：([0-9]+)|新規)>\s*$"
)
NUMBER_RE = re.compile(r"-|[0-9][0-9,]*(?:\.[0-9]+)?")
MONEY_LABEL_RE = re.compile(r"[0-9.]+(?:千|万)?円(?:以上)?")


def to_number(token: str) -> int:
    if token == "-":
        return 0
    return round(float(token.replace(",", "")))


def category_for(number: int, name: str) -> str:
    """Assign practical search categories while retaining the official number."""
    rules = (
        ("建設・宅建", ("建設", "宅地建物", "建築士", "測量", "解体工事")),
        ("土地・農地", ("農地", "土地改良", "開発行為", "都市計画", "河川", "道路", "公有地")),
        ("営業許可", ("営業許可", "風俗営業", "古物", "質屋", "旅館", "食品", "酒類", "たばこ", "理容", "美容", "クリーニング")),
        ("運輸・自動車", ("自動車", "運送", "運輸", "車庫", "軽車両", "小型船舶", "漁船", "遊漁船", "倉庫", "航空機", "ドローン", "回送運行")),
        ("国際・入管", ("在留", "帰化", "国籍", "外国人", "旅券", "査証", "難民", "国際", "英文", "外国語", "貿易")),
        ("法人・組合", ("会社", "法人", "組合", "定款", "議事録", "事業協同", "宗教", "学校", "医療", "社会福祉", "NPO")),
        ("相続・遺言", ("相続", "遺言", "遺産", "遺留分", "成年後見", "死後事務", "家系図")),
        ("契約・民事", ("契約書", "内容証明", "示談", "協議書", "公正証書", "離婚", "告訴", "告発", "請願", "陳情", "事実証明")),
        ("知財・著作権", ("著作権", "知的財産", "知的資産", "種苗", "品種登録", "回路配置")),
        ("環境・廃棄物", ("廃棄物", "産業廃棄", "環境", "公害", "リサイクル", "浄化槽")),
        ("労務・社会保険", ("労働", "就業規則", "社会保険", "年金", "雇用保険", "健康保険", "労災", "派遣", "職業紹介", "給与計算")),
        ("補助金・融資", ("補助金", "助成金", "融資", "経営革新", "経営改善", "事業承継", "資金")),
    )
    for category, keywords in rules:
        if any(keyword in name for keyword in keywords):
            return category

    # The official list is ordered broadly by field; these ranges catch items
    # whose names do not contain a distinctive keyword.
    if number <= 35:
        return "建設・宅建"
    if number <= 73:
        return "土地・農地"
    if number <= 118:
        return "営業許可"
    if number <= 172:
        return "運輸・自動車"
    if number <= 236:
        return "法人・組合"
    if number <= 284:
        return "国際・入管"
    if number <= 344:
        return "契約・民事"
    if number <= 410:
        return "労務・社会保険"
    if number <= 455:
        return "環境・廃棄物"
    return "その他・経営支援"


def band_labels(threshold_line: str, count: int) -> list[str]:
    thresholds = MONEY_LABEL_RE.findall(threshold_line)
    if not thresholds or count <= 0:
        return [f"金額帯{i + 1}" for i in range(count)]
    values = [x.removesuffix("以上") for x in thresholds]
    labels = [f"{values[0]}未満"]
    labels.extend(f"{values[i - 1]}～{values[i]}未満" for i in range(1, len(values)))
    labels.append(f"{values[-1]}以上")
    if len(labels) != count:
        return [f"金額帯{i + 1}" for i in range(count)]
    return labels


def extract(pdf_path: Path) -> list[dict]:
    with pdfplumber.open(pdf_path) as pdf:
        lines = []
        for page in pdf.pages:
            lines.extend(line.strip() for line in (page.extract_text() or "").splitlines())

    headers: list[tuple[int, re.Match[str]]] = []
    for index, line in enumerate(lines):
        match = HEADER_RE.match(line)
        if match:
            headers.append((index, match))

    if len(headers) != 487:
        raise ValueError(f"Expected 487 service headers, found {len(headers)}")

    services: list[dict] = []
    for position, (start, header) in enumerate(headers):
        end = headers[position + 1][0] if position + 1 < len(headers) else len(lines)
        block = lines[start + 1 : end]
        number = int(header.group(1))
        name = re.sub(r"\s+", " ", header.group(2)).strip()

        percentage_line = next((line for line in block if line.startswith("100.0%")), "")
        percentages = [float(value) for value in re.findall(r"([0-9]+(?:\.[0-9]+)?)%", percentage_line)]
        rates = percentages[1:]
        mode_count_match = re.search(r"([0-9,]+)件\s*$", percentage_line)
        mode_count = to_number(mode_count_match.group(1)) if mode_count_match else 0

        candidates: list[list[str]] = []
        for line in block:
            if any(marker in line for marker in ("円", "%", "回答者", "平均", "最小値", "最大値", "最頻値")):
                continue
            tokens = NUMBER_RE.findall(line)
            if tokens and re.match(r"^[0-9]", line):
                candidates.append(tokens)
        if not candidates:
            raise ValueError(f"No numeric row for service {number}: {name}")
        row = max(candidates, key=len)

        if rates:
            band_count = len(rates)
        else:
            # Zero-response records have no percentage row. Four trailing
            # values are average/min/max/mode and the first is respondents.
            band_count = max(len(row) - 5, 0)
            rates = [0.0] * band_count

        stats_at = 1 + band_count
        if len(row) < stats_at + 4:
            raise ValueError(
                f"Malformed numeric row for service {number}: expected at least "
                f"{stats_at + 4} values, got {len(row)} ({row})"
            )

        respondents = to_number(row[0])
        band_counts = [to_number(value) for value in row[1:stats_at]]
        if sum(band_counts) != respondents:
            raise ValueError(
                f"Band counts do not sum to respondents for service {number}: "
                f"{sum(band_counts)} != {respondents}"
            )
        average, minimum, maximum = map(to_number, row[stats_at : stats_at + 3])
        wrapped_modes = [
            to_number(candidate[0])
            for candidate in candidates
            if candidate is not row and len(candidate) == 1 and candidate[0] != "-"
        ]
        mode_values = wrapped_modes + [
            to_number(value) for value in row[stats_at + 3 :] if value != "-"
        ]
        mode_values = list(dict.fromkeys(value for value in mode_values if value > 0))
        mode = mode_values[0] if mode_values else None
        if respondents and not (minimum <= average <= maximum):
            raise ValueError(
                f"Average is outside min/max for service {number}: "
                f"{minimum} <= {average} <= {maximum}"
            )
        if percentages and abs(sum(rates) - 100) > 0.6:
            raise ValueError(
                f"Percentages do not sum to 100 for service {number}: {sum(rates)}"
            )
        threshold_line = next((line for line in block if "以上" in line and "円" in line), "")
        labels = band_labels(threshold_line, band_count)

        services.append(
            {
                "id": f"official-{number}",
                "officialNumber": number,
                "previousNumber": int(header.group(3)) if header.group(3) else None,
                "isNew": header.group(3) is None,
                "name": name,
                "category": category_for(number, name),
                "respondents": respondents,
                "average": average,
                "mode": mode,
                "modes": mode_values,
                "modeCount": mode_count or None,
                "min": minimum,
                "max": maximum,
                "restricted": "※" in name,
                "bands": [
                    {"label": label, "rate": rate}
                    for label, rate in zip(labels, rates, strict=True)
                ],
            }
        )

    numbers = [service["officialNumber"] for service in services]
    if numbers != list(range(1, 488)):
        raise ValueError("Official numbers are not the continuous range 1..487")
    return services


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    services = extract(args.pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(services, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Wrote {len(services)} services to {args.output}")


if __name__ == "__main__":
    main()
