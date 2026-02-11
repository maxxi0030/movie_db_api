# Movie API Research Project

Comparative analysis of movie/TV show APIs for retrieving cast information and metadata.

## 📋 Project Overview

This project was developed as part of a practical research assignment to evaluate different movie database APIs and determine the most suitable solution for obtaining detailed cast information for films and TV series.

## 🎯 Research Goals

- Compare functionality of various movie APIs (TMDB, OMDB, IMDB, TVmaze, TheTVDB)
- Evaluate data quality (cast completeness, character roles, metadata)
- Analyze pricing models and request limits
- Develop proof-of-concept applications

## 📁 Project Structure

```
.
├── app.py           # TMDB API implementation (recommended solution)
├── script.py        # TVmaze & TheTVDB API comparison
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## 🔧 Applications

### 1. TMDB Application (app.py) ⭐ Recommended

**Why TMDB?**
- Complete cast information with character roles
- Support for both movies and individual TV episodes
- Free API for non-commercial use with sufficient limits
- High-quality posters and rich metadata
- REST API with JSON responses

**Features:**
- Search movies and TV shows by title
- View detailed cast information with character names
- Display posters and episode stills
- Gender indicators for actors (♀️/♂️)
- Clean Bootstrap UI

**Usage:**
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

**Example searches:**
- Movies: "Inception", "The Matrix"
- TV Shows: "Breaking Bad" (specify season/episode)

---

### 2. API Comparison Tool (script.py)

Compares TVmaze and TheTVDB APIs for TV series data.

**Features:**
- Side-by-side comparison of API responses
- Cast information from both sources
- Guest stars vs. regular cast differentiation

**Usage:**
```bash
python script.py
# Open http://localhost:5000
# Select API: TVmaze or TheTVDB
```

**Note:** TheTVDB requires a valid authentication token (included token may expire).

---

## 📊 API Comparison Results

| API | Cost | Cast Data | Metadata | Best For |
|-----|------|-----------|----------|----------|
| **TMDB** | Free (non-commercial) | ✅ Excellent | ✅ Rich | Movies + TV episodes |
| **OMDB** | Free tier limited | ⚠️ Basic | ⚠️ Ratings only | Quick lookups |
| **IMDB Official** | $150k+/year | ✅ Complete | ✅ Complete | Enterprise only |
| **TVmaze** | Free | ✅ Good | ✅ Good | TV shows only |
| **TheTVDB** | Free tier | ✅ Good | ✅ Good | TV shows only |

## 🏆 Conclusion

**TMDB API** was selected as the optimal solution due to:
- Best balance of features and cost
- Comprehensive cast/character data
- Excellent documentation and reliability
- Active community support

## 🔑 API Keys

To run these applications, you need:

1. **TMDB API Key** (app.py):
   - Register at https://www.themoviedb.org/
   - Go to Settings → API → Request API Key
   - Replace `API_KEY` in `app.py`

2. **TheTVDB Token** (script.py):
   - Register at https://www.thetvdb.com/
   - Get API key from dashboard
   - Token expires periodically (needs refresh)

## 📦 Dependencies

```
Flask==3.0.0
requests==2.31.0
```

## 🖼️ Screenshots

### TMDB Application
- Search interface with season/episode selectors
- Movie/TV show results with posters
- Detailed cast list with character roles
- Responsive Bootstrap design

## 📝 Notes

- Both applications are for educational/research purposes
- API keys included in code are for demonstration only
- Follow API terms of service for production use
- TMDB requires attribution link in production apps

## 👨‍💻 Author

Developed during practical training assignment focused on API integration and comparative analysis.

---

**License:** Educational use only
