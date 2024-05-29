# UVG_Match: Flask Recommendation System Application

This is a Flask application that provides a user interface for a recommendation system, allowing users to generate new profiles, like or dislike recommendations, save preferences, and register/login/logout.

## Authors
- Juan Cruz
- Nadissa Vela
- Lingna Chen

## Prerequisites

To use this project, you need to have Python 3.12.3 installed on your computer, along with the required dependencies such as Flask 2.3.3 and Requests 2.31.0. Additionally, for the Neo4J Python library, you can use the latest version of the package, which is 5.11.0, available from PyPI (Python Package Index). All these libraries can be installed using pip, which is the Python package manager.

## Installation

1. **Install Python 3.12.3**

   Download and install Python 3.12.3 from the official [Python website](https://www.python.org/downloads/).

2. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/uvg_match.git
   cd uvg_match

3. **Install the Required Dependencies**

   Install the necessary libraries using pip:

   pip install Flask==2.3.3 requests==2.31.0 neo4j==5.11.0

##Dependencies
   Python 3.12.3
   Flask 2.3.3
   Requests 2.31.0
   Neo4J 5.11.0


##Project Structure
   app.py: The main application file where the Flask app is created and configured.
   templates/: Directory containing HTML templates.
   static/: Directory containing static files like CSS and JavaScript.
   src/: Directory containing the source code for the recommendation system, authentication, preferences handling, and like/dislike functionality.

##Usage
   Register: Create a new user account.
   Login: Access your user account.
   Generate New Profile: Generate a new profile based on user preferences.
   Like/Dislike: Like or dislike profiles.
   Save Preferences: Save user preferences for generating more accurate recommendations.
   Logout: Logout from the user account.
