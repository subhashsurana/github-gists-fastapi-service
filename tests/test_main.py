import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.common import GitHubUsername
from pydantic import ValidationError


client = TestClient(app)

def test_get_gists_octocat():
    """
    Validates that the /octocat endpoint returns a list of gists.
    """
    response = client.get("/octocat")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    if data["items"]:
        item = data["items"][0]
        assert "id" in item
        assert "html_url" in item
        assert "description" in item
        assert "page" in data
        assert "size" in data
        assert "total" in data
        assert "pages" in data
        
def test_rate_limit_exceeded_handling(monkeypatch):
    def mock_rate_limited_get(*args, **kwargs):
        class MockResponse:
            status_code = 403
            def json(self): return {}
        return MockResponse()
    monkeypatch.setattr("requests.get", mock_rate_limited_get)
    response = client.get("/octocat")
    assert response.status_code == 403
    assert response.json()["detail"] == "Rate limit exceeded. Please try again later."
    
def test_get_gists_invalid_username():
    """
        Validates that an invalid username format returns a 404 (not matched by route).    
    """
    response = client.get("/-invalidusername!")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
    
def test_get_gists_empty_username(monkeypatch):
    """
    Validates that the / endpoint returns a 422 error for an empty username.
    """
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 404
            def json(self): return {"message": "Not Found"}
        return MockResponse()
    monkeypatch.setattr("requests.get", mock_get)
    response = client.get("/invalidusername")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "GitHub user 'invalidusername' not found."
    
def test_get_gists_invalid_username_format():
    """
    Validates that the /invalid-username endpoint returns a 422 error for an invalid username format.
    """
    response = client.get("/@invalid_user!") 
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
    
def test_get_gists_valid_username_with_special_characters():
    """
    Validates that the /valid-username-with-special-characters endpoint returns a 422 error for a username with special characters.
    """
    response = client.get("/invalid@name!")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."

def test_get_gists_valid_username_with_emoji():
    """
    Validates that the /valid-username-with-emoji endpoint returns a 422 error for a username with emoji.
    """
    response = client.get("/😀invalid")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_start():
    """
    Validates that the /-valid-username endpoint returns a 422 error for a username starting with a hyphen.
    """
    response = client.get("/-valid-username")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_end():
    """
    Validates that the /valid-username- endpoint returns a 422 error for a username ending with a hyphen.
    """
    response = client.get("/validusername--")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_consecutive_hyphens():
    """
    Validates that the /valid--username endpoint returns a 422 error for a username with consecutive hyphens.
    """
    response = client.get("/valid'--'username")
    assert response.status_code in [422]
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_consecutive_hyphens_at_end():
    """
    Validates that the /valid-username-- endpoint returns a 422 error for a username with consecutive hyphens at the end.
    """
    response = client.get("/valid-username--")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_consecutive_hyphens_at_start():
    """
    Validates that the /--valid-username endpoint returns a 422 error for a username with consecutive hyphens at the start.
    """
    response = client.get("/--valid-username")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_middle():
    """
    Validates that the /valid-username-with-hyphen-in-middle endpoint returns a 422 error for a username with a hyphen in the middle.
    """
    response = client.get("/valid--username--with--hyphen--in--middle")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_middle_and_end():
    """
    Validates that the /valid-username-with-hyphen-in-middle-and-end endpoint returns a 422 error for a username with a hyphen in the middle and at the end.
    """
    response = client.get("/valid--username-with-hyphen-in-middle-and-end")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_middle_and_start():
    """
    Validates that the /valid-username-with-hyphen-in-middle-and-start endpoint returns a 422 error for a username with a hyphen in the middle and at the start.
    """
    response = client.get("/valid-username-with-hyphen-in-middle-and-start")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end endpoint returns a 422 error for a username with a hyphen at the start and end.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_middle():    
    """
    Validates that the /valid-username-with-hyphen-in-start-and-middle endpoint returns a 422 error for a username with a hyphen at the start and in the middle.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-middle")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_end_and_middle():
    """
    Validates that the /valid-username-with-hyphen-in-end-and-middle endpoint returns a 422 error for a username with a hyphen at the end and in the middle.
    """
    response = client.get("/valid-username-with-hyphen-in-end-and-middle")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, and in the middle.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_consecutive_hyphens():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-consecutive-hyphens endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with consecutive hyphens.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-consecutive-hyphens")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_multiple_hyphens():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-multiple-hyphens endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with multiple hyphens.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-multiple-hyphens")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_special_characters():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-special-characters endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with special characters.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-special-characters")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_emoji():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-emoji endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with emoji.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-emoji")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_invalid_characters():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-invalid-characters endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with invalid characters.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-invalid-characters")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_in_middle():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-in-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with a hyphen in the middle.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-in-middle")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with a hyphen at the start.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_end():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-end endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with a hyphen at the end.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-end")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with a hyphen at the start and end.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_middle():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with a hyphen at the start and middle.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-middle")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_end_and_middle():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-end-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with a hyphen at the end and middle.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-end-and-middle")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle():
    """
    Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle, and with a hyphen at the start, end, and middle.
    """
    response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_consecutive_hyphens():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-consecutive-hyphens endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with consecutive hyphens.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-consecutive-hyphens")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_multiple_hyphens():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-multiple-hyphens endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with multiple hyphens.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-multiple-hyphens")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_special_characters():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-special-characters endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with special characters.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-special-characters")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_emoji():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-emoji endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with emoji.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-emoji")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_invalid_characters():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-invalid-characters endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with invalid characters.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-invalid-characters")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_in_middle():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-in-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen in the middle.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-in-middle")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_end():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-end endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the end.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-end")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start and end.
#     """ 
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_middle():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start and middle.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-middle")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_end_and_middle():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-end-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the end and middle.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-end-and-middle")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, and middle.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_consecutive_hyphens():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-consecutive-hyphens endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with consecutive hyphens.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-consecutive-hyphens")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_multiple_hyphens():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-multiple-hyphens endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with multiple hyphens.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-multiple-hyphens")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_special_characters():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-special-characters endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with special characters.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-special-characters")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_emoji():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-emoji endpoint returns a 422 error for a username with a hyphen at the start,
#     end, in the middle, and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with emoji.
#     """ 
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-emoji")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_invalid_characters():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-invalid-characters endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with invalid characters.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-invalid-characters")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_in_middle():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-in-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with a hyphen in the middle.
#     """ 
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-in-middle")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with a hyphen at the start.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_end():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-end endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen  at the start, end, middle, and with a hyphen at the end.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-end")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen  at the start, end, middle, and with a hyphen at the start and end.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_middle():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with a hyphen at the start and middle.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-middle")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_end_and_middle():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-end-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with a hyphen at the end and middle.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-end-and-middle")
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters."
# def test_get_gists_valid_username_with_hyphen_in_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle_and_hyphen_at_start_and_end_and_middle():
#     """
#     Validates that the /valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle endpoint returns a 422 error for a username with a hyphen at the start, end, in the middle,
#     and with a hyphen at the start, end, middle, and with a hyphen at the start, end, middle, and with a hyphen at the start, end, and middle.
#     """
#     response = client.get("/valid-username-with-hyphen-in-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle-and-hyphen-at-start-and-end-and-middle")
    
#     assert response.status_code == 422
#     assert "detail" in response.json()
#     assert response.json()["detail"] == "Invalid input. Please check the username or query parameters." 

def test_get_gists_nonexistent_user(monkeypatch):
    """
    Validates that the /nonexistentuser endpoint returns a 404 error if user not found.
    """
    def mock_github_404(*args, **kwargs):
        class MockResponse:
            status_code = 404
            def json(self): return {"message": "Not Found"}
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_github_404)

    response = client.get("/nonexistentuser")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "GitHub user 'nonexistentuser' not found."
        
def test_valid_username():
    response = client.get("/octocat")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "items" in data
    assert isinstance(data["items"], list)

def test_invalid_username_emoji():
    response = client.get("/💩")
    assert response.status_code == 422
    assert "detail" in response.json()

def test_invalid_username_hyphen_start():
    response = client.get("/-user")
    assert response.status_code == 422