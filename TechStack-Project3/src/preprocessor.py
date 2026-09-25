import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw_skills.csv"

df = pd.read_csv(DATA_PATH)
#print(df.head())

synonym_map = {
    "k8s":"kubernetes",
    "ml":"machine learning",
    "js":"javascript",
    "ts":"typescript",
    "py": "python",
    "frontend": "frontend development",
    "ui": "ui/ux",
    "ux": "ui/ux",
    "cybersecurity": "security",
    "cyber security": "security",
    "infosec": "security",
    "react.js": "react",
    "reactjs": "react",
    "node": "node.js",
    "golang": "go",
    "cpp": "c++",
    "csharp": "c#",
    "postgres": "postgresql",
    "mongo": "nosql",
    "mongodb": "nosql",
    "tf": "tensorflow",
    "sklearn": "scikit-learn",
    "sci-kit learn": "scikit-learn",
    "data science": "data analysis",
    "devops": "ci/cd",
    "web development": "frontend development",
    "web dev": "frontend development",
}

def normalize_skills(skills_input) -> str:
    if isinstance(skills_input,str):
        raw_list = skills_input.split(",")
    elif isinstance(skills_input,list):
        raw_list = skills_input
    else:
        return ""    
                
    cleaned_tokens = []
    for item in raw_list:
        token = item.strip().lower()
        if not token:
            continue

        token = synonym_map.get(token,token)
        token = token.replace(" ","_")
        cleaned_tokens.append(token)

    return " ".join(cleaned_tokens)


def load_and_preprocess_data(csv_path: Path = DATA_PATH) -> pd.DataFrame:

    df = pd.read_csv(csv_path)

    #drop any rows with missing skills
    df = df.dropna(subset=["skills"]).copy()
    df = df[df["skills"].str.strip()!=""]  #save those skills that are not empty

    #Creating normalized skills column for TF-IDF
    df["normalized_skills"] = df["skills"].apply(normalize_skills)
    return df


    
def get_shared_vocabulary(df: pd.DataFrame) -> sorted:
    
    vocab = set()
    for skill_str in df["normalized_skills"]:
        vocab.update(skill_str.split())
    return sorted(vocab)


if __name__ == "__main__":
    catalog_df = load_and_preprocess_data()
    vocabulary = get_shared_vocabulary(catalog_df)

    print(f"Active job roles loaded(Item Cold Start Passed):{len(catalog_df)}")
    print(f"Total Unique Skills in Shared Vocabulary Space: {len(vocabulary)}")
    print(f"\nSample Row 0 ({catalog_df.iloc[0]['job_role']}):")
    print(f"  Raw:    {catalog_df.iloc[0]['skills']}")
    print(f"  Normalized: {catalog_df.iloc[0]['normalized_skills']}")        