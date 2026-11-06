import argparse,json,sqlite3,tempfile,unittest
from pathlib import Path
from urllib.parse import quote
def schema(db):return {r[0]:r[1]for r in db.execute("SELECT name,sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY name")}
def rehearse(source,script):
 uri='file:'+quote(Path(source).resolve().as_posix(),safe='/:')+'?mode=ro'
 with tempfile.TemporaryDirectory()as d:
  with sqlite3.connect(uri,uri=True)as src,sqlite3.connect(str(Path(d)/'rehearsal.sqlite'))as db:
   src.backup(db);before=schema(db)
   db.set_authorizer(lambda action,*args:sqlite3.SQLITE_DENY if action in(sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH)else sqlite3.SQLITE_OK)
   db.executescript(script);after=schema(db);tables={name:db.execute('SELECT COUNT(*) FROM "'+name.replace('"','""')+'"').fetchone()[0]for name, in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
   return {'mode':'temporary-copy rehearsal; source opened read-only','added':{k:v for k,v in after.items()if k not in before},'removed':[k for k in before if k not in after],'changed':{k:v for k,v in after.items()if k in before and before[k]!=v},'row_counts_after':tables}
class Tests(unittest.TestCase):
 def test_copy_and_attach(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'source.sqlite'
   with sqlite3.connect(p)as db:db.execute('CREATE TABLE notes(id INTEGER)');db.execute('INSERT INTO notes VALUES(1)')
   r=rehearse(p,'ALTER TABLE notes ADD COLUMN title TEXT;');self.assertIn('notes',r['changed'])
   with sqlite3.connect(p)as db:self.assertEqual(len(db.execute('PRAGMA table_info(notes)').fetchall()),1)
   with self.assertRaises(sqlite3.DatabaseError):rehearse(p,"ATTACH DATABASE ':memory:' AS other;")
if __name__=='__main__':
 p=argparse.ArgumentParser(description='Rehearse trusted SQL on a throwaway database copy');p.add_argument('database',nargs='?');p.add_argument('migration',nargs='?');p.add_argument('--self-test',action='store_true');a=p.parse_args()
 if a.self_test:unittest.main(argv=['migration'])
 elif a.database and a.migration:print(json.dumps(rehearse(a.database,Path(a.migration).read_text(encoding='utf-8')),indent=2))
 else:p.error('database and migration SQL file required')
