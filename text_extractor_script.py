import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import sys
import cv2
import easyocr

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Выберите папку с кадрами")
    root.destroy()
    return folder

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Выберите файл для сохранения",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    root.destroy()
    return file_path

def show_message(title, message, is_error=False):
    root = tk.Tk()
    root.withdraw()
    if is_error:
        messagebox.showerror(title, message)
    else:
        messagebox.showinfo(title, message)
    root.destroy()

def get_image_paths(image_folder):
    exts = ('.jpg', '.jpeg', '.png', '.bmp')
    paths = [p for p in Path(image_folder).iterdir() if p.suffix.lower() in exts]
    return sorted(paths)

def process_images(image_folder, lang='ru'):
    reader = easyocr.Reader([lang], gpu=False, verbose=False)
    image_paths = get_image_paths(image_folder)
    if not image_paths:
        show_message("Ошибка", "В папке не найдены изображения", True)
        return []

    results = []
    last_text = ""
    start_frame = 0

    for idx, img_path in enumerate(image_paths):
        img = cv2.imread(str(img_path))
        if img is None:
            continue

        h = img.shape[0]
        roi = img[int(h * 0.7):h, :]

        # Убран paragraph=True, который ломает структуру в некоторых версиях
        res = reader.readtext(roi, detail=1)
        texts = []
        for item in res:
            # Безопасная проверка: (bbox, text, confidence)
            if len(item) >= 3 and item[2] > 0.6:
                texts.append(item[1])
        current_text = " ".join(texts).strip()

        if current_text != last_text:
            if last_text:
                results.append((start_frame, idx - 1, last_text))
            start_frame = idx
            last_text = current_text

    if last_text:
        results.append((start_frame, len(image_paths) - 1, last_text))

    return results

    return results
def save_results(results, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for s, e, txt in results:
            f.write(f"[Кадр {s} - {e}] {txt}\n")

def main():
    args = sys.argv[1:]
    if not args:
        print("Использование:")
        print("  python ocr_extractor.py -path <папка_с_кадрами> [выходной_файл.txt]")
        print("  python ocr_extractor.py -ui")
        return

    flag = args[0]
    if flag == "-ui":
        image_folder = select_folder()
        if not image_folder:
            return
        output_file = select_file()
        if not output_file:
            return
    elif flag == "-path":
        if len(args) != 3:
            print("Ошибка: неверное количество аргументов после -path")
            return
        image_folder = args[1]
        if not os.path.isdir(image_folder):
            image_folder = select_folder()
            if not image_folder:
                return
        output_file = args[2]
        if not output_file:
            return

    print("Запуск распознавания...")
    results = process_images(image_folder)
    if not results:
        show_message("Результат", "Текст не найден")
        return

    save_results(results, output_file)
    if flag == "-ui":   
        show_message("Готово", f"Результат сохранён в:\n{output_file}")
    print(f"Готово. Сохранено в {output_file}")

if __name__ == "__main__":
    main()
