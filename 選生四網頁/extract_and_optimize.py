# -*- coding: utf-8 -*-
"""
抽取選生四網頁 15 個單元 HTML 中的 base64 圖片至獨立 WebP 靜態檔案，
將原本 9~19 MB 的巨大單檔 HTML 瘦身為 50~150 KB 的極速秒開網頁。
"""
import os, sys, re, json, base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UNITS = [
    ("1-1_遺傳變異對演化的重要性_優化版.html", "1-1"),
    ("1-2_族群遺傳學_優化版.html", "1-2"),
    ("1-3_現代生物演化理論_優化版.html", "1-3"),
    ("1-4_物種的形成與分類_優化版.html", "1-4"),
    ("2-1_生態學的研究層級_優化版.html", "2-1"),
    ("2-2_族群_優化版.html", "2-2"),
    ("2-3_群集_優化版.html", "2-3"),
    ("2-4_生態系_優化版.html", "2-4"),
    ("3-1_生物多樣性的三個層面_優化版.html", "3-1"),
    ("3-2_臺灣的生物多樣性_優化版.html", "3-2"),
    ("3-3_生物多樣性的保育_優化版.html", "3-3"),
    ("探討活動1-1_鐮形血球與天擇_優化版.html", "lab1-1"),
    ("探討活動2-1_頂級掠食者消失對群集結構的影響_優化版.html", "lab2-1"),
    ("探討活動2-2_生態球製作_優化版.html", "lab2-2"),
    ("探討活動3-1_櫻花鉤吻鮭的復育之路_優化版.html", "lab3-1"),
]

def sanitize_filename(name):
    return re.sub(r'[^\w\.\-]', '_', name)

def get_ext_from_header(header):
    if "png" in header: return ".png"
    if "jpeg" in header or "jpg" in header: return ".jpg"
    if "gif" in header: return ".gif"
    if "svg" in header: return ".svg"
    return ".webp"

def process_unit(filename, slug):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"[SKIP] {filepath} not found")
        return

    orig_size = os.path.getsize(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    assets_dir = os.path.join(BASE_DIR, "assets", slug, "assets")
    slides_dir = os.path.join(BASE_DIR, "assets", slug, "slides")
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(slides_dir, exist_ok=True)

    m_assets = re.search(r"const\s+ASSETS\s*=\s*(\{.*?\});", content, re.DOTALL)
    m_slides = re.search(r"const\s+SLIDES\s*=\s*(\{.*?\});", content, re.DOTALL)

    new_assets = {}
    saved_assets_count = 0
    if m_assets:
        raw_assets = json.loads(m_assets.group(1))
        for k, v in raw_assets.items():
            if isinstance(v, str) and v.startswith("data:image/"):
                header, b64 = v.split(",", 1)
                ext = get_ext_from_header(header)
                # If k already has extension
                lower_k = k.lower()
                if lower_k.endswith((".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg")):
                    img_name = sanitize_filename(k)
                else:
                    img_name = f"{sanitize_filename(k)}{ext}"
                target_path = os.path.join(assets_dir, img_name)
                with open(target_path, "wb") as img_f:
                    img_f.write(base64.b64decode(b64))
                new_assets[k] = f"assets/{slug}/assets/{img_name}"
                saved_assets_count += 1
            else:
                new_assets[k] = v

    new_slides = {}
    saved_slides_count = 0
    if m_slides:
        raw_slides = json.loads(m_slides.group(1))
        for slide_no, steps in raw_slides.items():
            new_steps = []
            for step_idx, step_data in enumerate(steps, 1):
                if isinstance(step_data, str) and step_data.startswith("data:image/"):
                    header, b64 = step_data.split(",", 1)
                    ext = get_ext_from_header(header)
                    try:
                        s_int = int(slide_no)
                        slide_prefix = f"s{s_int:02d}"
                    except ValueError:
                        slide_prefix = f"s_{sanitize_filename(str(slide_no))}"
                    img_name = f"{slide_prefix}_{step_idx}{ext}"
                    target_path = os.path.join(slides_dir, img_name)
                    with open(target_path, "wb") as img_f:
                        img_f.write(base64.b64decode(b64))
                    new_steps.append(f"assets/{slug}/slides/{img_name}")
                    saved_slides_count += 1
                else:
                    new_steps.append(step_data)
            new_slides[slide_no] = new_steps

    # Replace in content safely by string slices
    # Notice we must do the replacement from right to left (later index first) so offsets remain valid
    replacements = []
    if m_assets:
        replacements.append((m_assets.start(), m_assets.end(), f"const ASSETS = {json.dumps(new_assets, ensure_ascii=False, indent=2)};"))
    if m_slides:
        replacements.append((m_slides.start(), m_slides.end(), f"const SLIDES = {json.dumps(new_slides, ensure_ascii=False, indent=2)};"))

    replacements.sort(key=lambda x: x[0], reverse=True)
    new_content = content
    for start, end, rep in replacements:
        new_content = new_content[:start] + rep + new_content[end:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    new_size = os.path.getsize(filepath)
    reduction = (1 - new_size / orig_size) * 100
    print(f"[{slug}] {orig_size/1024/1024:.2f} MB -> {new_size/1024:.1f} KB (節省 {reduction:.1f}%) | 圖片: assets={saved_assets_count}, slides={saved_slides_count}")

def main():
    print("=== 開始選修生物4 小節網頁瘦身優化 ===")
    for filename, slug in UNITS:
        process_unit(filename, slug)
    print("=== 全部優化完成 ===")

if __name__ == "__main__":
    main()
