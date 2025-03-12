import sqlite3

def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect('projects.db')

def create_database():
    """Create the database schema with projects and incidents tables."""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS projects (
                            project_id INTEGER PRIMARY KEY,
                            description TEXT)''')
            c.execute('''CREATE TABLE IF NOT EXISTS incidents (
                            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            project_id INTEGER,
                            incident_type TEXT,
                            description TEXT,
                            severity TEXT,
                            mitigation_actions TEXT,
                            outcome TEXT,
                            FOREIGN KEY (project_id) REFERENCES projects(project_id))''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

def insert_sample_data():
    """Insert sample data into projects and incidents tables."""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO projects (project_id, description) VALUES (1, 'Downtown commercial building')")
            c.execute("INSERT OR IGNORE INTO projects (project_id, description) VALUES (2, 'Coastal residential development')")
            c.execute("INSERT OR IGNORE INTO incidents (project_id, incident_type, description, severity, mitigation_actions, outcome) "
                      "VALUES (1, 'Safety', 'Crane malfunction', 'High', 'Repaired crane', 'No injuries')")
            c.execute("INSERT OR IGNORE INTO incidents (project_id, incident_type, description, severity, mitigation_actions, outcome) "
                      "VALUES (2, 'Delay', 'Weather-related delays', 'Medium', 'Adjusted schedule', 'Minor delay')")
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting sample data: {e}")

def get_training_data():
    """Retrieve project descriptions and associated incident types for training."""
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT p.description, GROUP_CONCAT(i.incident_type) FROM projects p JOIN incidents i ON p.project_id = i.project_id GROUP BY p.project_id")
            data = c.fetchall()
        return [(desc, types.split(',')) for desc, types in data]
    except sqlite3.Error as e:
        print(f"Error retrieving training data: {e}")
        return []