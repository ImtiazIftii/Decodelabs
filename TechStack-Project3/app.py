import sys
from pathlib import Path
# 1. Keep this so the files INSIDE src/ can still import each other
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from src.preprocessor import get_shared_vocabulary
from src.vectorizer import build_tfidf_matrix
from src.recommender import get_trending_fallback,get_recommendations


def display_banner():
    print("\n" + "=" * 75)
    print("     AI TECH STACK & CAREER RECOMMENDER")
    print("     Powered by TF-IDF Vector Mapping & Cosine Similarity")
    print("=" * 75)
    print(" Commands:")
    print("   • Enter at least 3 skills separated by commas (e.g., Python, SQL, AWS)")
    print("   • Type 'skills' to view sample skills from the Shared Vocabulary")
    print("   • Type 'q' or 'exit' to quit")
    print("-" * 75)



def main():
    df,vectorizer,tfidf_matrix = build_tfidf_matrix()
    vocabulary = get_shared_vocabulary(df)

    display_banner()

    while True:
        raw_input = input("\n👉 Enter your skills (or 'skills' / 'q'): ").strip()
        if raw_input.lower() in ["q","quit","exit"]:
            print("\n👋 Exiting Tech Stack Recommender. Good luck on your career journey!\n")
            break

        if raw_input.lower() == "skills":
            print("\n📚 RECOGNIZED SKILLS BY CAREER TRACK:")
            print("-" * 80)
            # Group by domain_category and grab the first row's first 6 skills for each track
            for domain, group in df.groupby("domain_category", sort=False):
                sample_skills = ", ".join(group.iloc[0]["skills"].split(",")[:6])
                print(f"  {domain:<25} | {sample_skills}")
            print("-" * 80)
            continue

        user_skills = [s.strip() for s in raw_input.split(",") if s.strip()]

        if len(user_skills) < 3:
            print(f"⚠️  You entered {len(user_skills)} skill(s). Please provide at least 3 skills separated by commas!")
            continue

        top3 = get_recommendations(user_skills, df, vectorizer, tfidf_matrix)
        print("\n" + "-" * 75)
        if top3 is None or top3.empty:
            print(f" ⚠️  No direct matches found in vocabulary for: {', '.join(user_skills)}")
            print("Top 3 Trending Tech Roles:\n")

        else:
            print(f" 🎯  TOP 3 RECOMMENDED CAREER PATHS FOR: {', '.join(user_skills)}\n")
            for rank, (_, row) in enumerate(top3.iterrows(), start=1):
                matched = row["matched_skills"].replace("_", " ")
                missing = row["missing_skills"].replace("_", " ")
                print(f"   #{rank}  {row['job_role']:<28} — {row['score']*100:5.2f}% Match ({row['domain_category']})")
                print(f"       {'Matched Skills:':<27} {matched}")
                print(f"       {'Next Skills You Can Learn:':<27} {missing}\n")
        print("-" * 75)
if __name__ == "__main__":
    main()