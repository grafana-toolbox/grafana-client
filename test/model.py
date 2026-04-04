import typing as t


class TestModel:
    @staticmethod
    def permissions() -> t.List[t.Dict[str, t.Any]]:
        return [
            {"role": "Viewer", "permission": 1},
            {"role": "Editor", "permission": 2},
            {"teamId": 1, "permission": 1},
            {"userId": 1, "permission": 4},
        ]

    """
    items=[
        {"permission": "View"},
        {"permission": "Edit"},
    ],
    """
