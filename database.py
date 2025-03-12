import sqlite3

def create_database():
    conn = sqlite3.connect('projects.db')
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
    conn.close()

def insert_sample_data():
    conn = sqlite3.connect('projects.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO projects (project_id, description) VALUES (1, 'Downtown commercial building')")
    c.execute("INSERT OR IGNORE INTO projects (project_id, description) VALUES (2, 'Coastal residential development')")
    c.execute("INSERT OR IGNORE INTO incidents (project_id, incident_type, description, severity, mitigation_actions, outcome) "
              "VALUES (1, 'Safety', 'Crane malfunction', 'High', 'Repaired crane', 'No injuries')")
    conn.commit()
    conn.close()