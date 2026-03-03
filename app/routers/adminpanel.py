from fastapi import APIRouter


# creating fastapi router for endpoint
router = APIRouter(
    prefix='/api',
    tags=['admin/staff panel']
)
