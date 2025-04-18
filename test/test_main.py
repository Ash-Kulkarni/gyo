import json


def test_ws_response(client):
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text(json.dumps({"vx": 0, "vy": 0, "angle": 0}))
        response = websocket.receive_text()
        data = json.loads(response)
        assert isinstance(data, dict)
        players = data.get("players")
        assert isinstance(players, dict)
        assert len(players) == 1
        pid, info = next(iter(players.items()))
        assert "x" in info and "y" in info and "a" in info
