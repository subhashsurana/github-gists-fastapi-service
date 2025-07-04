from fastapi import APIRouter, HTTPException, Path
from app.schemas.common import GitHubUsername
import requests
from fastapi_pagination import Page, paginate
from pydantic import BaseModel
import logging

router = APIRouter()

logger = logging.getLogger("uvicorn.error")

class GistSummary(BaseModel):
    id: str
    html_url: str
    description: str | None

@router.get("/{username}", response_model=Page[GistSummary])
async def get_gists(
    username: str = Path(
    ..., 
    min_length=1,
    max_length=39,
    pattern="^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$",
    description="""GitHub username (1-39 characters, alphanumeric and hyphen, cannot start/end with hyphen)
    disallowing '-octocat', 'octocat-,octo--cat', '--octocat', 'octocat--cat','octocat-octo-cat', 'octocat-octo-cat-'""" )
    ):
    """
    Fetch the public gists for a given GitHub username and return a simplified list.
    Username must match GitHub's allowed characters.
    """
    url = f"https://api.github.com/users/{username}/gists"
    try:
        response = requests.get(url, timeout=5)
        logger.info(f"printing the url response: {response}")
        if response.status_code == 404:
            logger.warning(f"GitHub user '{username}' not found.")
            raise HTTPException(status_code=response.status_code, detail=f"GitHub user '{username}' not found.")
        
        elif response.status_code == 403:
            logger.warning(f"Rate limit exceeded for user '{username}'.")
            raise HTTPException(status_code=response.status_code, detail="Rate limit exceeded. Please try again later.")
        
        elif response.status_code != 200:
            logger.error(f"Error fetching gists for {username}: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Error fetching gists from GitHub.") 
               
        gists = response.json()
        
        if not isinstance(gists, list):
            logger.error(f"Invalid response from GitHub for user '{username}': {gists}")
            raise HTTPException(status_code=502, detail="Invalid response from GitHub API.")
        
        result = [
            GistSummary(
                id=gist.get("id"),
                html_url=gist.get("html_url"),
                description=gist.get("description")
            )
            for gist in gists
        ]
        
        if not result:
            logger.info(f"User '{username}' has no gists or doesn't exist.")
            raise HTTPException(status_code=404, detail=f"No gists found for GitHub user '{username}'.")
        
        return paginate(result)
    
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching gists for user '{username}'")
        raise HTTPException(status_code=504, detail="GitHub API timed out.")
    
    except requests.RequestException as e:
        logger.error(f"Unexpected error while contacting GitHub {username}: {e}")
        raise HTTPException(status_code=502, detail="Error communicating with GitHub API.")
    
    except HTTPException:
         # re-raise known HTTP errors as-is
        raise
    
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")
