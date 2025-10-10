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
        """
        print("search_by_barcode")
        try:
            print(f"Searching for barcode: {barcode}")
            url = f"{self.BASE_URL}/release"
            params = {
                "query": f"barcode:{barcode}",
                "fmt": "json",
                "limit": 1
            }

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            print(data)
            return None
        except Exception as e:
            print(f"Error searching for barcode {barcode}: {e}")
            return None

        
    
    async def close(self):
        """
        Close the HTTP client
        """
        await self.client.aclose()

musicbrainz_service = MusicBrainzService()


