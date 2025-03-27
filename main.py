from flask import Flask, Response
from datetime import datetime
import enhanced_newsletter
import os

app = Flask(__name__)

@app.route('/')
def run_script():
    today = datetime.now().strftime('%Y%m%d')
    # Assuming the JSON files are in the 'docs' subdirectory
    input_file = os.path.join('docs', f'full_articles_{today}.json') 

    try:
        # Check if the input file exists
        if not os.path.exists(input_file):
            return f"Error: Input file not found at {input_file}", 404

        # Call the function from your script
        # It returns (output_filename, newsletter_content)
        output_filename, newsletter_content = enhanced_newsletter.create_newsletter(input_file)
        
        # Return the newsletter content with a plain text content type
        return Response(newsletter_content, mimetype='text/plain')

    except FileNotFoundError:
         return f"Error: Input file not found at {input_file}", 404
    except Exception as e:
        # Log the error for debugging (optional, good practice)
        app.logger.error(f"Error running newsletter script: {e}") 
        return f"An error occurred: {e}", 500

# Note: Gunicorn will run the app, so the __main__ block 
# for app.run() is not strictly needed for Render deployment,
# but can be useful for local testing.
# if __name__ == '__main__':
#     app.run(debug=True)