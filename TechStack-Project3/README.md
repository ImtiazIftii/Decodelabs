===============================================================================
DECODELABS INDUSTRIAL TRAINING KIT (BATCH 2026)
PROJECT 3: AI RECOMMENDATION LOGIC — TECH STACK & CAREER RECOMMENDER
===============================================================================

1. PROJECT OVERVIEW
-------------------------------------------------------------------------------
This project implements a commercial-grade Content-Based Recommendation Engine
("The Digital Matchmaker") designed to cure Choice Overload by mapping a user's
technical skills to the most relevant software engineering and AI career paths.

Instead of relying on simple binary tag overlap (1s and 0s / Jaccard Similarity)
or magnitude-sensitive Euclidean distance, this engine uses Term Frequency-
Inverse Document Frequency (TF-IDF) vector mapping paired with multidimensional
Cosine Similarity. It follows a strict Input-Process-Output (IPO) architecture
and executes the 4-Step Ranking Pipeline with built-in Cold Start safeguards
and Explainable AI (XAI) skill-gap analysis.


2. SYSTEM ARCHITECTURE & FILE STRUCTURE
-------------------------------------------------------------------------------
The codebase is engineered using Separation of Concerns, isolating the data
layer, mathematical processing engine, and user interface:

TechStack-Project3/
│
├── data/
│   └── raw_skills.csv        # Canonical catalog of 20 Tech Roles, 118 unique
│                             # skills, domain categories, and popularity ranks
├── src/
│   ├── preprocessor.py       # Phase 1: Dynamic pathlib loader, Item Cold Start
│   │                         # audit, Synonym Mapper, and Shared Vocabulary
│   ├── vectorizer.py         # Phase 2: TF-IDF matrix builder (.fit_transform)
│   │                         # and user input vector mapper (.transform)
│   └── recommender.py        # Phase 3 & 4: 4-Step Ranking Pipeline (Ingestion,
│                             # Scoring, Sorting, Filtering) + Cold Start Fallback
│
├── app.py                    # Phase 5: Interactive CLI application loop with
│                             # Domain-grouped skill directory & XAI output
└── README.txt                # Project documentation and engineering notes


3. HOW THE ENGINE WORKS (THE 4-STEP RANKING PIPELINE)
-------------------------------------------------------------------------------
Step 1: INGESTION (Capturing User State)
  - Accepts user skill inputs and enforces a minimum requirement of 3 skills
    (Onboarding Survey bypass) to guarantee sufficient vector density.
  - Normalizes user tokens via preprocessor.py: lowercases, strips whitespace,
    maps common slang/abbreviations via SYNONYM_MAP (e.g., "k8s" -> "kubernetes",
    "cybersec" -> "security"), and glues multi-word skills with underscores
    (e.g., "cloud computing" -> "cloud_computing") so TF-IDF treats each
    compound skill as a single mathematical dimension.

Step 2: SCORING (TF-IDF & Cosine Similarity Math)
  - Projects the user's normalized skills into the pre-fitted 118-dimensional
    TF-IDF space using .transform() (preserving catalog IDF weights).
  - Computes Cosine Similarity between the (1, 118) user vector and the
    (20, 118) CSR sparse catalog matrix, measuring angular alignment between
    0.0 (orthogonal / unrelated) and 1.0 (identical orientation).

Step 3: SORTING (Descending Rank Organization)
  - Pairs calculated similarity scores with job role metadata in a Pandas
    DataFrame and sorts strictly in descending order (ascending=False).

Step 4: FILTERING (Preventing Choice Overload)
  - Removes any orthogonal roles where similarity score == 0.0.
  - Truncates the sorted output using .head(3) to return only the Top 3 career
    matches alongside Matched Skills (set intersection) and Next Skills to Learn
    (set subtraction: Role Skills - User Skills).


4. ENGINEERING LESSONS & KEY TECHNICAL INSIGHTS FROM DEVELOPMENT
-------------------------------------------------------------------------------
During the development and testing of this system, several critical ML and
software engineering challenges were diagnosed and solved:

  * GPS Path Anchoring (pathlib):
    Replaced fragile "../data/raw_skills.csv" strings with dynamic path
    resolution using Path(__file__).resolve().parent.parent so modules execute
    reliably whether launched from inside src/ or from the root directory.

  * Preserving Technical Tokens in TF-IDF:
    Standard Scikit-Learn regex tokenizers strip punctuation and single-letter
    words, which destroys skills like "C", "C++", "C#", and "CI/CD". By passing
    tokenizer=str.split and token_pattern=None after custom preprocessing, all
    118 technical tokens were preserved intact. (Verified when testing ["a", "b", "c"],
    where the engine accurately identified "c" as the C language and matched
    Embedded Systems Engineer at 32.51%!).

  * Why .fit_transform() vs. .transform() Matters:
    Learned that calling .fit_transform() on user input rebuilds a tiny 3-word
    vocabulary that crashes dimension alignment. The catalog must be fitted once
    (.fit_transform) to lock in the 118-word vocabulary and logarithmic IDF
    weights (verified: git [1.3365] < python [1.4796] < kubernetes [2.9459] <
    figma [3.3514]), while user queries must only call .transform().

  * Solving the Shared Vocabulary & Cold Start Traps:
    When testing ["Python", "SQL", "cybersecurity"], Cybersecurity Analyst
    initially missed the Top 3 because the catalog used the token "security".
    Expanding SYNONYM_MAP bridged the human-to-catalog naming gap. Furthermore,
    when testing completely out-of-vocabulary inputs (["cooking", "gardening",
    "pottery"]), the zero-vector state is intercepted to trigger
    get_trending_fallback(df), serving the Top 3 Global Trending Roles by
    popularity_rank instead of an empty table.


5. HOW TO RUN THE PROJECT
-------------------------------------------------------------------------------
1. Install dependencies:
   pip install pandas scikit-learn scipy

2. Run the interactive application from the project root:
   python app.py

3. Inside the CLI:
   - Type at least 3 comma-separated skills (e.g., Python, Cloud, Automation)
   - Type 'skills' to browse recognized skills grouped by Career Track
   - Type 'q' to exit
===============================================================================