import os
import logging
import requests  # Make sure to install this package using pip if not already installed
from pyrogram import Client, filters
from utils import get_poster


# Configure logging
logging.basicConfig(
    filename="imdb_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Error logging function
def log_error(error_message):
    logging.error(error_message)

# Function to fetch movie details including poster from OMDb API
async def get_poster(title):
    api_key = "7998b36c"  # Replace with your OMDb API key
    try:
        # Fetch data from OMDb API
        response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={api_key}")
        data = response.json()

        # Check if the response contains a valid movie
        if data.get("Response") == "True":
            return {
                'title': data.get('Title', 'N/A'),
                'languages': data.get('Language', 'N/A').split(', '),
                'year': data.get('Year', 'N/A'),
                'release_date': data.get('Released', 'N/A'),
                'genres': data.get('Genre', 'N/A').split(', '),
                'rating': data.get('imdbRating', 'N/A'),
                'runtime': data.get('Runtime', 'N/A'),
                'poster': data.get('Poster', ''),  # Get the actual poster URL
                'plot': data.get('Plot', 'No plot available.'),
            }
        else:
            log_error(f"No data found for {title}. Error: {data.get('Error')}")
            return None
    except Exception as e:
        # Log error if fetching fails
        log_error(f"Failed to fetch data for {title}: {str(e)}")
        return None

@Client.on_message(filters.command("imdbpost"))
async def imdb_post(bot, message):
    if len(message.command) < 2:
        await message.reply("Usage: /imdbpost <movie_name>")
        return

    # Extract the title from the command
    title = " ".join(message.command[1:])
    k = await message.reply("Fetching IMDb information...")

    # Fetch IMDb data based on the title
    try:
        imdb_data = await get_poster(title)
        if not imdb_data:
            await k.edit("No IMDb information found.")
            return
    except Exception as e:
        log_error(f"Error fetching IMDb data for '{title}': {str(e)}")
        await k.edit("Error fetching IMDb information. Please try again later.")
        return

    # Extract necessary details
    imdb_title = imdb_data.get('title', 'N/A')
    imdb_language = ', '.join(imdb_data.get('languages', ['N/A']))
    imdb_release_year = imdb_data.get('year', 'N/A')
    imdb_release_date = imdb_data.get('release_date', 'N/A')
    imdb_genres = ', '.join(imdb_data.get('genres', ['N/A']))
    imdb_rating = imdb_data.get('rating', 'N/A')
    imdb_runtime = imdb_data.get('runtime', 'N/A')
    imdb_poster = imdb_data.get('poster', '')

    # Create the custom HTML using the fetched IMDb details
    custom_html = f"""
    <div class="entry-content" style="background-color: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 8px; font-family: Arial, sans-serif;">
    <p style="text-align: center; margin-bottom: 20px;"><img src="{imdb_poster}" alt="Poster of {imdb_title}" style="border-radius: 8px; max-width: 100%;"/></p>

    <h2 style="text-align: center; color: #ffdd57; margin-bottom: 10px;">Download {imdb_title} in {imdb_language} Languages, and 1080p, 720p, & 480p Qualities.</h2>
    <p style="text-align: justify; line-height: 1.6;">
        ✅ Download {imdb_title}. This movie is available in {imdb_language} Languages and high-quality formats:
        <span style="color: #ffa500;"><strong>1080p</strong></span>, 
        <span style="color: #ffa500;"><strong>720p</strong></span>, and 
        <span style="color: #ffa500;"><strong>480p</strong></span>. 
        {imdb_title} is a gripping {imdb_genres} movie that keeps you hooked from start to finish. Now available for streaming and download in {imdb_language}, this film offers stunning visuals and an unforgettable plotline. Don’t miss out on the ultimate cinematic experience with {imdb_title}.
    </p>

    <h3 style="text-align: center; color: #66bb6a; margin-top: 20px;">Watch or Download {imdb_title} in {imdb_language} Languages and in 480p, 720p & 1080p qualities.</h3>
    <ul style="list-style: none; padding: 0; margin: 10px 0 20px;">
        <li><strong>🎬 Full Name:</strong> {imdb_title}</li>
        <li><strong>🗂️ Genres:</strong> {imdb_genres}</li>
        <li><strong>⭐ Rating:</strong> {imdb_rating}</li>
        <li><strong>⏰ Runtime:</strong> {imdb_runtime}</li>
        <li><strong>🗣️ Language:</strong> {imdb_language}</li>
        <li><strong>📅 Released Year:</strong> {imdb_release_year}</li>
        <li><strong>📆 Release Date:</strong> {imdb_release_date}</li>
    </ul>

    <h4 style="text-align: center; color: #ff6347;"><strong>Plot Summary:</strong></h4>
    <p style="text-align: justify; margin-bottom: 20px;">{imdb_data.get('plot', 'No plot available.')}</p>
    
    <hr style="border: 1px solid #444; margin: 20px 0;"/>

    <div style="text-align: center;">
        <h5 style="color: #ffffff;"><strong>{imdb_title} <span style="color: #ffdd57;">{imdb_language}</span> <span style="color: #ffa500;">Complete</span> 480p [450MB]</strong></h5>
        <a href="https://nexdrive.fun/genxfm784776261893/" target="_blank" rel="nofollow noopener noreferrer" style="text-decoration: none;">
            <button class="dwd-button" style="background-color: #2196f3; color: #fff; border: none; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; transition: background 0.3s;">Download Now</button>
        </a>

        <h5 style="color: #ffffff; margin-top: 20px;"><strong>{imdb_title} <span style="color: #ffdd57;">{imdb_language}</span> <span style="color: #ffa500;">Complete</span> 720p [800MB]</strong></h5>
        <a href="https://nexdrive.fun/genxfm784776261893/" target="_blank" rel="nofollow noopener noreferrer" style="text-decoration: none;">
            <button class="dwd-button" style="background-color: #4caf50; color: #fff; border: none; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; transition: background 0.3s;">Download Now</button>
        </a>

        <h5 style="color: #ffffff; margin-top: 20px;"><strong>{imdb_title} <span style="color: #ffdd57;">{imdb_language}</span> <span style="color: #ffa500;">Complete</span> 1080p [999MB]</strong></h5>
        <a href="https://nexdrive.fun/genxfm784776261893/" target="_blank" rel="nofollow noopener noreferrer" style="text-decoration: none;">
            <button class="dwd-button" style="background-color: #e91e63; color: #fff; border: none; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; transition: background 0.3s;">Download Now</button>
        </a>
    </div>

    <hr style="border: 1px solid #444; margin: 20px 0;"/>

    <h3 style="text-align: center; color: #32cd32;">Wrapping Up ❤️</h3>
    <p style="text-align: center;">Thank you for visiting MovieZapiya. Enjoy the best quality downloads of Movies and TV Series. Don’t forget to share with your friends!</p>
    </div>
    """

    # Save the HTML to a file
    file_name = f"{title.replace(' ', '_')}.html"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(custom_html)

    # Send the HTML file to the user
    await bot.send_document(message.chat.id, file_name, caption=f"Here's your custom IMDb post for {imdb_title}.")

    # Delete the file from the server after sending
    os.remove(file_name)
    await k.delete()
    
    
    
    
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from requests.auth import HTTPBasicAuth

# WordPress credentials and URL
WORDPRESS_URL = 'https://moviezapiya.fun/wp-json/wp/v2'
WORDPRESS_USERNAME = 'MovieZapiyaOfficial'
WORDPRESS_PASSWORD = 'uY2h ZA88 zO1G 12fH WtSL keTh'

# Function to get IMDb data
def get_imdb_data(movie_name):
    # Implement the IMDb data fetching logic here
    # Example response structure
    return {
        'title': movie_name,
        'poster': 'https://example.com/poster.jpg',
        'genres': 'Action, Drama',
        'rating': '8.5',
        'runtime': '120 min',
        'language': 'English',
        'release_year': '2023',
        'release_date': '2023-05-10',
        'plot': 'A thrilling action-packed movie.'
    }

# Function to create post on WordPress
def create_wordpress_post(title, content, featured_image_url):
    headers = {'Content-Type': 'application/json'}
    auth = HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    data = {
        'title': title,
        'content': content,
        'status': 'publish'
    }
    
    # Upload featured image
    image_data = requests.get(featured_image_url).content
    media_response = requests.post(f"{WORDPRESS_URL}/media", headers=headers, auth=auth, files={'file': image_data})
    
    if media_response.status_code == 201:
        media_id = media_response.json().get('id')
        data['featured_media'] = media_id

    # Post creation
    response = requests.post(f"{WORDPRESS_URL}/posts", json=data, headers=headers, auth=auth)
    return response.status_code == 201

# Bot command function
@Client.on_message(filters.command("url_to_wppost"))
async def imdb_post(bot, message):
    if len(message.command) < 4:
        await message.reply("Usage: /url_to_wppost <movie_name_for_imdb_data> <targeted_post_link> <word_replacement>(oldWord|newWord)")
        return
    
    movie_name = message.command[1]
    post_link = message.command[2]
    word_replacement = message.command[3].split('|')

    try:
        response = requests.get(post_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data from the targeted post
        extracted_title = soup.find('h1').text
        screenshot_images = [img['src'] for img in soup.find_all('img') if 'screenshot' in img.get('alt', '').lower()]
        buttons = [{'title': btn.text, 'url': btn['href']} for btn in soup.find_all('a') if 'button' in btn.get('class', [])]
        
        # Word replacement
        if len(word_replacement) == 2:
            extracted_title = extracted_title.replace(word_replacement[0], word_replacement[1])
            for button in buttons:
                button['title'] = button['title'].replace(word_replacement[0], word_replacement[1])

        # Get IMDb data
        imdb_data = get_imdb_data(movie_name)

        # Format the content for WordPress post
        CUSTOM_HTML_FORMAT = f"""
        <div class="entry-content" style="background-color: #1e1e1e; color: #d4d4d4; padding: 20px; border-radius: 8px; font-family: Arial, sans-serif;">
            <p style="text-align: center; margin-bottom: 20px;">
                <img src="{imdb_data['poster']}" alt="Poster of {imdb_data['title']}" style="border-radius: 8px; max-width: 100%;"/>
            </p>

            <h2 style="text-align: center; color: #ffdd57; margin-bottom: 10px;">{extracted_title}</h2>
            <p style="text-align: justify; line-height: 1.6;">
                ✅ Download {imdb_data['title']}. This movie is available in high-quality formats:
                <span style="color: #ffa500;"><strong>1080p</strong></span>, 
                <span style="color: #ffa500;"><strong>720p</strong></span>, and 
                <span style="color: #ffa500;"><strong>480p</strong></span>. 
                {imdb_data['title']} is a gripping {imdb_data['genres']} movie that keeps you hooked from start to finish. Now available for streaming and download in {imdb_data['language']}, this film offers stunning visuals and an unforgettable plotline. Don’t miss out on the ultimate cinematic experience with {imdb_data['title']}.
            </p>

            <h3 style="text-align: center; color: #66bb6a; margin-top: 20px;">Watch or Download {imdb_data['title']} in 480p, 720p & 1080p qualities.</h3>
            <ul style="list-style: none; padding: 0; margin: 10px 0 20px;">
                <li><strong>🎬 Full Name:</strong> {imdb_data['title']}</li>
                <li><strong>🗂️ Genres:</strong> {imdb_data['genres']}</li>
                <li><strong>⭐ Rating:</strong> {imdb_data['rating']}</li>
                <li><strong>⏰ Runtime:</strong> {imdb_data['runtime']}</li>
                <li><strong>🗣️ Language:</strong> {imdb_data['language']}</li>
                <li><strong>📅 Released Year:</strong> {imdb_data['release_year']}</li>
                <li><strong>📆 Release Date:</strong> {imdb_data['release_date']}</li>
            </ul>

            <h4 style="text-align: center; color: #ff6347;"><strong>Plot Summary:</strong></h4>
            <p style="text-align: justify; margin-bottom: 20px;">{imdb_data.get('plot', 'No plot available.')}</p>
            
            <hr style="border: 1px solid #444; margin: 20px 0;"/>
            
            <h4 style="text-align: center;"><span style="font-family: 'comic sans ms', sans-serif; color: #ff9900;"><em><strong>: SCREENSHOTS :</strong></em></span></h4>
            {"".join([f'<p style="text-align: center;"><img src="{url}" alt="Screenshot" style="max-width: 100%; margin-bottom: 10px;"></p>' for url in screenshot_images])}

            {"".join([f'''
            <div style="text-align: center;">
                <h5 style="color: #ffffff;"><strong>{button['title']}</strong></h5>
                <a href="{button['url']}" target="_blank" rel="nofollow noopener noreferrer" style="text-decoration: none;">
                    <button class="dwd-button" style="background-color: #2196f3; color: #fff; border: none; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; transition: background 0.3s;">Download Now</button>
                </a>
            </div>
            ''' for button in buttons])}

            <hr style="border: 1px solid #444; margin: 20px 0;"/>

            <h3 style="text-align: center; color: #32cd32;">Wrapping Up ❤️</h3>
            <p style="text-align: center;">Thank you for visiting MovieZapiya. Enjoy the best quality downloads of Movies and TV Series. Don’t forget to share with your friends!</p>
        </div>
        """

        # Create WordPress post
        post_created = create_wordpress_post(extracted_title, CUSTOM_HTML_FORMAT, imdb_data['poster'])
        if post_created:
            await message.reply("Post created successfully!")
        else:
            await message.reply("Failed to create post.")
    
    except Exception as e:
        await message.reply(f"Error: {e}")
        
        
    
