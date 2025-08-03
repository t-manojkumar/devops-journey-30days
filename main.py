import string
import random

# --- In-Memory "Database" ---
# What: A Python dictionary.
# Why: For now, this is the simplest possible way to store our data.
#      The 'key' will be the short_code and the 'value' will be the original_url.
#      Note: This data will be lost every time the script stops. We'll fix this
#      on Day 9 when we add a real database.
url_mapping = {}


def generate_short_code(length=6):
    """
    What: This function generates a random string of a given length.
    Why:  We need a way to create unique, short codes for each URL.
          Using a combination of letters and numbers gives us many possibilities.
    """
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits
    # Generate a random string by choosing 'length' characters from the set
    short_code = ''.join(random.choice(characters) for _ in range(length))
    return short_code


def shorten_url(original_url):
    """
    What: The main function to shorten a URL.
    Why:  This function orchestrates the process. It generates a new code,
          stores the URL and code in our dictionary, and returns the short code.
    """
    short_code = generate_short_code()
    # Make sure the generated code isn't already used (very rare, but good practice)
    while short_code in url_mapping:
        short_code = generate_short_code()

    # Store the mapping
    url_mapping[short_code] = original_url
    print(f"URL '{original_url}' shortened to '{short_code}'")
    return short_code


def get_original_url(short_code):
    """
    What: This function looks up a short code to find the original URL.
    Why:  This is the core of the "redirect" feature. When a user visits
          our short link, this function will find the destination.
    """
    # Return the original URL, or None if the code is not found
    return url_mapping.get(short_code)


# --- Testing Block ---
# What: This special block of code only runs when you execute the script directly.
# Why:  It allows us to test our functions from the command line without this test
#       code running when we import these functions into other files later (like
#       our web server on Day 4). It's a standard Python convention.
if __name__ == "__main__":
    print("--- Testing LinkShorty Core Logic ---")

    # Test the shorten_url function
    my_test_url = "https://www.google.com/search?q=devops"
    generated_code = shorten_url(my_test_url)

    # Test the get_original_url function
    retrieved_url = get_original_url(generated_code)
    print(f"Retrieved URL for '{generated_code}': {retrieved_url}")

    # Test a non-existent code
    non_existent_retrieval = get_original_url("nota_real_code")
    print(f"Retrieved URL for a fake code: {non_existent_retrieval}")

    # Verify that the test was successful
    if my_test_url == retrieved_url:
        print("\n✅ Test successful!")
    else:
        print("\n❌ Test failed!")