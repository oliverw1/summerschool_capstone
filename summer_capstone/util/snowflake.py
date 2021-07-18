import awswrangler as wr

def get_snowflake_login_options(url, user, password, db, schema, warehouse, role):
    return {
        "sfURL": url,
        "sfUser": user,
        "sfPassword": password,
        "sfDatabase": db,
        "sfSchema": schema,
        "sfWarehouse": warehouse,
        "sfRole": role
    }

def get_snowflake_creds_from_sm(secret_name: str):
    creds = wr.secretsmanager.get_secret_json(secret_name)
    return {
        "sfURL": creds["URL"],
        "sfPassword": creds["PASSWORD"],
        "sfUser": creds["USER_NAME"]
    }