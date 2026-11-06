# Using SQLite Migration Rehearsal

## Quick start

Run `python app.py database.sqlite migration.sql`. The source opens read-only and is backed up to a temporary database before SQL runs. The tool never applies changes to the source. ATTACH/DETACH are denied.

## Supported workflow

1. SQLite backup API to a temporary copy.
2. Schema diff and post-migration row counts.
3. Read-only original and blocked ATTACH/DETACH.

## Validation and troubleshooting

Run the commands in the README. Invalid inputs produce explicit errors rather than silently changing the requested operation. Browser audio requires a user gesture; microphone apps require HTTPS or localhost and permission. For file tools, supply supported input formats and writable output directories.

## Limitations

Rehearses trusted SQLite SQL only; does not apply migrations to production or validate other database engines. Large files require temporary disk space.

Tests use synthetic fixtures. These tests do not certify hardware compatibility, real-world forecast quality, trained-model accuracy, or production suitability for every input.
