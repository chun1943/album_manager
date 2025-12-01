import httpx
from typing import Optional, Dict, Any
import asyncio

class MusicBrainzService:
    BASE_URL = "https://musicbrainz.org/ws/2"

    def __init__(self):
        self.client = httpx.AsyncClient(
            headers = {
                "User-Agent": "AlbumScanner/1.0 (jane42242002@gmail.com)"
            },
            timeout=10.0
        )

    async def search_by_barcode(self, barcode: str) -> Optional[Dict]:
        """
        Search for an album by barcode using MusicBrainz API
        Returns a structured dict with album information or None if not found
        """
        try:
            url = f"{self.BASE_URL}/release"
            params = {
                "query": f"barcode:{barcode}",
                "fmt": "json",
                "limit": 1
            }

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if any releases found
            if not data.get("releases") or len(data["releases"]) == 0:
                return None
            
            release = data["releases"][0]
            
            # Extract title
            title = release.get("title", "")
            
            # Extract artist from artist-credit array
            artist = "Unknown Artist"
            artist_credits = release.get("artist-credit", [])
            if artist_credits and len(artist_credits) > 0:
                artist_names = []
                for credit in artist_credits:
                    if isinstance(credit, dict) and "name" in credit:
                        artist_names.append(credit["name"])
                    elif isinstance(credit, dict) and "artist" in credit:
                        artist_obj = credit.get("artist", {})
                        artist_names.append(artist_obj.get("name", ""))
                artist = ", ".join(artist_names) if artist_names else "Unknown Artist"
            
            # Extract year from date (format: YYYY-MM-DD or YYYY-MM or YYYY)
            year = None
            date_str = release.get("date", "")
            if date_str:
                try:
                    year = int(date_str.split("-")[0])
                except (ValueError, IndexError):
                    pass
            
            # Extract genre from release-group (if available)
            genre = None
            release_group = release.get("release-group", {})
            if release_group:
                genres = release_group.get("genres", [])
                if genres and len(genres) > 0:
                    genre = genres[0].get("name", None)
            
            # Build cover URL from Cover Art Archive
            # Format: https://coverartarchive.org/release/{release_id}/front
            cover_url = None
            release_id = release.get("id")
            if release_id:
                cover_url = f"https://coverartarchive.org/release/{release_id}/front"
            
            return {
                "id": release_id or barcode,
                "title": title,
                "artist": artist,
                "year": year,
                "barcode": barcode,
                "cover_url": cover_url,
                "genre": genre or "Unknown"
            }
        except Exception as e:
            print(f"Error searching for barcode {barcode}: {e}")
            return None

        
    
    async def close(self):
        """
        Close the HTTP client
        """
        await self.client.aclose()




