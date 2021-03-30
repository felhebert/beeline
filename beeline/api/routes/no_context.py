"""Offer display model route - V1."""
from datetime import datetime
from typing import Dict, List, Optional

from math import cos, pi

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field
import tensorflow as tf

router = APIRouter()

model = tf.keras.models.load_model(
    "resources/models/no_context/",
    custom_objects={"<lambda>": lambda x: tf.strings.bytes_split(x)}
)


class NoContextIn(BaseModel):
    product_id: int = Field(..., title="Product Id field", gt=0)
    ts: datetime = Field(
        ..., title="Timestamp of the event (eg. when aggregation volumes are needed)"
    )
    creation_date: datetime = Field(..., title="Timestamp of product creation date")
    aggregation_volumes: List[float] = Field(..., title="Previous aggregation volumes")

    class Config:
        schema_extra = {
            "example": {
                "product_id": 8979865585,
                "ts": 1610409600,
                "aggregation_volumes": [27, 98, 65, 78, 22, 33],
            }
        }

    @property
    def creation_date_month(self) -> float:
        months_in_a_year = 12
        creation_date_month = cos(2 * pi * self.creation_date.month / months_in_a_year)
        return creation_date_month

    @property
    def product_seniority(self) -> int:
        return self.creation_date.seconds

    def dict(self):
        return {
            "creation_date_month": self.creation_date_month,
            "product_seniority": self.product_seniority,
            "aggregation_volumes": self.aggregation_volumes
        }


class NoContextOut(BaseModel):
    product_id: int
    forecasts: List[float]

    class Config:
        schema_extra = {"example": {"product_id": 89765585, "forecasts": [34, 21, 12]}}


@router.post(
    "/predict",
    response_model=NoContextOut,
    responses={
        500: {"description": "Internal Error"},
        200: {"description": "Product successfully predicted"},
    },
)
async def predict(product: NoContextIn) -> NoContextOut:
    """Predicts the three next forecasts for a given product at a given timestamp."""

    input_dict = {
        name: tf.convert_to_tensor([value]) for name, value in product.dict().items()
    }
    return NoContextOut(
        product_id=product.product_id,
        forecasts=model(input_dict)[0],
    )
