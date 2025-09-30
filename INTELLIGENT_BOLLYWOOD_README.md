# 🎭 Intelligent Bollywood Song Recommender with Semantic Mood Analysis

A sophisticated, AI-powered command-line application that recommends perfect Bollywood songs by understanding the semantic meaning of **any English word** you provide as a mood.

## 🧠 How It Works (The "Brain" Behind the Magic)

### 1. **Semantic Mood Analysis**
- Uses advanced NLP (spaCy's `en_core_web_md` model) with 300-dimensional word vectors
- Understands semantic meaning of **any English word** (not just predefined keywords)
- Compares your word against core emotional states using cosine similarity
- Examples: "triumphant" → "energetic", "melancholic" → "sad", "euphoric" → "happy"

### 2. **Musical DNA Translation**
- Converts analyzed emotions into quantitative "musical attributes"
- Generates target values for valence, energy, tempo, and danceability
- Applies intelligent randomization based on semantic similarity scores
- Ensures varied recommendations while maintaining mood accuracy

### 3. **Two-Phase Intelligent Search**
- **Phase 1**: Broad Bollywood search using Indian market preferences
- **Phase 2**: Advanced scoring algorithm ranks 20 candidates by musical fit
- Returns the 5 most perfectly matched songs

### 4. **Advanced Scoring Algorithm**
- Calculates "match scores" by comparing actual vs. target audio features
- Weighted scoring: Valence (35%) + Energy (35%) + Tempo (20%) + Danceability (10%)
- Ensures recommendations are scientifically aligned with your emotional state

## 🚀 Setup Instructions

### 1. Install Dependencies

First, install the required packages:

```bash
pip install spotipy python-dotenv spacy
```

Then install the spaCy language model:

```bash
python -m spacy download en_core_web_md
```

**Alternative**: Use the updated requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new app
3. Copy your Client ID and Client Secret
4. Create a `.env` file:

```env
SPOTIPY_CLIENT_ID='your_spotify_client_id_here'
SPOTIPY_CLIENT_SECRET='your_spotify_client_secret_here'
```

### 3. Run the Application

```bash
python intelligent_bollywood_recommender.py
```

## 🎨 Usage Examples

The beauty of this system is that it understands **ANY English word** as a mood:

### Simple Moods
```
What's your mood? happy
What's your mood? sad
What's your mood? energetic
```

### Complex Emotions
```
What's your mood? melancholic
What's your mood? euphoric
What's your mood? contemplative
What's your mood? triumphant
What's your mood? nostalgic
```

### Advanced Emotional States
```
What's your mood? serene
What's your mood? exuberant
What's your mood? wistful
What's your mood? jubilant
What's your mood? brooding
```

## 🎼 Sample Output

```
🎭 Welcome to the Intelligent Bollywood Song Recommender! 🎭
======================================================================
✨ I can understand ANY English word as a mood and find perfect songs!
📝 Examples: triumphant, melancholic, euphoric, contemplative, nostalgic
======================================================================

🧠 Loading semantic analysis model (en_core_web_md)...
✅ Semantic model loaded successfully!
🎵 Successfully connected to Spotify API!

🎨 Tell me about your mood using any English word...
What's your mood? triumphant

🎭 Analyzing mood: 'triumphant'
🎯 Semantic analysis: 'triumphant' is closest to 'energetic' (similarity: 0.742)

🎼 Musical DNA generated:
   Valence: 0.81
   Energy: 0.89
   Tempo: 142 BPM
   Danceability: 0.87

🔍 Phase 1: Searching Bollywood songs...
📊 Found 20 candidate songs
🎯 Phase 2: Analyzing and ranking songs...

🏆 Top matches:
   1. Jai Ho by A.R. Rahman (score: 0.943)
   2. Nagada Sang Dhol by Shreya Ghoshal (score: 0.921)
   3. Malhari by Vishal Dadlani (score: 0.898)

🎵 Here are 5 perfect Bollywood songs for your 'triumphant' mood:

🎶 1. Jai Ho
   👨‍🎤 by A.R. Rahman

🎶 2. Nagada Sang Dhol
   👨‍🎤 by Shreya Ghoshal

🎶 3. Malhari
   👨‍🎤 by Vishal Dadlani

🎶 4. Senorita
   👨‍🎤 by Farhan Akhtar

🎶 5. Tattad Tattad
   👨‍🎤 by Arijit Singh

🎧 Enjoy your personalized Bollywood music experience!

⏱️  Analysis completed in 2.3 seconds
```

## 🔬 Technical Architecture

### SemanticMoodAnalyzer Class
- Loads spaCy's `en_core_web_md` model (300D word vectors)
- Performs cosine similarity analysis between input and core moods
- Returns semantic match with confidence score

### MusicalProfileGenerator Class
- Maps core moods to quantitative musical attributes
- Applies intelligent randomization based on semantic similarity
- Generates target values for Spotify's recommendation algorithm

### BollywoodSongFinder Class
- Manages Spotify API interactions
- Implements two-phase search strategy
- Advanced scoring algorithm with weighted attribute matching

### IntelligentBollywoodRecommender Class
- Orchestrates the entire recommendation pipeline
- Handles user interaction and result presentation
- Provides comprehensive error handling

## 🎯 Key Features

### ✨ **Universal Mood Understanding**
- Works with **any English word** - not just predefined keywords
- Semantic analysis understands context and emotional nuance
- Handles complex emotions like "melancholic", "jubilant", "contemplative"

### 🎵 **Bollywood-Focused Search**
- Specifically targets Indian music market
- Uses Bollywood genre seeds: 'indian', 'bollywood', 'filmi'
- Optimized for Hindi film music discovery

### 🧮 **Scientific Matching**
- Quantitative analysis of musical attributes
- Weighted scoring algorithm for precise matching
- Audio feature analysis for each candidate song

### 🎲 **Intelligent Randomization**
- Prevents repetitive recommendations
- Randomization factor based on semantic similarity
- Maintains mood accuracy while ensuring variety

## 🛠️ Advanced Configuration

### Mood Profile Customization
You can modify the core mood profiles in `MusicalProfileGenerator`:

```python
self.core_profiles = {
    'happy': {'valence': 0.85, 'energy': 0.80, 'tempo': 130, 'danceability': 0.75},
    'sad': {'valence': 0.20, 'energy': 0.25, 'tempo': 75, 'danceability': 0.30},
    # Add your custom profiles...
}
```

### Scoring Algorithm Weights
Adjust the importance of different musical attributes:

```python
weights = {
    'valence': 0.35,     # Emotional positivity
    'energy': 0.35,      # Intensity and power  
    'tempo': 0.20,       # Speed/rhythm
    'danceability': 0.10 # Rhythmic elements
}
```

## 🔧 Troubleshooting

### spaCy Model Issues
```bash
# Download the model manually
python -m spacy download en_core_web_md

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_md'); print('Model loaded!')"
```

### Spotify API Issues
- Ensure your `.env` file is in the correct directory
- Check that your Spotify app has proper permissions
- Verify your credentials are active

### No Songs Found
- Try different mood words
- Check your internet connection
- Ensure Spotify API is accessible in your region

## 🎓 Understanding the Science

### Word Vectors & Semantic Similarity
The system uses 300-dimensional word vectors from spaCy's `en_core_web_md` model. Each word is represented as a point in high-dimensional space, where semantically similar words are closer together.

### Cosine Similarity
```python
similarity = user_token.similarity(mood_token)
```
This calculates the cosine of the angle between two word vectors, giving a similarity score from 0 (completely different) to 1 (identical meaning).

### Musical Attribute Mapping
Spotify's audio features provide quantitative measures:
- **Valence**: Musical positivity (0 = sad, 1 = happy)
- **Energy**: Intensity and power (0 = calm, 1 = energetic)  
- **Tempo**: Speed in beats per minute
- **Danceability**: Rhythmic elements (0 = not danceable, 1 = very danceable)

## 🎉 What Makes This Special

1. **True AI Understanding**: Not keyword matching - actual semantic comprehension
2. **Bollywood Expertise**: Specifically optimized for Indian film music
3. **Scientific Precision**: Quantitative analysis ensures perfect mood matching
4. **Infinite Vocabulary**: Works with any English word you can think of
5. **Advanced Ranking**: Two-phase search with intelligent scoring

This isn't just a music recommender - it's an AI-powered emotional companion that speaks the language of Bollywood music! 🎭🎵
