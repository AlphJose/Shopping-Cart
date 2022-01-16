# Responses
def success_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }