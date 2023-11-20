from typing import Dict, Any
import config.config as config_module
from fastapi import HTTPException, APIRouter

config_router = APIRouter()


@config_router.get("/config/{config_name}", response_model=Dict[str, Any])
async def get_config(config_name: str) -> Dict[str, Any]:
    try:
        config_class = getattr(config_module, config_name)
        return {
            attr: getattr(config_class, attr)
            for attr in dir(config_class)
            if not attr.startswith("__") and not attr.startswith("_abc") and not attr.startswith("model_")
               and not callable(getattr(config_class, attr))
        }
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Configuration '{config_name}' not found")

