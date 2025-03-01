from fastapi import APIRouter

from app.api.v1.endpoints import artists, ai_interaction, data, test, artworks

api_router = APIRouter()

# 注册路由
api_router.include_router(artists.router, prefix="/artists", tags=["artists"])
api_router.include_router(artworks.router, prefix="/artworks", tags=["artworks"])
api_router.include_router(ai_interaction.router, prefix="/ai-interaction", tags=["ai-interaction"])
api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(test.router, prefix="/test", tags=["test"])
