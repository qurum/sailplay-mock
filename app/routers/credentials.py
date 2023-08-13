from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Response
from pymongo import ReturnDocument

from app.database import Credentials
from app.schemas.credentials import CredentialsCreateSchema, CredentialsUpdateSchema
from app.serializers.credentials_serializers import (
    credentials_list_envelope,
    credentials_envelope,
)

router = APIRouter()


@router.get("/")
async def index():
    credentials_list = Credentials.find().sort("created_at", 1)
    return credentials_list_envelope(credentials_list)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(payload: CredentialsCreateSchema):
    credentials = Credentials.find_one(
        {
            "store_department_key": payload.store_department_key,
            "store_department_id": payload.store_department_id,
        }
    )
    if credentials:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Credentials already exist"
        )

    payload.created_at = datetime.utcnow()
    payload.updated_at = datetime.utcnow()
    result = Credentials.insert_one(payload.model_dump())
    pipeline = [
        {"$match": {"_id": result.inserted_id}},
    ]
    return credentials_list_envelope(Credentials.aggregate(pipeline))[0]


@router.put("/{credentials_id}")
async def update(credentials_id: str, payload: CredentialsUpdateSchema):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid id: {credentials_id}",
        )

    updated_credentials = Credentials.find_one_and_update(
        {"_id": ObjectId(credentials_id)},
        {"$set": payload.model_dump()},
        return_document=ReturnDocument.AFTER,
    )

    if not updated_credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No credentials with this id: {credentials_id} found",
        )

    return credentials_envelope(updated_credentials)


@router.delete("/{credentials_id}")
async def delete(credentials_id: str):
    if not ObjectId.is_valid(credentials_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid id: {credentials_id}",
        )

    deleted_credentials = Credentials.find_one_and_delete(
        {"_id": ObjectId(credentials_id)}
    )

    if not deleted_credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No credentials with this id: {credentials_id} found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
