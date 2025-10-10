"""
API service for handling communication with the backend
"""
import httpx
from typing import Dict, List, Any, Optional, Tuple
from core.config import API_URL, API_TIMEOUT


class APIService:
    """Service class for handling API requests"""
    
    def __init__(self):
        self.base_url = API_URL
        self.timeout = API_TIMEOUT
    
    def request(self, endpoint: str, data: Optional[Dict] = None, 
               method: str = "post", timeout: Optional[float] = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Make API requests with consistent error handling
        
        Args:
            endpoint: API endpoint (without the base URL)
            data: Dictionary of data to send (for POST requests)
            method: HTTP method (default: post)
            timeout: Request timeout in seconds (defaults to API_TIMEOUT)
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        if timeout is None:
            timeout = self.timeout
            
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.lower() == "post":
                response = httpx.post(url, json=data, timeout=timeout)
            elif method.lower() == "get":
                response = httpx.get(url, params=data, timeout=timeout)
            else:
                return False, None, f"Unsupported HTTP method: {method}"
            
            if response.status_code == 200:
                return True, response.json(), None
            else:
                return False, None, f"API error: {response.status_code} - {response.text}"
                
        except httpx.TimeoutException:
            return False, None, f"API request timed out after {timeout} seconds. The server might be busy or unreachable."
        except httpx.ConnectError:
            return False, None, "Cannot connect to API server. Please check if the server is running."
        except Exception as e:
            return False, None, f"Error connecting to API: {str(e)}"


# Global instance for backward compatibility
def api_request(endpoint, data=None, method="post", timeout=None):
    """
    Helper function to make API requests with consistent error handling
    (Legacy function for backward compatibility)
    """
    api_service = APIService()
    return api_service.request(endpoint, data, method, timeout)
