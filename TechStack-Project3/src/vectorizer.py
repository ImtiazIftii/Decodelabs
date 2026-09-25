import sklearn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from preprocessor import load_and_preprocess_data,normalize_skills 
from scipy.sparse import csr_matrix

#This matrix turns my skillset and roles row column into a matrix with values and weights based on the tfid algorithm
def build_tfidf_matrix() -> tuple[pd.DataFrame,TfidfVectorizer,csr_matrix]:
    tf = TfidfVectorizer(tokenizer=str.split,token_pattern=None)
    df = load_and_preprocess_data()
    tfidf_matrix = tf.fit_transform(df["normalized_skills"])
    return df,tf,tfidf_matrix


def vectorize_user_input(user_skills,fitted_vectorizer) -> csr_matrix:
    normalized_string = normalize_skills(user_skills)
    #only fitting not transforming on the user input
    #transform works only on list and not string so we sent "[normalized-string]"
    user_vector = fitted_vectorizer.transform([normalized_string]) #this converts the string into a vector
    return user_vector


if __name__ == "__main__":
    df,tf,tfidf_matrix = build_tfidf_matrix()

    print(f"Matrix Shape: {tfidf_matrix.shape}")

    print("\nIDF Weight Inspection:")
    test_words = ["git","python","kubernetes","figma"]
    for word in test_words:
        if word in tf.vocabulary_: #if the word is already learned
            col_index = tf.vocabulary_[word]
            idf_weight = tf.idf_[col_index]
            print(f"   {word:20s} → IDF: {idf_weight:.4f}")
        else:
            print(f"   {word:20s} → NOT FOUND in vocabulary!")

    #Testing user vector
    test_input = ["Python","Cloud","Automation"]
    user_vector = vectorize_user_input(test_input,tf)
    print(f"\nUser Input: {test_input}")
    print(f"   User Vector Shape: {user_vector.shape}")
    print(f"   User Vector Sum:   {user_vector.sum():.4f}")

    if user_vector.shape[1] == tfidf_matrix.shape[1] and user_vector.sum() > 0:
        print("Equal dimensions and no zero vector")
    else:
        print("Wrong, fix vectorizer")    

