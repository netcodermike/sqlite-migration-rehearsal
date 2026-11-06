ALTER TABLE notes ADD COLUMN archived INTEGER NOT NULL DEFAULT 0;
CREATE INDEX notes_title_idx ON notes(title);
