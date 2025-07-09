from pydantic import constr

# GitHub username must:
# - be 1-39 characters
# - contain only a-zA-Z0-9 and hyphens
# - not start or end with a hyphen
# - not have consecutive hyphens (optional strictness)
# - disallowing '-octocat', 'octocat-,octo--cat', '--octocat', 'octocat--cat','octocat-octo-cat', 'octocat-octo-cat-'
GitHubUsername = constr(
    min_length=1,
    max_length=39,
    pattern=r"^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"
               
)
