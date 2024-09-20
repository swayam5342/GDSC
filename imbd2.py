from imdb import IMDb

# Create an instance of the IMDb class
ia = IMDb()

# Function to get show popularity and genre by title
def get_show_popularity_and_genre(show_title):
    # Search for the show by title
    search_results = ia.search_movie(show_title)
    
    if search_results:
        show = search_results[0]  # Get the first result from the search
        ia.update(show)  # Fetch detailed information
        
        # Extract relevant details
        title = show.get('title')
        year = show.get('year')
        rating = show.get('rating')
        votes = show.get('votes')
        genres = show.get('genres')

        # Print show details
        print(f"Title: {title}")
        print(f"Year: {year}")
        print(f"Rating: {rating}")
        print(f"Number of votes: {votes}")
        print(f"Genres: {', '.join(genres) if genres else 'No genre information available'}")
        
        # Calculate and print popularity score (if rating and votes are available)
        if rating and votes:
            popularity_score = rating * votes
            print(f"Popularity Score (Rating x Votes): {popularity_score}")
        else:
            print("Rating or votes information is not available.")
    else:
        print(f"No results found for '{show_title}'.")

# Example usage
show_title = "Breaking Bad"
get_show_popularity_and_genre(show_title)
