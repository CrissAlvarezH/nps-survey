
def get_metadata(request) -> dict:
    metadata = {
        "user-agent": request.META.get("HTTP_USER_AGENT"),
        "host": request.META.get("HTTP_HOST"),
        "user": request.META.get("USER"),
        "desktop_session": request.META.get("DESKTOP_SESSION")
    }
    return metadata
