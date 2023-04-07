from pydantic import BaseModel


class DetailResponse(BaseModel):
    """
    If you do not know what response -> use this response model
    And write this at the end of your endpoint function
    message = "success"
    return {"detail": message}
    """

    detail: str
