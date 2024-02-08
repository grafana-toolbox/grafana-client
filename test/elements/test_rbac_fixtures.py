RBAC_ROLES_ALL = [
    {
        "version": 5,
        "uid": "vi9mlLjGz",
        "name": "fixed:datasources.permissions:writer",
        "description": "Create, read or delete data source permissions.",
        "global": True,
        "updated": "2021-05-13T22:41:49+02:00",
        "created": "2021-05-13T16:24:26+02:00",
    }
]

PERMISSION_RBAC_DATASOURCE = [
    {
        "id": 1,
        "roleName": "fixed:datasources:reader",
        "isManaged": False,
        "isInherited": False,
        "isServiceAccount": False,
        "userId": 1,
        "userLogin": "admin_user",
        "userAvatarUrl": "/avatar/admin_user",
        "actions": [
            "datasources:read",
            "datasources:query",
            "datasources:read",
            "datasources:query",
            "datasources:write",
            "datasources:delete",
        ],
        "permission": "Edit",
    },
    {
        "id": 2,
        "roleName": "managed:teams:1:permissions",
        "isManaged": True,
        "isInherited": False,
        "isServiceAccount": False,
        "team": "A team",
        "teamId": 1,
        "teamAvatarUrl": "/avatar/523d70c8551046f441727d690431858c",
        "actions": ["datasources:read", "datasources:query"],
        "permission": "Query",
    },
    {
        "id": 3,
        "roleName": "basic:admin",
        "isManaged": False,
        "isInherited": False,
        "isServiceAccount": False,
        "builtInRole": "Admin",
        "actions": ["datasources:query", "datasources:read", "datasources:write", "datasources:delete"],
        "permission": "Edit",
    },
]
