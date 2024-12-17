import os

def read_fold(in_dir, file_type, callback = lambda x: print(x)):
  for file in os.listdir(in_dir):
      if file.endswith(('.jpg', '.jpeg', '.png')) and file.endswith('1.jpg'):
          in_path = os.path.join(in_dir, file)
          output_path = os.path.join(output_dir, file)
          # 提取结果
          callback(in_path)
          extracted = extract_table(in_path, TableExtractionMode.COLS, slice_obj)
          with open(f"{output_path}.json", "w") as f:
              json.dump(extracted, f, ensure_ascii=False)
          break