"""Add mahavastu routes"""
content = open('api/routes/advanced_routes.py', encoding='utf-8').read()

# Add mahavastu import
if 'mahavastu_engine' not in content:
    content = content.replace(
        'from engine.plot_layout_engine import PlotLayoutEngine',
        'from engine.plot_layout_engine import PlotLayoutEngine\nfrom engine.mahavastu_engine import MahaVastuEngine'
    )
    
    # Add mahavastu endpoints at end
    mahavastu_endpoints = '''

# ═══ MAHAVASTU ═══
class SpaceSurgeryRequest(BaseModel):
    zone: str
    defect_type: str = "cut_corner"


class PyramidRequest(BaseModel):
    zone: str
    issue_type: str = "Cut_Corner"


class MarmaRequest(BaseModel):
    marma_zone: str


@router.post("/mahavastu/space-surgery")
def space_surgery(req: SpaceSurgeryRequest):
    engine = MahaVastuEngine()
    result = engine.suggest_space_surgery(req.zone, req.defect_type)
    return {"status": "success", "data": result}


@router.post("/mahavastu/pyramids")
def pyramids(req: PyramidRequest):
    engine = MahaVastuEngine()
    result = engine.suggest_pyramids(req.zone, req.issue_type)
    return {"status": "success", "data": result}


@router.post("/mahavastu/marma")
def marma(req: MarmaRequest):
    engine = MahaVastuEngine()
    result = engine.suggest_marma_remedy(req.marma_zone)
    return {"status": "success", "data": result}
'''
    
    content = content + mahavastu_endpoints
    open('api/routes/advanced_routes.py', 'w', encoding='utf-8').write(content)
    print('MahaVastu routes added!')
else:
    print('MahaVastu routes already exist')
