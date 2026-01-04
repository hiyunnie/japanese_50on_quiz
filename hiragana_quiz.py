import random
import time
import sys
import os

# 判斷是否被打包成 exe
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)  # exe 所在資料夾
else:
    base_path = os.path.dirname(__file__)       # 正常執行 Python

words_file = os.path.join(base_path, 'words.txt')

# 讀取單字
def load_words(file_path):
    words = []
    if not os.path.exists(file_path):
        print(f"找不到單字檔: {file_path}")
        return words
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue
            kanji, hiragana, romaji, meaning = parts
            words.append({
                "kanji": kanji,
                "hiragana": hiragana,
                "romaji": romaji.lower(),
                "meaning": meaning
            })
    return words

# 前五題：羅馬拼音 → 選平假名
def ask_question_romaji(word):
    correct = word['hiragana']
    options = [correct]

    # 產生 3 個類似的干擾選項
    while len(options) < 4:
        chars = list(correct)
        idx = random.randint(0, len(chars)-1)
        fake_char = random.choice(list(
            "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
        ))
        if fake_char != chars[idx]:
            chars[idx] = fake_char
        fake_option = "".join(chars)
        if fake_option not in options:
            options.append(fake_option)

    random.shuffle(options)

    print(f"\n題: 請選出平假名 (意思: {word['meaning']}, romaji: {word['romaji']})")
    for i, c in enumerate(options):
        print(f"{i+1}) {c}", end="  ")
    print()
    try:
        choice = int(input("你的答案編號: ").strip())
        if options[choice-1] == correct:
            print("✅ 正確")
            return True
        else:
            print(f"❌ 錯誤，正確答案是: {correct}")
            return False
    except:
        print(f"❌ 輸入錯誤，正確答案是: {correct}")
        return False

# 後五題：平假名 → 輸入羅馬拼音
def ask_question_hiragana(word):
    print(f"\n題: 請輸入單詞羅馬拼音 (意思: {word['meaning']}, 日文提示: {word['hiragana']})")
    answer = input("你的答案: ").strip().lower()
    if answer == word['romaji']:
        print("✅ 正確")
        return True
    else:
        print(f"❌ 錯誤，正確答案是: {word['romaji']}")
        return False

def main():
    words = load_words(words_file)
    if not words:
        print("單字列表為空或讀取失敗")
        input("按 Enter 鍵結束...")
        return

    selected = random.sample(words, 10)
    correct_count = 0
    start_time = time.time()  # 開始計時

    # 前五題
    for word in selected[:5]:
        if ask_question_romaji(word):
            correct_count +=1

    # 後五題
    for word in selected[5:]:
        if ask_question_hiragana(word):
            correct_count +=1
    
    end_time = time.time()  # 結束計時
    elapsed = end_time - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    print(f"\n作答總時長: {minutes} 分 {seconds} 秒")
    print(f"測驗結束！你答對 {correct_count} 題 / 10 題")
    input("按 Enter 鍵結束...")

if __name__ == "__main__":
    main()
