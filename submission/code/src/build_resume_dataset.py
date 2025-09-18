import os, json
from pathlib import Path
from parse_resumes import parse_resume_file

def build_dataset(input_dir="data/resumes", output_dir="data/parsed_resumes"):
    os.makedirs(output_dir, exist_ok=True)

    for file in Path(input_dir).glob("*"):
        if file.suffix.lower() not in [".pdf", ".docx", ".txt"]:
            continue
        print(f"Parsing {file.name}...")
        parsed = parse_resume_file(str(file))
        out_path = Path(output_dir) / (file.stem + ".json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)
    print("✅ Dataset built successfully!")

if __name__ == "__main__":
    build_dataset()
