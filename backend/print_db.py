import sqlite3

DB_FILE = "app.db"

def fetch_data_from_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("---- Events Data ----")
    cursor.execute("SELECT title, date, booking_link FROM events")
    events = cursor.fetchall()
    for event in events:
        print(f"Title: {event[0]}, Date: {event[1]}, Booking Link: {event[2]}")
    
    print("\n---- Emails Data ----")
    cursor.execute("SELECT email FROM emails")
    emails = cursor.fetchall()
    for email in emails:
        print(f"Email: {email[0]}")

    conn.close()

if __name__ == "__main__":
    fetch_data_from_db()
