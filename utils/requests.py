
def get_metadata(request) -> dict:
    metadata = {
        "user-agent": request.META["HTTP_USER_AGENT"],
        "host": request.META["HTTP_HOST"],
        "user": request.META["USER"],
        "desktop_session": request.META["DESKTOP_SESSION"]
    }
    return metadata
