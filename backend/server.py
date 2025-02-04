from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)
CORS(app)

events = []

def scrape_events():
    global events
    try:
        url = "https://allevents.in/sydney/all?ref=new-cityhome-popular"
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/58.0.3029.110 Safari/537.3')
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Handle HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        events_container = soup.select_one("ul.event-card-parent")
        if not events_container:
            print("Events container not found")
            return

        events = []

        for event in events_container.find_all('li', class_='event-card'):
            title_tag = event.find('h3')
            title = title_tag.text.strip() if title_tag else ''

            date_tag = event.find('div', class_='date')
            date = date_tag.text.strip() if date_tag else ''

            booking_link = event.get('data-link', '')

            if title and date and booking_link:
                events.append({
                    'title': title,
                    'date': date,
                    'booking_link': booking_link
                })
        print("Events scraped successfully")
    except requests.RequestException as e:
        print(f"Error fetching events: {e}")
    except Exception as e:
        print(f"Error scraping events: {e}")

scrape_events()

scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_events, trigger="interval", hours=24)
scheduler.start()

@app.route('/api/events')
def get_events():
    return jsonify(events)

@app.route('/api/submit-email', methods=['POST'])
def submit_email():
    data = request.json
    email = data.get('email')
    print(f"Email submitted: {email}")
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
