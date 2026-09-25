import sklearn
import pandas as pd
from preprocessor import load_and_preprocess_data,normalize_skills 
from scipy.sparse import csr_matrix
from vectorizer import vectorize_user_input,build_tfidf_matrix
from sklearn.metrics.pairwise import cosine_similarity



# I need to take user input and vectorize them
   

def get_recommendations(skills,df,vectorizer,tfidf_matrix):
    #Ingestion
    if len(skills) < 3:
        print("Give 3 skills minimum and try again")
        return None
    vectorized_skills = vectorize_user_input(skills,vectorizer)
    #Scoring the skills using similarity
    scores = cosine_similarity(vectorized_skills,tfidf_matrix)
    scores = scores[0]

    results = df[["job_role","domain_category"]].copy()
    results["score"] = scores
    # Phase 5 Explainability: Show which skills matched and which to learn next
    #Uses the idea of set to first find the intersecting skills and then shows that skill
    #Then it shows the user to skills they can learn by simply doing Total-Intersection
    user_tokens = set(normalize_skills(skills).split())
    results["matched_skills"] = df["normalized_skills"].apply(
        lambda s: ", ".join(sorted(user_tokens.intersection(s.split())))
    )
    results["missing_skills"] = df["normalized_skills"].apply(
        lambda s: ", ".join(sorted(set(s.split()) - user_tokens)[:5]) # Top 5 skills to learn next
    )
    results = results.sort_values(by="score",ascending=False)
    
    results = results[results["score"] > 0]
    top3 = results.head(3)
    return top3


#Sends trending 3 when the values are not on the skill set or is empty
def get_trending_fallback(df) -> pd.DataFrame:
    trend3 = df.sort_values(by = 'popularity_rank')
    trend3 = trend3.head(3)
    return trend3


#always i need this function to test my output
if __name__ == "__main__":
    df, vectorizer, tfidf_matrix = build_tfidf_matrix()

    raw_input = input("Enter 3 skills you are comfortable in (Separate by commas): ")
    test_input = [s.strip() for s in raw_input.split(",") if s.strip()]
    top3 = get_recommendations(test_input, df, vectorizer, tfidf_matrix)

    if top3 is None or top3.empty:
        print(f"\n No direct skill matches found for {test_input}.")
        print(" Showing Top 3 Trending Tech Roles :\n")
        fallback = get_trending_fallback(df)
        for _, row in fallback.iterrows():
            print(f"   #{row['popularity_rank']:<3} {row['job_role']:<28} ({row['domain_category']})")
    else:
        print(f"\n Top Recommendations for: {test_input}\n")
        for _, row in top3.iterrows():
            matched = row["matched_skills"].replace("_", " ")
            missing = row["missing_skills"].replace("_", " ")
            print(f"   {row['job_role']:<28} — {row['score']*100:5.2f}% Match ({row['domain_category']})")
            print(f"     {'Matched Skills:':<27} {matched}")
            print(f"     {'Next Skills You Can Learn:':<27} {missing}\n")