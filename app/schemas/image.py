from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class SearchResultImage(BaseModel):
    name: str = Field(..., description="Filename of the image")
    score: float = Field(..., ge=0, le=1,
                         description="Similarity score of the image")
    image_url: Optional[HttpUrl] = Field(
        default=None, description="URL of the image")

    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "name": "example.jpg",
                    "score": 0.95,
                    "image_url": "http://url/static/example.jpg"
                }
            ]
        }
    }


class SearchResponse(BaseModel):
    results: list[SearchResultImage] = Field(...,
                                             description="List of search results")

    model_config = {
        "json_schema_extra": {
            "example": {
                "results": [
                    {
                        "name": "example.jpg",
                        "score": 0.95,
                        "image_url": "http://url/static/example.jpg"
                    }
                ]
            }
        }
    }
