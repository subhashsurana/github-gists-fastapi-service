# GitHub Gists FastAPI Service

This FastAPI-based microservice allows users to fetch and paginate public GitHub gists for any given GitHub username. It validates input, gracefully handles errors like rate-limiting and user-not-found, and returns a clean, paginated response.

## 🚀 Features

#### ✅ Fetch public gists for any valid GitHub username

#### 🔄 Pagination using fastapi-pagination

#### 🧪 Pytest-based test suite with mocking and validation

#### 🔐 Username input validation using reusable Pydantic constraints

#### 🛡️ Handles errors (e.g., invalid usernames, GitHub API rate limits, non-existent users)

#### ⚙️ Dockerized (secured and minimal image)

## Project Structure

```
fastapi-project
├── app
│   ├── main.py               # FastAPI app entrypoint
│   ├── api
│   │   └── routes.py         # API routes definition
│   ├── models
│   │   └── __init__.py       # Data models
│   ├── schemas
│   │   └── __init__.py       # Pydantic schemas for data validation
|   |   └── common.py         # Shared validators (e.g., GitHubUsername)
│   └── dependencies
│       └── __init__.py       # Reusable dependencies
├── tests
│   └── test_main.py          # Unit tests with pytest + monkeypatch
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Files to ignore in version control
```

## Setup & Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-user/github-gists-fastapi-service.git
   cd github-gists-fastapi-service
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install the required dependencies:
   ```bash 
   pip install -r requirements.txt
   ```

## Running the Application

To run this FastAPI application, execute below command:
   ```bash
   uvicorn app.main:app --reload
   ```
Visit `http://127.0.0.1:8080` in your browser to access the application. The interactive API documentation can be found at `http://127.0.0.1:8080/docs` (Interactive Swagger UI).

## Testing

To run the tests, use the following command:
```bash
python -m pytest -v
```
You can also generate coverage reports or integrate with GitHub Actions CI/CD.

## License

This project is licensed under the MIT License.

## API Usage

Endpoint

`GET /{username}`

📅 Path Parameters:

`username: GitHub username` (must match GitHub's naming rules)

Example:

`GET /octocat`

Response (Paginated):
```yaml
{
  "items": [
    {
      "id": "6cad326836d38bd3a7ae",
      "html_url": "https://gist.github.com/octocat/6cad326836d38bd3a7ae",
      "description": "Hello world!"
    }
  ],
  "total": 12,
  "page": 1,
  "size": 50,
  "pages": 1
```
## Input Validation

Usernames must:

- Be 1 to 39 characters long

- Use only letters, numbers, and hyphens

- Not start or end with a hyphen

- Not have consecutive hyphens

- Regex enforced via reusable Pydantic constraint in schemas/common.py:

`pattern=r"^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"`

## Error Handling

| Scenario | Status Code | Message |
| :--- | :---: | :--- |
| Invalid username format | `422` | Invalid input. Please check the username or query parameters. |
| GitHub user not found | `404` | GitHub user 'xyz' not found. |
| No gists for valid user | `404` | No gists found for GitHub user 'xyz'. |
| GitHub rate limit exceeded | `403` | Rate limit exceeded. Please try again later. |
| GitHub API timeout/unreachable | `502`  | Error communicating with GitHub API. |
| GitHub API timeout/unreachable | `504` | GitHub API timed out. |


## GitHub Token Auth
To prevent hitting GitHub rate limits for unauthenticated API requests, you can inject a GitHub token via environment variable 
```bash
export GITHUB_TOKEN=your_personal_access_token
```

## Docker (Optional)

Build & run:

```bash
docker build -t github-gists-api-svc:v1 .
docker run -p 8080:8080 --name github-gists-api-svc github-gists-api-svc:v1
```