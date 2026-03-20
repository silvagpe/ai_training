"""Minimal GitHub API client for pull request reviews."""
import json
from typing import Any, Dict, List, Optional
from urllib import error, parse, request


class GitHubAPIError(RuntimeError):
    """Raised when GitHub API returns an unexpected response."""


class GitHubClient:
    """Simple GitHub REST client using urllib from the standard library."""

    def __init__(self, token: str, api_url: str = "https://api.github.com") -> None:
        self.token = token
        self.api_url = api_url.rstrip("/")

    def _request(
        self,
        method: str,
        path: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        full_url: Optional[str] = None,
        accept: str = "application/vnd.github+json",
    ) -> Any:
        url = full_url if full_url else f"{self.api_url}/{path.lstrip('/')}"
        data = None
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": accept,
            "User-Agent": "ai-code-review-bot",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = request.Request(url=url, data=data, method=method, headers=headers)

        try:
            with request.urlopen(req, timeout=20) as response:
                body = response.read().decode("utf-8")
                if not body:
                    return None
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return json.loads(body)
                return body
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise GitHubAPIError(
                f"GitHub API request failed ({exc.code}) for {method} {url}: {detail}"
            ) from exc
        except error.URLError as exc:
            raise GitHubAPIError(f"GitHub API network error for {method} {url}: {exc}") from exc

    def list_pull_request_files(self, repository: str, pr_number: int) -> List[Dict[str, Any]]:
        """List changed files in a pull request with pagination."""
        files: List[Dict[str, Any]] = []
        page = 1
        per_page = 100

        while True:
            query = parse.urlencode({"per_page": per_page, "page": page})
            path = f"repos/{repository}/pulls/{pr_number}/files?{query}"
            chunk = self._request("GET", path=path)

            if not isinstance(chunk, list):
                raise GitHubAPIError("Unexpected GitHub response when listing pull request files")

            files.extend(chunk)
            if len(chunk) < per_page:
                break
            page += 1

        return files

    def download_raw_file(self, raw_url: str) -> str:
        """Download raw file content from GitHub."""
        data = self._request(
            "GET",
            full_url=raw_url,
            accept="application/vnd.github.raw",
        )
        if not isinstance(data, str):
            raise GitHubAPIError("Unexpected content type when downloading raw file")
        return data

    def create_pull_request_review(
        self,
        repository: str,
        pr_number: int,
        body: str,
        comments: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Create a pull request review with optional inline comments."""
        payload: Dict[str, Any] = {
            "event": "COMMENT",
            "body": body,
        }
        if comments:
            payload["comments"] = comments

        response = self._request(
            "POST",
            path=f"repos/{repository}/pulls/{pr_number}/reviews",
            payload=payload,
        )
        if not isinstance(response, dict):
            raise GitHubAPIError("Unexpected GitHub response when creating pull request review")
        return response
