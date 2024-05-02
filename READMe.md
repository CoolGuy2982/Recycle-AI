# Recycle-AI

Recycle-AI is a web application designed to assist users in identifying recyclable objects and providing information on how to recycle them properly. Utilizing a camera interface, users can capture images of waste items, which are then analyzed using AI to determine their recyclability.

## Features

- **Camera Capture**: Allows users to take pictures of waste items for analysis.
- **AI-Powered Analysis**: Analyzes images to identify materials and provide recycling information.
- **Google Maps Integration**: Shows nearby recycling centers based on the items' materials.
- **Educational Resources**: Offers DIY videos and guides on recycling processes.

## Setup
To run this project, you will need to install the following dependencies:

```markdown
pip install -r requirements.txt
```

Make sure to set your environment variables in the `.env` file:

```env
GOOGLE_API_KEY= your gemini key here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

Activate the virtual environment:

```bash
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

Run the application:

```bash
run app.py
```

## Project Structure

```
RECYCLE-AI/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   ├── templates/
│   ├── __init__.py
│   ├── routes.py
│   ├── utils.py
├── .env
├── .gitignore
├── app.py
├── LICENSE
├── README.md
├── requirements.txt
```

- `app/`: Contains the Flask application.
- `static/`: Stores CSS and JavaScript files.
- `templates/`: Holds the HTML templates.
- `.env`: Stores configuration and secret keys.
- `.gitignore`: Lists files to be ignored by git.
- `app.py`: Entry point to the Flask application.
- `LICENSE`: License file.
- `requirements.txt`: List of Python dependencies.

## Usage

Navigate to the home page and use the camera interface to take a picture of the item you want to recycle. The AI will analyze the image and provide information on the recyclability of the item, educational resources, and a map showing nearby recycling centers.

## License

This project is licensed under the MIT License - see the License file for details.
