from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing


app = Flask(__name__)
CORS(app)  # Initialize CORS

# ... rest of your API code


@app.route('/', methods=['GET', 'POST'])
def receive_string():
    if request.method == 'POST':
        input_string = request.form['input_string']

        # Fetch results from Zenserp API
        zenserp_api_key = '637b6190-ad5d-11ee-8eb6-2b7976ea59ec'  # Replace with your API key
        zenserp_url = f'https://app.zenserp.com/api/v2/search?q={input_string}&apikey={zenserp_api_key}'
        response = requests.get(zenserp_url)
        if response.status_code == 200:
            zenserp_data = response.json()  # Parse the JSON data
            # processed_data = "zenserp api has successed"
            processed_data = extract_relevant_results(zenserp_data)
            print(zenserp_data)
        else :
            processed_data = "zenserp api has failed"

        # processed_data = perform_operations(input_string)  # Replace with your operations
        return jsonify({'response': processed_data})  # Return processed data as JSON
        # return processed_data
    else:
        return 'Please send a POST request with the string data.'

# Function to extract relevant data from Zenserp response
def extract_relevant_results(zenserp_data):
    # Customize this function to extract the data you want to display
    results = []
    print(zenserp_data)
    for organic_result in zenserp_data['organic']:
        try: 
            link = organic_result['url']            
            response = requests.get(link)
            print(response.status_code)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')  # Parse HTML using BeautifulSoup

            # Extract desired elements from the HTML (example: title and main content)
            title = soup.find('title').text
            extracted_link = [a['href'] for a in soup.find_all('a', href=True)][:5]   # Extract HREF properties from <a> tags
            extracted_text = soup.get_text(separator=' ', strip=True)   # Extract text from HTML also remove all tags 
            text_words = extracted_text.split()[:100]
            result_text = ' '.join(text_words)
            result = {
                'title': title,
                'link': link,
                'Elink': extracted_link,
                'Etext': result_text,
                
            }
            results.append(result)
        except requests.exceptions.RequestException as e:
                print(f"Error fetching HTML from : {e}")
        if (len(results) == 3):
            break    

    return results

if __name__ == '__main__':
    app.run(debug=True)




