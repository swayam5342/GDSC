# pip install IMDbPY

from imdb import IMDb

# Create an instance of the IMDb class
ia = IMDb()

# Function to get show popularity by title
def get_show_popularity(show_title):
    # Search for the show by title
    search_results = ia.search_movie(show_title)
    
    if search_results:
        show = search_results[0]  # Get the first result from the search
        ia.update(show)  # Fetch the detailed information
        
        # Extract relevant details
        title = show.get('title')
        year = show.get('year')
        rating = show.get('rating')
        votes = show.get('votes')
        
        print(f"Title: {title}")
        print(f"Year: {year}")
        print(f"Rating: {rating}")
        print(f"Number of votes: {votes}")
        
        # Popularity can be assumed based on the number of votes and rating
        if rating and votes:
            popularity_score = rating * votes
            print(f"Popularity Score (Rating x Votes): {popularity_score}")
        else:
            print("Rating or votes information is not available.")
    else:
        print(f"No results found for '{show_title}'.")

# Example usage
show_title = "Death Note"
get_show_popularity(show_title)
