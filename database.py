import sqlite3


class ActivityDatabase:
    def __init__(self, db_name='activities.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY,
        type TEXT,
        activity TEXT NOT NULL,
        participants INTEGER,
        price FLOAT,
        link TEXT,
        key TEXT,
        accessibility FLOAT
        );        
        '''
        self.conn.execute(query)
        self.conn.commit()

    def save_activity(self, activity_data):
        query = '''
            INSERT INTO activities (activity, type, participants, price, link, key, accessibility)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        self.conn.execute(query, (
            activity_data['activity'],
            activity_data['type'],
            activity_data['participants'],
            activity_data['price'],
            activity_data['link'],
            activity_data['key'],
            activity_data['accessibility']
        ))
        self.conn.commit()

    def get_latest_activities(self, limit=5):
        query = '''
            SELECT * FROM activities ORDER BY id DESC LIMIT ?
        '''
        cursor = self.conn.execute(query, (limit,))
        return cursor.fetchall()

    def close_connection(self):
        self.conn.close()
