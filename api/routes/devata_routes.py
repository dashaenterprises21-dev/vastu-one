from fastapi import APIRouter, HTTPException
from api.dependencies import get_all_devatas, get_devatas_data, get_elements_data
from engine.remedy_engine import RemedyEngine

router = APIRouter(prefix="/api", tags=["Devatas & Elements"])


@router.get("/devatas")
def list_devatas():
    return {"total": len(get_all_devatas()), "devatas": get_all_devatas()}


@router.get("/devatas/{name}")
def get_devata(name: str):
    for d in get_all_devatas():
        if d["name"].lower() == name.lower():
            return d
    raise HTTPException(status_code=404, detail=f"Devata '{name}' not found")


@router.get("/remedy/{devata_name}")
def get_remedy(devata_name: str):
    remedy = RemedyEngine(get_devatas_data(), get_elements_data())
    r = remedy.remedy_for_devata(devata_name)
    if not r:
        raise HTTPException(status_code=404, detail=f"Remedy for '{devata_name}' not found")
    return r


@router.get("/elements")
def list_elements():
    return get_elements_data()


@router.get("/elements/{name}/remedy")
def element_remedy(name: str):
    remedy = RemedyEngine(get_devatas_data(), get_elements_data())
    r = remedy.remedy_for_element(name)
    if not r:
        raise HTTPException(status_code=404, detail=f"Element '{name}' not found")
    return r