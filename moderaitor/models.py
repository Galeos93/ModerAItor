from boto3.dynamodb.types import TypeSerializer

from pydantic import BaseModel, validator


ACCEPTED_ITEM = "SAFE"
SUSPICIOUS_ITEM = "FLAG"
MODERATION_VALUES = (
    ACCEPTED_ITEM,
    SUSPICIOUS_ITEM
)

def base_model_to_dynamo_item(model: dict) -> dict:
    serializer = TypeSerializer()
    dyn_item = {
        key: serializer.serialize(value) for key, value in model.items()
    }
    return dyn_item


class BaseComment(BaseModel):
    id: str
    username: str
    body: str


class ReviewedComment(BaseComment):
    flag: str

    @validator('flag')
    def check_flag_has_valid_value(cls, field):
        if field not in MODERATION_VALUES:
            raise ValueError(f"Output is not part of {MODERATION_VALUES}")
        return field


class ReviewedCommentWithContext(ReviewedComment):
    context: str
