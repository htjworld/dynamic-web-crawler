import os
import json
import csv
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import subprocess

def save_data_to_file(data):
    """사용자가 선택한 포맷에 따라 데이터를 저장"""
    # 파일 형식 선택
    filetypes = [("JSON files", "*.json"), ("JSONL files", "*.jsonl"), ("CSV files", "*.csv"), ("All files", "*.*")]
    save_path = filedialog.asksaveasfilename(
        title="Select File to Save (Formats: JSON, JSONL, CSV)",
        defaultextension=".json",
        filetypes=filetypes
    )
    if not save_path:
        messagebox.showwarning("No File Selected", "No file selected. Data was not saved.")
        return

    try:
        # 파일 확장자에 따라 저장 형식 결정
        if save_path.endswith(".json"):
            save_as_json(data, save_path)
        elif save_path.endswith(".jsonl"):
            save_as_jsonl(data, save_path)
        elif save_path.endswith(".csv"):
            save_as_csv(data, save_path)
        else:
            messagebox.showerror("Unsupported Format", "Unsupported file format selected.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def save_as_json(data, save_path):
    """JSON 포맷으로 저장"""
    with open(save_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    messagebox.showinfo("Success", f"Data successfully saved as JSON to {save_path}")

def save_as_jsonl(data, save_path):
    """JSONL 포맷으로 저장"""
    with open(save_path, "w", encoding="utf-8") as file:
        for record in data:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
    messagebox.showinfo("Success", f"Data successfully saved as JSONL to {save_path}")

def save_as_csv(data, save_path):
    """CSV 포맷으로 저장"""
    import csv
    with open(save_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    messagebox.showinfo("Success", f"Data successfully saved as CSV to {save_path}")

# json 파일 불러오기
def load_json_data(entry_widget):
    """JSON 또는 JSONL 파일을 불러와 해당 Entry 필드에 데이터 입력"""
    file_path = filedialog.askopenfilename(
        title="Select JSON or JSONL File",
        filetypes=[("JSON files", "*.json"), ("JSONL files", "*.jsonl"), ("All files", "*.*")]
    )

    if not file_path:
        return  # 사용자가 파일을 선택하지 않음

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # 확장자에 따라 JSON 또는 JSONL 처리
            if file_path.endswith(".json"):
                data = json.load(file)
            elif file_path.endswith(".jsonl"):
                data = [json.loads(line) for line in file]
            else:
                messagebox.showerror("Error", "Unsupported file format.")
                return

            # 데이터가 리스트 형식인지 확인
            if not isinstance(data, list):
                messagebox.showerror("Error", "Invalid file format. Data should be a list.")
                return
            
            # 리스트 내부 값이 딕셔너리인지 확인 후 Value 값만 추출
            processed_data = []
            for item in data:
                if isinstance(item, dict):
                    processed_data.append(list(item.values()))  # Value 값만 추출
                else:
                    messagebox.showerror("Error", "Invalid data format inside the list.")
                    return

            # JSON 데이터를 Entry 필드에 입력 (문자열 변환)
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, json.dumps(processed_data, ensure_ascii=False))
            messagebox.showinfo("Success", "File loaded successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")