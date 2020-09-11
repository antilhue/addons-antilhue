{
    "name": "Approval of user sign up",
    "summary": "Allows you to approve or reject web site registration requests",
    "version": "13.0.1.0.0",
    "category": "Authentication",
    "license": "AGPL-3",
    "depends": [
        "auth_signup",
    ],
    "external_dependencies": {
        "python": [
            "email_validator",
        ],
    },
    "data": [
        "views/signup.xml",
        "views/res_users_views.xml",
        "views/res_config_settings.xml",
        "views/mail_template.xml",
    ],
    'installable': True,
}
