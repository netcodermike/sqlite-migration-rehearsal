import sqlite3
from pathlib import Path
p=Path('examples/demo.sqlite')
if not p.exists():
 with sqlite3.connect(p)as db:db.execute('CREATE TABLE notes(id INTEGER PRIMARY KEY,title TEXT)');db.execute("INSERT INTO notes(title)VALUES('Synthetic note')")
print('Synthetic database ready')
