from pydantic import BaseModel


class FeedSyncResultSchema(BaseModel):
    status: str
