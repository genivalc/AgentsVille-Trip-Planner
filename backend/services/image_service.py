import requests
from typing import List, Optional, Dict
import os

class ImageService:
    def __init__(self, unsplash_access_key: Optional[str] = None):
        self.unsplash_access_key = unsplash_access_key or os.getenv("UNSPLASH_ACCESS_KEY")
        self.base_url = "https://api.unsplash.com"

    def search_location_images(self, location: str, count: int = 5) -> List[Dict]:
        """Busca imagens de um local específico"""
        if not self.unsplash_access_key:
            return self._get_placeholder_images(location, count)

        try:
            headers = {"Authorization": f"Client-ID {self.unsplash_access_key}"}
            params = {
                "query": f"{location} travel tourism",
                "per_page": count,
                "orientation": "landscape"
            }
            
            response = requests.get(
                f"{self.base_url}/search/photos",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for photo in data.get("results", []):
                    images.append({
                        "id": photo["id"],
                        "url": photo["urls"]["regular"],
                        "thumb_url": photo["urls"]["thumb"],
                        "description": photo.get("description") or photo.get("alt_description", ""),
                        "photographer": photo["user"]["name"],
                        "photographer_url": photo["user"]["links"]["html"]
                    })
                
                return images
            
        except Exception as e:
            print(f"Erro ao buscar imagens: {e}")
        
        return self._get_placeholder_images(location, count)

    def get_activity_images(self, activity_name: str, location: str, count: int = 3) -> List[Dict]:
        """Busca imagens relacionadas a uma atividade específica"""
        query = f"{activity_name} {location}"
        return self.search_location_images(query, count)

    def _get_placeholder_images(self, location: str, count: int) -> List[Dict]:
        """Retorna imagens placeholder quando a API não está disponível"""
        placeholder_images = []
        
        for i in range(count):
            placeholder_images.append({
                "id": f"placeholder_{i}",
                "url": f"https://picsum.photos/800/600?random={hash(location + str(i)) % 1000}",
                "thumb_url": f"https://picsum.photos/200/150?random={hash(location + str(i)) % 1000}",
                "description": f"Beautiful view of {location}",
                "photographer": "Placeholder",
                "photographer_url": "https://picsum.photos"
            })
        
        return placeholder_images

    def get_destination_gallery(self, destination: str) -> Dict:
        """Retorna uma galeria completa de imagens do destino"""
        return {
            "destination": destination,
            "images": self.search_location_images(destination, 10),
            "featured_image": self.search_location_images(f"{destination} landmark", 1)[0] if self.search_location_images(f"{destination} landmark", 1) else None
        }
