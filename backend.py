import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Spotify API credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

# Spotify API function to get artist details
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def spotify(name):
    # Search for the artist
    results = sp.search(q='artist:' + name, type='artist')
    
    # Extract artist info
    artists = results['artists']['items']
    if artists:
        artist = artists[0]
        return {
            "Name": artist['name'],
            "Followers": artist['followers']['total'],
            "Genres": ', '.join(artist['genres'])
        }
    else:
        return None  # Return None if artist not found

# Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="roh286tan910",
        database="gdsc"
    )

# Insert a new user into the database
def insert_user(name, gender, phone, language, artists, q2, q8, q9, q10):
    db = connect_db()
    cursor = db.cursor()
    
    query = """INSERT INTO user_responses (name, gender, phone_number, language, q1, q2, q8, q9, q10) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (name, gender, phone, language, ', '.join(artists), q2, q8, q9, q10)
    
    cursor.execute(query, values)
    db.commit()
    user_id = cursor.lastrowid  # Get the last inserted user ID
    db.close()
    
    return user_id

# Compare MCQ responses between users and assign 5 points per match
def compare_mcq_responses(user_id, new_user_responses):
    db = connect_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT user_id, q1, q2, q8, q9, q10 FROM user_responses")
    all_users = cursor.fetchall()
    
    total_mcq_points = {}
    
    # Loop through all existing users and compare their responses to the new user's responses
    for user in all_users:
        if user[0] == user_id:
            continue  # Skip the current user
        
        existing_user_responses = user[1:]  # Get q1 to q10 responses of the existing user
        points = 0
        
        # Compare MCQ answers question by question
        if new_user_responses[0] == existing_user_responses[1]:
            points += 5
        if new_user_responses[1] == existing_user_responses[2]:
            points += 5
        if new_user_responses[2] == existing_user_responses[3]:
            points += 5
        if new_user_responses[3] == existing_user_responses[4]:
            points += 5

        total_mcq_points[user[0]] = points  # Assign points for this user pair
    
    db.close()
    return total_mcq_points

# Function to get all users' artist preferences from the database
def get_all_users():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id, q1 FROM user_responses")  # q1 could hold artist names in this case
    users = cursor.fetchall()
    db.close()
    return users

# Calculate points based on artist matching
def calculate_artist_points(user_artists, input_artists):
    total_points = 0
    matched_artists = set()

    input_artist_set = {artist.lower() for artist in input_artists}

    for user_artist in user_artists:
        artist_data = spotify(user_artist.strip())  
        if artist_data is None:
            continue

        if user_artist.lower() in input_artist_set:
            followers = artist_data['Followers']
            if followers > 25000000:
                total_points += 10
            elif 7000000 <= followers <= 25000000:
                total_points += 18
            else:
                total_points += 25
            matched_artists.add(user_artist.lower())  

    for user_artist in user_artists:
        artist_data = spotify(user_artist.strip())
        if artist_data is None:
            continue
        
        user_genres = artist_data['Genres'].lower().split(', ')
        
        for input_artist in input_artists:
            input_artist_data = spotify(input_artist.strip())
            if input_artist_data is None:
                continue
            
            input_genres = input_artist_data['Genres'].lower().split(', ')
            if user_artist.lower() not in matched_artists and any(genre in input_genres for genre in user_genres):
                total_points += 1  
                break

    return total_points

# Function to generate pairings combining MCQ points and artist matching points
def generate_pairings(user_id, input_artists, mcq_responses):
    all_users = get_all_users()
    
    total_pairings = {}
    
    mcq_points = compare_mcq_responses(user_id, mcq_responses)
    
    for db_user_id, db_user_artists in all_users:
        if db_user_id == user_id:
            continue  # Skip self-pairing
        
        db_user_artist_list = db_user_artists.split(',')
        artist_points = calculate_artist_points(db_user_artist_list, input_artists)
        
        # Combine MCQ points and artist points
        total_points = artist_points + mcq_points.get(db_user_id, 0)
        
        total_pairings[db_user_id] = total_points
    
    return total_pairings

# Function to prompt user input
def get_user_input():
    name = input("Enter Your Name : ")
    gender = input("Enter Your Gender (Male/Female/Other) : ")
    phone = input("Enter Your Phone Number : ")
    language = input("Enter Your Preferred Language : ")

    # Asking the user for their favorite artists
    artists = []
    for i in range(1, 4):
        artist = input(f"Enter favorite artist {i}: ")
        artists.append(artist)

    # Asking MCQ questions
    print("\nAnswer The Following MCQs : \n")

    q1 = input("How Are You Feeling Today? : \n")
    q2 = input("(2) Imagine It's A Friday Evening, And All Your Classes Have Just Been Unexpectedly Cancelled. You Suddenly Find Yourself With Three Glorious Hours Of Free Time On The Massive VIT Campus, With No Immediate Responsibilities. How Do You Choose To Spend This Time? : \n"
               "a) Head To Your Room & Dial In On Some Video Games\n"
               "b) Take A Walk Around The Campus With Some Beats\n"
               "c) Grab A Ball And Some Ballers To Play A Sport\n"
               "d) Head To Periyar To Catch Up On Some Work\n"
               "e) Get Some Popcorn With A Show Or Movie\n"
               "f) Hit The Gym To Hit A Couple Sets\n"
               "g) Get Cozy With A Book\n"
               "h) Sleep\n\n"
               "->  ")

    q8 = input("(8) Imagine There’s a Buzzing Event Happening on Campus—Which of These Activities Are You Most Likely to Show Up For? What Kind of Campus Scene Gets You Excited to Be a Part of It? : \n"
               "a) Flash Mob/Dance Battle [Dance Performance or Competition]\n"
               "b) Cultural Carnival [Music Concert or Cultural Fest]\n"
               "c) Fitness Frenzy [Fitness Bootcamp or Yoga Session]\n"
               "d) Art & Soul [Art Exhibition or Cultural Showcase]\n"
               "e) Social Mixer [Networking Event or Career Fair]\n"
               "f) Tech Extravaganza [Hackathon or Coding Event]\n"
               "g) Brainstorm Bash [Guest Lecture or Seminar]\n"
               "h) Marathon Movie Madness [Film Screening]\n"
               "i) E-Sports Fever [Gaming Tournament]\n"
               "j) Serious Sport Mode [Sports Event]\n\n"
               "-> ")

    q9 = input("(9) Imagine You’re at Peak Productivity Mode—But What Time of Day Does That Magic Happen? When Do You Feel Most in Sync With Your To-Do List and Ready to Take on the World? : \n"
               "a) Crack of Dawn [5 AM - 8 AM]\n"
               "b) Mid-Morning Hustle [8 AM - 11 AM]\n"
               "c) Post-Lunch Power Hour [12 PM - 3 PM]\n"
               "d) Golden Hour Grind [4 PM - 7 PM]\n"
               "e) Night Owl Mode [8 PM - 11 PM]\n"
               "f) Midnight Madness [12 AM - 4 AM]\n\n"
               "-> ")

    q10 = input("(10) Imagine You’ve Got a Deadline Looming, But Procrastination Has Other Plans. Which of the Following is Your Go-To Way of Avoiding Work When You Should Really Be Focusing? : \n"
                "a) Go on a Random Walk Around Campus, Hoping Inspiration Strikes\n"
                "b) Organize Your Playlist (Because Music Matters More Right Now)\n"
                "c) Binge-Watch “Just One More” Episode of Your Favorite Show\n"
                "d) Start a New Hobby You’ll Definitely Master in 30 Minutes\n"
                "e) Scroll Through Social Media Like It's a Part-Time Job\n"
                "f) Clean Your Entire Room for the First Time in Weeks\n"
                "g) Play “Just One Game” That Somehow Lasts Hours\n"
                "h) Whip Up a Snack You Absolutely Don’t Need\n"
                "i) Dive Headfirst Into a YouTube Rabbit Hole\n"
                "j) Nap Like There’s No Tomorrow\n\n"
                "-> ")

    # Return all the responses
    return name, gender, phone, language, artists, [q1, q2, q8, q9, q10]

# Example usage
if __name__ == "__main__":
    name, gender, phone, language, input_artists, mcq_responses = get_user_input()
    
    # Insert the user into the database and get user_id
    user_id = insert_user(name, gender, phone, language, input_artists, mcq_responses[1], mcq_responses[2], mcq_responses[3], mcq_responses[4])

    # Generate pairings and total points
    pairings = generate_pairings(user_id, input_artists, mcq_responses)
    
    for user, points in pairings.items():
        print(f"User {user} paired with User {user_id} has {points} points.")


