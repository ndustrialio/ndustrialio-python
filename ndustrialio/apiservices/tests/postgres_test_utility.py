import os

def initializeTestData(db_con, psql_setup_file=None):
    if psql_setup_file:
        with db_con.cursor() as cur:
            cur.execute(fileRead(psql_setup_file))

def fileRead(path):
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, path)
    with open(file_path, 'r') as f:
        return f.read()

def executeQuery(db_con, query):
    rows = []
    with db_con.cursor() as cur:
        cur.execute(query)
        try:
            rows = cur.fetchall()
        except Exception:
            pass
    return rows