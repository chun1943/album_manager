# Integration Points and External Dependencies

## External Services

| Service      | Purpose              | Integration Type | Key Files                    |
| ------------ | -------------------- | ---------------- | ---------------------------- |
| MusicBrainz  | Album metadata lookup| REST API         | `musicbrainz_service.py`     |
| Cover Art Archive | Album covers    | HTTP URL         | Referenced in service (not directly called) |

**MusicBrainz Integration Details:**
- Base URL: `https://musicbrainz.org/ws/2`
- Endpoint: `/release` with query parameter `barcode:{barcode}`
- User-Agent: Required (set to "AlbumScanner/1.0 (jane42242002@gmail.com)")
- Timeout: 10 seconds
- Response: JSON with release information
- **Current Behavior**: Extracts title, artist, year, genre, cover_url but only title/artist are used

**Cover Art Archive:**
- URL Pattern: `https://coverartarchive.org/release/{release_id}/front`
- **Note**: URL is constructed but not validated or stored

## Internal Integration Points

- **Frontend Communication**: REST API on port 8000 (configurable via PORT env var)
- **Database**: SQLite (default) or PostgreSQL (via DATABASE_URL env var)
- **No Background Jobs**: All processing is synchronous
- **No Caching**: Every request hits database/external API
