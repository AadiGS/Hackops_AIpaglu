# pip install spotipy python-dotenv spacy
# python -m spacy download en_core_web_md

"""
Intelligent Bollywood Song Recommender with Semantic Mood Analysis

This sophisticated application uses Natural Language Processing to understand the semantic 
meaning of any English word provided as a mood, translates it into quantitative "musical DNA," 
and finds the perfect Bollywood songs using advanced scoring algorithms.

Features:
- Semantic mood analysis using spaCy word vectors
- Intelligent mood-to-music translation with randomization
- Two-phase search: broad Bollywood search + detailed ranking
- Advanced scoring algorithm for perfect song matching
- Support for any English word as mood input

Setup:
Create a .env file with your Spotify credentials:
SPOTIPY_CLIENT_ID='your_spotify_client_id'
SPOTIPY_CLIENT_SECRET='your_spotify_client_secret'
"""

import os
import random
import time
from typing import List, Dict, Tuple, Optional
import spotipy
import spacy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv


class SemanticMoodAnalyzer:
    """Handles semantic analysis of mood words using spaCy NLP model."""
    
    def __init__(self):
        """Initialize the semantic analyzer with spaCy model."""
        print("Loading semantic analysis model (en_core_web_md)...")
        try:
            self.nlp = spacy.load("en_core_web_md")
            print("Semantic model loaded successfully!")
        except Exception as e:
            print(f"Error loading spaCy model: {str(e)}")
            print("Please install the model using: python -m spacy download en_core_web_md")
            raise e
    
    def analyze_mood_semantics(self, mood_word: str) -> Tuple[str, float]:
        """
        Analyze the semantic meaning of a mood word and find the closest core mood.
        Enhanced to handle comprehensive emotion vocabulary.
        
        Args:
            mood_word (str): Any English word representing a mood
            
        Returns:
            Tuple[str, float]: (closest_core_mood, similarity_score)
        """
        # Expanded core moods for comprehensive semantic comparison
        core_moods = ['happy', 'sad', 'energetic', 'calm', 'romantic', 'angry', 'fear', 'surprise', 'disgust']
        
        # First check for direct keyword mappings for better accuracy
        mood_lower = mood_word.lower().strip()
        
        # Direct mappings for specific emotion categories
        direct_mappings = {
            # Happy/Upbeat emotions
            'joyful': 'happy', 'cheerful': 'happy', 'elated': 'happy', 'blissful': 'happy',
            'content': 'happy', 'hopeful': 'happy', 'upbeat': 'happy', 'ecstatic': 'happy',
            'triumphant': 'happy', 'joy': 'happy',
            
            # Sad/Reflective emotions
            'melancholy': 'sad', 'gloomy': 'sad', 'pensive': 'sad', 'sorrowful': 'sad',
            'reflective': 'sad', 'heartbroken': 'sad', 'wistful': 'sad', 'somber': 'sad',
            'sadness': 'sad',
            
            # High-energy emotions
            'pumped': 'energetic', 'motivated': 'energetic', 'victorious': 'energetic',
            'intense': 'energetic', 'fired': 'energetic', 'unstoppable': 'energetic',
            'rebellious': 'energetic', 'powerful': 'energetic',
            
            # Calm/Relaxing emotions
            'peaceful': 'calm', 'serene': 'calm', 'mellow': 'calm', 'tranquil': 'calm',
            'contemplative': 'calm', 'easygoing': 'calm', 'soothing': 'calm', 'meditative': 'calm',
            
            # Romantic emotions
            'passionate': 'romantic', 'loving': 'romantic', 'affectionate': 'romantic',
            'sentimental': 'romantic', 'dreamy': 'romantic', 'enamored': 'romantic',
            'tender': 'romantic', 'adoring': 'romantic',
            
            # Anger emotions
            'anger': 'angry', 'furious': 'angry', 'rage': 'angry', 'mad': 'angry',
            'irritated': 'angry', 'livid': 'angry', 'outraged': 'angry',
            
            # Fear emotions
            'fear': 'fear', 'scared': 'fear', 'terrified': 'fear', 'anxious': 'fear',
            'worried': 'fear', 'nervous': 'fear', 'frightened': 'fear',
            
            # Surprise emotions  
            'surprise': 'surprise', 'surprised': 'surprise', 'amazed': 'surprise',
            'astonished': 'surprise', 'shocked': 'surprise', 'startled': 'surprise',
            
            # Disgust emotions
            'disgust': 'disgust', 'disgusted': 'disgust', 'repulsed': 'disgust',
            'revolted': 'disgust', 'sickened': 'disgust'
        }
        
        # Check for direct mapping first
        if mood_lower in direct_mappings:
            mapped_mood = direct_mappings[mood_lower]
            print(f"Direct mapping: '{mood_word}' -> '{mapped_mood}' (confidence: 1.000)")
            return mapped_mood, 1.0
        
        # Process the user's input word for semantic analysis
        user_token = self.nlp(mood_word.lower().strip())
        
        # Check if the word has semantic meaning (vector representation)
        if not user_token.has_vector:
            print(f"'{mood_word}' doesn't have semantic meaning in the model")
            return 'calm', 0.0  # Default fallback
        
        highest_similarity = -1
        closest_mood = 'calm'
        
        # Compare semantic similarity with each core mood
        for mood in core_moods:
            mood_token = self.nlp(mood)
            similarity = user_token.similarity(mood_token)
            
            if similarity > highest_similarity:
                highest_similarity = similarity
                closest_mood = mood
        
        print(f"Semantic analysis: '{mood_word}' is closest to '{closest_mood}' (similarity: {highest_similarity:.3f})")
        return closest_mood, highest_similarity


class MusicalProfileGenerator:
    """Generates musical profiles from analyzed moods with intelligent randomization."""
    
    def __init__(self):
        """Initialize the musical profile generator with comprehensive mood mappings."""
        # Enhanced core mood to musical attribute mappings
        self.core_profiles = {
            'happy': {'valence': 0.85, 'energy': 0.80, 'tempo': 130, 'danceability': 0.75},
            'sad': {'valence': 0.20, 'energy': 0.25, 'tempo': 75, 'danceability': 0.30},
            'energetic': {'valence': 0.75, 'energy': 0.90, 'tempo': 145, 'danceability': 0.85},
            'calm': {'valence': 0.60, 'energy': 0.25, 'tempo': 85, 'danceability': 0.40},
            'romantic': {'valence': 0.70, 'energy': 0.45, 'tempo': 95, 'danceability': 0.55},
            'angry': {'valence': 0.25, 'energy': 0.95, 'tempo': 150, 'danceability': 0.70},
            'fear': {'valence': 0.15, 'energy': 0.60, 'tempo': 110, 'danceability': 0.35},
            'surprise': {'valence': 0.65, 'energy': 0.75, 'tempo': 125, 'danceability': 0.65},
            'disgust': {'valence': 0.10, 'energy': 0.40, 'tempo': 90, 'danceability': 0.25}
        }
    
    def generate_musical_profile(self, core_mood: str, similarity_score: float) -> Dict[str, float]:
        """
        Generate a musical profile with intelligent randomization based on similarity.
        
        Args:
            core_mood (str): The closest core mood identified
            similarity_score (float): How similar the input was to the core mood
            
        Returns:
            Dict[str, float]: Musical profile with target values
        """
        base_profile = self.core_profiles.get(core_mood, self.core_profiles['calm'])
        
        # Randomization factor based on similarity (less similar = more randomization)
        randomization_factor = max(0.05, 0.15 * (1 - similarity_score))
        
        # Apply intelligent randomization
        profile = {}
        for attribute, base_value in base_profile.items():
            if attribute == 'tempo':
                # Tempo has different scale
                variation = random.uniform(-15, 15) * randomization_factor
                profile[f'target_{attribute}'] = max(60, min(180, base_value + variation))
            else:
                # Valence, energy, danceability are 0-1 scale
                variation = random.uniform(-0.1, 0.1) * randomization_factor
                profile[f'target_{attribute}'] = max(0.0, min(1.0, base_value + variation))
        
        return profile


class BollywoodSongFinder:
    """Handles Spotify API interactions and intelligent song ranking."""
    
    def __init__(self):
        """Initialize Spotify client."""
        self.spotify_client = self._setup_spotify_client()
    
    def _setup_spotify_client(self) -> spotipy.Spotify:
        """Set up and authenticate Spotify client."""
        load_dotenv()
        
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            raise Exception(
                "Missing Spotify credentials. Please create a .env file with:\n"
                "SPOTIPY_CLIENT_ID='your_spotify_client_id'\n"
                "SPOTIPY_CLIENT_SECRET='your_spotify_client_secret'\n"
                "\nGet credentials at: https://developer.spotify.com/dashboard/"
            )
        
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            spotify_client = spotipy.Spotify(auth_manager=auth_manager)
            
            # Test connection
            spotify_client.user('spotify')
            print("Successfully connected to Spotify API!")
            return spotify_client
            
        except Exception as e:
            raise Exception(f"Failed to authenticate with Spotify: {str(e)}")
    
    def find_and_rank_songs(self, musical_profile: Dict[str, float]) -> List[Dict]:
        """
        Two-phase search: broad Bollywood search + intelligent ranking.
        
        Args:
            musical_profile (Dict[str, float]): Target musical attributes
            
        Returns:
            List[Dict]: Top 5 ranked songs
        """
        print("Phase 1: Searching Bollywood songs...")
        
        # Phase 1: Broad search for candidate songs
        candidate_songs = self._get_candidate_songs(musical_profile)
        
        if not candidate_songs:
            print("No candidate songs found")
            return []
        
        print(f"Found {len(candidate_songs)} candidate songs")
        print("Phase 2: Analyzing and ranking songs...")
        
        # Phase 2: Detailed analysis and ranking
        ranked_songs = self._rank_songs_by_match_score(candidate_songs, musical_profile)
        
        return ranked_songs[:5]  # Return top 5
    
    def _search_bollywood_by_artists(self, musical_profile: Dict[str, float]) -> List[Dict]:
        """Alternative search using popular Bollywood artists as seeds."""
        bollywood_artists = [
            'A.R. Rahman', 'Arijit Singh', 'Shreya Ghoshal', 
            'Rahat Fateh Ali Khan', 'Armaan Malik', 'Neha Kakkar'
        ]
        
        try:
            # Get some popular Bollywood artists
            artist_ids = []
            for artist_name in bollywood_artists[:3]:  # Use first 3 artists
                try:
                    results = self.spotify_client.search(q=artist_name, type='artist', limit=1)
                    if results['artists']['items']:
                        artist_ids.append(results['artists']['items'][0]['id'])
                        if len(artist_ids) >= 3:  # Spotify allows max 5 seeds total
                            break
                except:
                    continue
            
            if artist_ids:
                print(f"Using {len(artist_ids)} Bollywood artists as seeds...")
                recommendations = self.spotify_client.recommendations(
                    seed_artists=artist_ids,
                    limit=20,
                    market='IN',
                    **musical_profile
                )
                return recommendations.get('tracks', [])
        except Exception as e:
            print(f"Artist-based search failed: {str(e)}")
        
        return []
    
    def _get_candidate_songs(self, musical_profile: Dict[str, float]) -> List[Dict]:
        """Get a broad set of candidate songs using both recommendations API and search fallback."""
        
        # First, try to get available genres to use proper genre seeds
        try:
            available_genres = self.spotify_client.recommendation_genre_seeds()
            genre_list = available_genres.get('genres', [])
            print(f"Available genres: {len(genre_list)} total")
            
            # Find suitable genres for Indian/Bollywood music
            suitable_genres = []
            indian_related = ['indian', 'bollywood', 'filmi', 'world-music', 'pop', 'folk', 'classical']
            
            for genre in indian_related:
                if genre in genre_list:
                    suitable_genres.append(genre)
                    
            if not suitable_genres:
                # Use most common genres if no Indian-specific ones found
                suitable_genres = ['pop', 'rock', 'electronic'][:min(3, len(genre_list))]
                
            print(f"Using genres: {suitable_genres}")
            
        except Exception as e:
            print(f"Could not get genre seeds: {str(e)}")
            suitable_genres = ['pop']  # Fallback
        
        # Try recommendations API with proper parameters
        try:
            print("Trying recommendations API...")
            
            # Use only the most essential parameters to avoid 404
            params = {
                'seed_genres': suitable_genres[:5],  # Max 5 seeds
                'limit': 20,
                'market': 'US',  # Use US market which has broader availability
            }
            
            # Add musical profile parameters carefully
            if 'target_valence' in musical_profile:
                params['target_valence'] = musical_profile['target_valence']
            if 'target_energy' in musical_profile:
                params['target_energy'] = musical_profile['target_energy']
            if 'target_tempo' in musical_profile:
                params['target_tempo'] = musical_profile['target_tempo']
            
            recommendations = self.spotify_client.recommendations(**params)
            tracks = recommendations.get('tracks', [])
            
            if tracks:
                print(f"Successfully got {len(tracks)} recommendations!")
                return tracks
                
        except Exception as e:
            print(f"Recommendations API failed: {str(e)}")
        
        # Fallback to search-based approach
        print("Falling back to search-based approach...")
        return self._search_bollywood_songs(musical_profile)
    
    def _search_bollywood_songs(self, musical_profile: Dict[str, float]) -> List[Dict]:
        """Search for Bollywood songs using mood-specific search terms."""
        
        # Determine mood-specific search terms based on musical profile
        valence = musical_profile.get('target_valence', 0.5)
        energy = musical_profile.get('target_energy', 0.5)
        tempo = musical_profile.get('target_tempo', 120)
        
        # Categorize the mood based on musical attributes - ONLY Hindi/Bollywood
        if valence > 0.7 and energy > 0.7:
            # Happy/Energetic mood
            search_terms = [
                "hindi bollywood happy song", "bollywood dance hindi", "arijit singh upbeat hindi",
                "shreya ghoshal bollywood happy", "hindi celebration song", "bollywood party hindi"
            ]
        elif valence < 0.3 and energy > 0.8:
            # Angry/Intense mood
            search_terms = [
                "hindi bollywood intense", "bollywood powerful hindi song", "hindi action song",
                "bollywood rock hindi", "hindi motivational song", "bollywood energy hindi"
            ]
        elif valence < 0.4 and energy < 0.4:
            # Sad/Low mood  
            search_terms = [
                "hindi bollywood sad song", "arijit singh emotional hindi", "bollywood breakup hindi",
                "hindi heartbreak song", "shreya ghoshal sad hindi", "bollywood emotional hindi"
            ]
        elif valence < 0.2:
            # Fear/Disgust mood
            search_terms = [
                "hindi bollywood dark song", "bollywood thriller hindi", "hindi suspense song",
                "bollywood dramatic hindi", "hindi intense song", "bollywood mystery hindi"
            ]
        elif energy < 0.4:
            # Calm/Relaxed mood
            search_terms = [
                "hindi bollywood romantic", "bollywood love song hindi", "hindi melodic song",
                "arijit singh romantic hindi", "shreya ghoshal love hindi", "bollywood slow hindi"
            ]
        elif energy > 0.8:
            # High energy mood (surprise, pumped)
            search_terms = [
                "hindi bollywood energetic", "bollywood dance hindi song", "hindi party song",
                "bollywood fast hindi", "hindi celebration", "bollywood upbeat hindi"
            ]
        elif valence > 0.6 and energy < 0.6:
            # Romantic mood
            search_terms = [
                "hindi bollywood love song", "bollywood romantic hindi", "arijit singh love hindi",
                "shreya ghoshal romantic hindi", "hindi melody song", "bollywood soulful hindi"
            ]
        else:
            # Default/Mixed mood - Always Hindi/Bollywood
            search_terms = [
                "hindi bollywood song", "bollywood hindi film song", "arijit singh hindi", 
                "shreya ghoshal bollywood", "ar rahman hindi", "bollywood music hindi"
            ]
        
        print(f"Using mood-specific search terms for valence={valence:.2f}, energy={energy:.2f}")
        
        all_tracks = []
        
        for term in search_terms:
            try:
                print(f"Searching for: {term}")
                results = self.spotify_client.search(
                    q=term, 
                    type='track', 
                    limit=10,
                    market='US'  # Use US market for broader availability
                )
                
                tracks = results.get('tracks', {}).get('items', [])
                all_tracks.extend(tracks)
                
                if len(all_tracks) >= 20:  # Stop once we have enough
                    break
                    
            except Exception as e:
                print(f"Search for '{term}' failed: {str(e)}")
                continue
        
        # Filter for Hindi/Bollywood songs only, then remove duplicates
        hindi_tracks = []
        for track in all_tracks:
            if self._is_hindi_bollywood_song(track):
                hindi_tracks.append(track)
        
        print(f"Filtered to {len(hindi_tracks)} Hindi/Bollywood tracks from {len(all_tracks)} total")
        
        # Remove duplicates by track ID and similar track names
        seen_ids = set()
        seen_names = set()
        unique_tracks = []
        
        for track in hindi_tracks:
            track_id = track['id']
            track_name = self._normalize_track_name(track['name'])
            
            # Check if we've seen this ID or a very similar name
            if track_id not in seen_ids and track_name not in seen_names:
                seen_ids.add(track_id)
                seen_names.add(track_name)
                unique_tracks.append(track)
        
        print(f"Found {len(unique_tracks)} unique Hindi/Bollywood tracks")
        return unique_tracks[:20]  # Return up to 20 tracks
    
    def _is_hindi_bollywood_song(self, track: Dict) -> bool:
        """
        Check if a track is likely to be a Hindi/Bollywood song.
        Uses track name, artist names, and album information to determine.
        """
        track_name = track['name'].lower()
        album_name = track.get('album', {}).get('name', '').lower()
        
        # Get all artist names
        artist_names = [artist['name'].lower() for artist in track.get('artists', [])]
        all_artists = ' '.join(artist_names)
        
        # Known Bollywood/Hindi music indicators
        hindi_indicators = [
            # Language indicators
            'hindi', 'bollywood', 'filmi', 'indian',
            
            # Common Hindi/Urdu words in song titles
            'dil', 'pyaar', 'mohabbat', 'ishq', 'saath', 'zindagi', 'khuda', 'rab',
            'meri', 'tera', 'mere', 'tere', 'main', 'tu', 'hum', 'tumhe',
            'kya', 'hai', 'ho', 'na', 'se', 'ki', 'ka', 'ke', 'wala', 'wali',
            
            # Common Bollywood movie/album phrases
            'from', 'soundtrack', 'film', 'movie', 'picture'
        ]
        
        # Popular Hindi/Bollywood artists
        hindi_artists = [
            'arijit singh', 'shreya ghoshal', 'a.r. rahman', 'ar rahman', 'rahat fateh ali khan',
            'sonu nigam', 'alka yagnik', 'udit narayan', 'kumar sanu', 'lata mangeshkar',
            'kishore kumar', 'mohammed rafi', 'asha bhosle', 'armaan malik', 'neha kakkar',
            'atif aslam', 'vishal dadlani', 'shaan', 'kailash kher', 'jubin nautiyal',
            'darshan raval', 'guru randhawa', 'badshah', 'yo yo honey singh', 'mika singh',
            'sunidhi chauhan', 'shilpa rao', 'asees kaur', 'tulsi kumar', 'palak muchhal',
            'rahat fateh', 'mohit chauhan', 'benny dayal', 'k.k.', 'kk', 'shantanu moitra',
            'vishal-shekhar', 'shankar-ehsaan-loy', 'sajid-wajid', 'nadeem-shravan',
            'jatin-lalit', 'anand-milind', 'laxmikant-pyarelal', 'r.d. burman', 'rd burman',
            'ilaiyaraaja', 'harris jayaraj', 'devi sri prasad', 'thaman', 'pritam',
            'tanishk bagchi', 'amaal mallik', 'sachin-jigar', 'meet bros', 'himesh reshammiya'
        ]
        
        # Check for Hindi indicators in track name or album
        hindi_score = 0
        combined_text = f"{track_name} {album_name}"
        
        for indicator in hindi_indicators:
            if indicator in combined_text:
                hindi_score += 1
        
        # Check for known Hindi artists
        for artist in hindi_artists:
            if artist in all_artists:
                hindi_score += 3  # Higher weight for artist names
        
        # Additional checks for common patterns
        if any(word in track_name for word in ['(from ', '- from ', 'theme', 'title track']):
            hindi_score += 1  # Likely from a movie
            
        # Check if track has typical Bollywood song structure
        if any(pattern in track_name for pattern in ['version', 'reprise', 'remix', 'unplugged']):
            hindi_score += 1
        
        # Return True if we have strong indicators this is a Hindi/Bollywood song
        return hindi_score >= 2  # Need at least 2 indicators
    
    def _normalize_track_name(self, track_name: str) -> str:
        """
        Normalize track names to identify similar/duplicate songs.
        Removes common variations like remixes, versions, featured artists, etc.
        """
        import re
        
        # Convert to lowercase
        name = track_name.lower()
        
        # Remove common variations and suffixes (including dash variations)
        variations_to_remove = [
            r'\s*\(.*remix.*\)',           # Remove remix versions
            r'\s*\(.*reprise.*\)',         # Remove reprise versions
            r'\s*\(.*version.*\)',         # Remove different versions
            r'\s*\(.*edit.*\)',            # Remove edited versions
            r'\s*\(.*feat\..*\)',          # Remove featured artists
            r'\s*\(.*featuring.*\)',       # Remove featuring artists
            r'\s*\(.*ft\..*\)',            # Remove ft. artists
            r'\s*\(.*with.*\)',            # Remove "with" collaborations
            r'\s*\(.*from.*\)',            # Remove "from album/movie" info
            r'\s*\(.*soundtrack.*\)',      # Remove soundtrack info
            r'\s*\(.*original.*\)',        # Remove original versions
            r'\s*\(.*instrumental.*\)',    # Remove instrumental versions
            r'\s*\(.*acoustic.*\)',        # Remove acoustic versions
            r'\s*\(.*live.*\)',            # Remove live versions
            r'\s*\(.*radio.*\)',           # Remove radio versions
            r'\s*\(.*clean.*\)',           # Remove clean versions
            r'\s*\(.*explicit.*\)',        # Remove explicit versions
            r'\s*\(.*lofi.*\)',            # Remove lofi versions
            r'\s*\(.*lo-fi.*\)',           # Remove lo-fi versions
            r'\s*-\s*.*remix.*',           # Remove remix after dash
            r'\s*-\s*.*version.*',         # Remove version after dash
            r'\s*-\s*.*edit.*',            # Remove edit after dash
            r'\s*-\s*.*lofi.*',            # Remove lofi after dash
            r'\s*-\s*.*lo-fi.*',           # Remove lo-fi after dash
            r'\s*-\s*.*remastered.*',      # Remove remastered after dash
            r'\s*-\s*.*slowed.*',          # Remove slowed versions
            r'\s*-\s*.*reverb.*',          # Remove reverb versions
        ]
        
        # Apply all variations removal
        for pattern in variations_to_remove:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
        # Remove extra whitespace and special characters
        name = re.sub(r'[^\w\s]', '', name)  # Remove special chars except letters, numbers, spaces
        name = re.sub(r'\s+', ' ', name)     # Replace multiple spaces with single space
        name = name.strip()                   # Remove leading/trailing spaces
        
        # Remove common Hindi/English words that don't add meaning
        common_words = ['song', 'music', 'hindi', 'bollywood', 'full', 'complete', 'official']
        words = name.split()
        filtered_words = [word for word in words if word not in common_words]
        
        # If we removed too many words, keep the original (but still cleaned)
        if len(filtered_words) >= 2:
            name = ' '.join(filtered_words)
        elif len(filtered_words) >= 1:  # Keep at least one meaningful word
            name = ' '.join(filtered_words)
        
        return name
    
    def _rank_songs_by_match_score(self, songs: List[Dict], target_profile: Dict[str, float]) -> List[Dict]:
        """
        Calculate match scores and rank songs by how well they fit the target profile.
        Since audio features API may not be available, use metadata-based ranking.
        
        Args:
            songs (List[Dict]): Candidate songs
            target_profile (Dict[str, float]): Target musical attributes
            
        Returns:
            List[Dict]: Songs ranked by match score (highest first)
        """
        scored_songs = []
        track_ids = [song['id'] for song in songs]
        
        # Try to get audio features first
        try:
            audio_features_list = self.spotify_client.audio_features(track_ids)
            
            for song, features in zip(songs, audio_features_list):
                if features:  # Make sure features exist
                    match_score = self._calculate_match_score(features, target_profile)
                    scored_songs.append({
                        'song': song,
                        'score': match_score,
                        'features': features
                    })
            
            if scored_songs:  # If we got audio features, use them
                scored_songs.sort(key=lambda x: x['score'], reverse=True)
                
                print("Top matches (using audio features):")
                for i, item in enumerate(scored_songs[:3], 1):
                    song_name = item['song']['name']
                    artist = item['song']['artists'][0]['name']
                    score = item['score']
                    print(f"   {i}. {song_name} by {artist} (score: {score:.3f})")
                
                # Final deduplication by track name before returning
                final_songs = []
                seen_final_names = set()
                
                for item in scored_songs:
                    song = item['song']
                    normalized_name = self._normalize_track_name(song['name'])
                    
                    if normalized_name not in seen_final_names:
                        seen_final_names.add(normalized_name)
                        final_songs.append(song)
                        
                        if len(final_songs) >= 20:  # Limit to 20 unique songs
                            break
                
                return final_songs
            
        except Exception as e:
            print(f"Audio features unavailable: {str(e)}")
        
        # Fallback: Use metadata-based ranking
        print("Using metadata-based ranking...")
        return self._rank_by_metadata(songs, target_profile)
    
    def _rank_by_metadata(self, songs: List[Dict], target_profile: Dict[str, float]) -> List[Dict]:
        """
        Rank songs using metadata and heuristics when audio features aren't available.
        """
        valence = target_profile.get('target_valence', 0.5)
        energy = target_profile.get('target_energy', 0.5)
        
        scored_songs = []
        
        for song in songs:
            score = 0.5  # Base score
            song_name = song['name'].lower()
            artist_name = song['artists'][0]['name'].lower() if song['artists'] else ""
            
            # Enhanced keyword-based scoring for different moods
            if valence > 0.7 and energy > 0.7:  # Happy/Energetic
                happy_keywords = ['happy', 'dance', 'party', 'celebration', 'joy', 'fun', 'upbeat', 'cheerful']
                score += sum(0.1 for keyword in happy_keywords if keyword in song_name)
                
            elif valence < 0.3 and energy > 0.8:  # Angry/Intense
                angry_keywords = ['power', 'intense', 'strong', 'fight', 'battle', 'action', 'rock', 'force']
                score += sum(0.1 for keyword in angry_keywords if keyword in song_name)
                
            elif valence < 0.4 and energy < 0.4:  # Sad/Low
                sad_keywords = ['sad', 'cry', 'heart', 'break', 'emotional', 'pain', 'tears', 'lonely', 'melancholy']
                score += sum(0.1 for keyword in sad_keywords if keyword in song_name)
                
            elif valence < 0.2:  # Fear/Disgust
                dark_keywords = ['dark', 'fear', 'shadow', 'mystery', 'thriller', 'dramatic', 'suspense']
                score += sum(0.1 for keyword in dark_keywords if keyword in song_name)
                
            elif energy < 0.4:  # Calm/Romantic
                calm_keywords = ['love', 'romantic', 'heart', 'pyaar', 'mohabbat', 'dil', 'ishq', 'peaceful', 'serene']
                score += sum(0.1 for keyword in calm_keywords if keyword in song_name)
                
            elif energy > 0.8:  # High energy (surprise, pumped)
                energetic_keywords = ['energy', 'power', 'strong', 'fast', 'rock', 'beat', 'pumped', 'victory']
                score += sum(0.1 for keyword in energetic_keywords if keyword in song_name)
                
            elif valence > 0.6 and energy < 0.6:  # Romantic
                romantic_keywords = ['love', 'romantic', 'heart', 'pyaar', 'mohabbat', 'dil', 'ishq', 'tender', 'passionate']
                score += sum(0.1 for keyword in romantic_keywords if keyword in song_name)
            
            # Boost score for popular artists known for specific moods
            if valence < 0.4 and any(artist in artist_name for artist in ['arijit singh', 'rahat fateh']):
                score += 0.2  # These artists are known for emotional songs
            elif valence > 0.7 and any(artist in artist_name for artist in ['vishal dadlani', 'benny dayal']):
                score += 0.2  # These artists are known for upbeat songs
                
            # Add some randomization to ensure variety
            score += random.uniform(-0.1, 0.1)
            
            scored_songs.append({
                'song': song,
                'score': score
            })
        
        # Sort by score
        scored_songs.sort(key=lambda x: x['score'], reverse=True)
        
        print("Top matches (using metadata):")
        for i, item in enumerate(scored_songs[:3], 1):
            song_name = item['song']['name']
            artist = item['song']['artists'][0]['name']
            score = item['score']
            print(f"   {i}. {song_name} by {artist} (score: {score:.3f})")
        
        # Final deduplication by track name before returning
        final_songs = []
        seen_final_names = set()
        
        for item in scored_songs:
            song = item['song']
            normalized_name = self._normalize_track_name(song['name'])
            
            if normalized_name not in seen_final_names:
                seen_final_names.add(normalized_name)
                final_songs.append(song)
                
                if len(final_songs) >= 20:  # Limit to 20 unique songs
                    break
        
        return final_songs
    
    def _calculate_match_score(self, features: Dict, target_profile: Dict[str, float]) -> float:
        """
        Calculate how well a song matches the target musical profile.
        
        Args:
            features (Dict): Song's audio features from Spotify
            target_profile (Dict[str, float]): Target musical attributes
            
        Returns:
            float: Match score (0-1, higher is better)
        """
        # Weights for different attributes (sum should be 1.0)
        weights = {
            'valence': 0.35,     # Emotional positivity/negativity
            'energy': 0.35,      # Intensity and power
            'tempo': 0.20,       # Speed
            'danceability': 0.10 # Rhythmic elements
        }
        
        total_score = 0.0
        
        for attribute, weight in weights.items():
            target_key = f'target_{attribute}'
            if target_key in target_profile:
                target_value = target_profile[target_key]
                actual_value = features.get(attribute, 0.5)
                
                # Normalize tempo to 0-1 scale for comparison
                if attribute == 'tempo':
                    target_value = target_value / 180.0  # Max reasonable tempo
                    actual_value = actual_value / 180.0
                
                # Calculate similarity (1 - absolute difference)
                similarity = 1.0 - abs(target_value - actual_value)
                total_score += similarity * weight
        
        return max(0.0, min(1.0, total_score))  # Clamp to 0-1 range


class IntelligentBollywoodRecommender:
    """Main application class that orchestrates the recommendation process."""
    
    def __init__(self):
        """Initialize all components."""
        self.mood_analyzer = SemanticMoodAnalyzer()
        self.profile_generator = MusicalProfileGenerator()
        self.song_finder = BollywoodSongFinder()
    
    def recommend_songs(self, mood_word: str) -> List[Dict]:
        """
        Main recommendation pipeline.
        
        Args:
            mood_word (str): Any English word representing a mood
            
        Returns:
            List[Dict]: Top 5 recommended songs
        """
        print(f"Analyzing mood: '{mood_word}'")
        
        # Step 1: Semantic mood analysis
        core_mood, similarity = self.mood_analyzer.analyze_mood_semantics(mood_word)
        
        # Step 2: Generate musical profile
        musical_profile = self.profile_generator.generate_musical_profile(core_mood, similarity)
        
        print("Musical DNA generated:")
        for key, value in musical_profile.items():
            if 'tempo' in key:
                print(f"   {key.replace('target_', '').title()}: {value:.0f} BPM")
            else:
                print(f"   {key.replace('target_', '').title()}: {value:.2f}")
        
        # Step 3: Find and rank songs
        songs = self.song_finder.find_and_rank_songs(musical_profile)
        
        return songs
    
    def display_recommendations(self, songs: List[Dict], mood_word: str):
        """Display the final recommendations in a beautiful format."""
        if not songs:
            print("Sorry, I couldn't find any Bollywood songs matching your mood.")
            print("Try a different mood word or check your internet connection.")
            return
        
        print(f"\nHere are 5 perfect Bollywood songs for your '{mood_word}' mood:\n")
        
        for i, song in enumerate(songs, 1):
            song_name = song['name']
            artists = [artist['name'] for artist in song['artists']]
            artist_string = ', '.join(artists)
            
            # Add some visual flair
            print(f"{i}. {song_name}")
            print(f"   by {artist_string}")
            if i < len(songs):  # Don't add separator after last song
                print()
        
        print("Enjoy your personalized Bollywood music experience!")


def main():
    """Main application entry point."""
    print("Welcome to the Intelligent Bollywood Song Recommender!")
    print("=" * 70)
    print("I can understand ANY English word as a mood and find perfect songs!")
    print("Examples: triumphant, melancholic, euphoric, contemplative, nostalgic")
    print("=" * 70)
    
    try:
        # Initialize the recommender system
        recommender = IntelligentBollywoodRecommender()
        
        # Get user input
        print("\nTell me about your mood using any English word...")
        mood_input = input("What's your mood? ").strip()
        
        if not mood_input:
            print("Please enter a mood word to get recommendations!")
            return
        
        # Get recommendations
        start_time = time.time()
        songs = recommender.recommend_songs(mood_input)
        end_time = time.time()
        
        # Display results
        recommender.display_recommendations(songs, mood_input)
        
        print(f"\nAnalysis completed in {end_time - start_time:.1f} seconds")
        
    except KeyboardInterrupt:
        print("\nThanks for using the Intelligent Bollywood Recommender!")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
