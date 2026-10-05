def validate_sensor_payload(data):
    """Return error message if invalid, None if OK"""
    if not data:
        return "Empty payload received"
    if isinstance(data, dict):
        if "reading" not in data or data["reading"] in (None, "", " "):
            return "Reading field is required"
    return None

# Usage before DB insert:
# error = validate_sensor_payload(request_data)
# if error:
#     return {"error": error}, 400
