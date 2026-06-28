import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


app_path = Path(__file__).resolve().parents[1] / "src" / "app.py"
spec = importlib.util.spec_from_file_location("app_module", app_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

client = TestClient(module.app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "test-student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200

    delete_response = client.request(
        "DELETE",
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert delete_response.status_code == 200
    assert email not in module.activities[activity_name]["participants"]
