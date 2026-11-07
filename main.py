import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import translators
import random
import time

# --- Красивости для консоли ---
def print_header():
    print("\n" + "="*50)
    print("🎮 ГОЛОСОВОЙ ТЕСТЕР: НАЗОВИ ПО‑АНГЛИЙСКИ")
    print("="*50 + "\n")

def print_progress(current, total):
    percent = int((current / total) * 100)
    bar = "█" * (percent // 5) + "-" * (20 - percent // 5)
    print(f"[{bar}] {percent}% ({current}/{total})")


word_pairs = {
    "кот": "cat", "собака": "dog", "яблоко": "apple", "молоко": "milk", "солнце": "sun",
    "банан": "banana", "школа": "school", "друг": "friend", "окно": "window", "жёлтый": "yellow",
    "машина": "car", "город": "city", "книга": "book", "ручка": "pen", "чашка": "cup",
    "технология": "technology", "университет": "university", "информация": "information",
    "произношение": "pronunciation", "воображение": "imagination", "исследование": "research",
    "разработка": "development", "архитектура": "architecture", "коммуникация": "communication",
    "перспектива": "perspective", "инновация": "innovation", "стратегия": "strategy",
    "репутация": "reputation", "адаптация": "adaptation", "интеграция": "integration"
}

words_by_level = {
    "es": [
        "кот", "собака", "яблоко", "молоко", "солнце"
    ],
    "md": [
        "банан", "школа", "друг", "окно", "жёлтый",
        "машина", "город", "книга", "ручка", "чашка"
    ],
    "hd": [
        "технология", "университет", "информация", "произношение", "воображение",
        "исследование", "разработка", "архитектура", "коммуникация", "перспектива",
        "инновация", "стратегия", "репутация", "адаптация", "интеграция"
    ]
}

print_header()
what = input('Выбери уровень сложности:\n  es — лёгкий (5 слов)\n  md — средний (10 слов)\n  hd — сложный (15 слов)\nТвой выбор: ').lower()

if what not in ['es', 'md', 'hd']:
    print("❌ Такого уровня нет. Запускай заново!")
    exit()

words_list = words_by_level[what]
total_rounds = len(words_list)
correct_count = 0

print(f"\n✅ Уровень выбран: {what}. Всего раундов: {total_rounds}")
time.sleep(1)

for i in range(total_rounds):
    word_ru = random.choice(words_list)      
    correct_en = word_pairs[word_ru]         
    
    print("\n" + "-"*30)
    print(f"Раунд {i+1}/{total_rounds}")
    print(f"💡 Назови по‑английски: {word_ru}")
    print("-"*30)

    duration = 5
    sample_rate = 44100

    print("🗣 Скажи английское слово (5 секунд)...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    print("✅ Запись завершена, распознаём...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        # Распознаём АНГЛИЙСКУЮ речь
        spoken_text_en = recognizer.recognize_google(audio, language="en-US")
        print(f"👂 Ты сказал: {spoken_text_en}")

        back_translation = translators.translate_text(
            spoken_text_en,
            from_language="en",
            to_language="ru",
            translator="bing"
        )
        print(f"🌍 Обратно на русский (для наглядности): {back_translation}")


        if spoken_text_en.lower().strip() == correct_en.lower():
            print("🎉 Молодец! Правильно!")
            correct_count += 1
        else:
            print(f"❌ Неправильно. Правильный вариант: {correct_en}")

    except sr.UnknownValueError:
        print("🔇 Не удалось распознать речь. Попробуй говорить чётче и громче.")
    except sr.RequestError as e:
        print(f"⚠️ Ошибка сервиса распознавания: {e}")
    except Exception as e:
        print(f"⚠️ Произошла ошибка: {e}")

    # Показываем прогресс
    print_progress(i + 1, total_rounds)
    time.sleep(1)

# --- Финал и статистика ---
print("\n" + "="*50)
print("🏆 ИТОГИ:")
print(f"   Всего раундов: {total_rounds}")
print(f"   Правильно: {correct_count}")
percent_success = (correct_count / total_rounds) * 100
print(f"   Процент успеха: {percent_success:.1f}%")

if percent_success == 100:
    print("🌟 Идеально! Ты прошёл все раунды без ошибок!")
elif percent_success > 50:
    print("👍 Хороший результат!")
else:
    print("😕 Не расстраивайся — потренируйся ещё!")
print("="*50 + "\n")
