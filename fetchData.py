import os
import django
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gutendex.settings")
django.setup()

import requests
from books.models import Book, Person
from bs4 import BeautifulSoup  # Used to scrape HTML pages

# Delete the records from the junction table (Many-to-Many)
Book.authors.through.objects.all().delete()

# Now you can delete all books
Book.objects.all().delete()

# Optionally, delete records from the Person table if you want to clear authors too
Person.objects.all().delete()

##definition to fetch the data of the books
def fetch_books():
    # URL of the Gutendex API with a limit of 100 per pag
    url = "https://gutendex.com/books/?limit=100"
    
    books_collected = []
    
    while len(books_collected) < 100:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            books_collected.extend(data.get('results', []))  # Collect books from current page
            
            if len(books_collected) >= 100:
                break  # Stop when we reach 1000 books
            
            # Update the URL to the next page if there is one
            url = data.get('next')
            if not url:  # If there is no next page, stop
                break
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break
    
    return books_collected
books_data = fetch_books()

# Print the first 300 charachters of fetched data (optional, just a check)
if books_data:
    print(str(books_data)[:300])

##Definition to fetch the cover image of each book (scrape gutenberg)
def fetch_cover_image(url):
    # Send a request to the page
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        return None  # or handle error appropriately
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the image tag with class 'cover-art'
    img_tag = soup.find('img', {'class': 'cover-art'})
    
    # If the image tag exists and has the 'src' attribute
    if img_tag and img_tag.has_attr('src'):
        return img_tag['src']
    
    # If no valid image is found, return None
    return None

##insert the fetched data (cover images and books data)
def insert_books(data):
    for item in data:  # Loop through the books in the response
        book_data = {
            "gutenberg_id": item.get('id'),
            "title": item.get('title'),
            "gutenberg_url": f"https://www.gutenberg.org/ebooks/{item.get('id')}",  # Add the Gutenberg URL here
        }

       # Fetch the cover image
        gutenberg_id = item.get('id')
        gutenberg_url = f"https://www.gutenberg.org/ebooks/{gutenberg_id}"  # Full URL to fetch image
        cover_image = fetch_cover_image(gutenberg_url)
        if cover_image:
            print(f"Cover image for {book_data['title']}: {cover_image}")
            book_data["cover_image_url"] = cover_image  # Save cover image URL

        with transaction.atomic():
            # Check if the book already exists in the database
            book, created = Book.objects.get_or_create(
                gutenberg_id=book_data["gutenberg_id"], 
                defaults=book_data
            )
            if not created:
                print(f"Book with gutenberg_id {book_data['gutenberg_id']} already exists. Updating URL.")

            book.gutenberg_url = book_data["gutenberg_url"]  # Update the URL
            book.cover_image_url = book_data.get("cover_image_url")  # Ensure cover_image_url is updated
            book.save()  # Save the updated book

            authors_list = []  # Empty list for authors
            # Loop through the authors and create or get Author instances
            for author_data in item.get('authors', []):
                # Create or retrieve the Author instance
                author_name = author_data.get('name')  # This is where the error occurred
                author, created = Person.objects.get_or_create(name=author_name)
                authors_list.append(author)


            # Add authors to the book's authors field (ManyToMany relationship)
            book.authors.set(authors_list)

    print("Books inserted successfully!")

    # Main execution block
if __name__ == "__main__":
    # Fetch books data from the API
    books_data = fetch_books()

    # Insert the fetched books data into the database
    if books_data:
        insert_books(books_data)