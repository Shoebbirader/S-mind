from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple

from engine.static_solver import Node, Material, Section, Element
from utils.state_manager import model_data

app = FastAPI()

# --- Pydantic Models for API data validation ---

class NodeCreateModel(BaseModel):
    id: int
    coordinates: Tuple[float, float, float]

class MaterialCreateModel(BaseModel):
    id: int
    name: str
    E: float  # Young's Modulus
    nu: float  # Poisson's Ratio
    density: float

class SectionCreateModel(BaseModel):
    id: int
    name: str
    A: float   # Area
    Ix: float  # Moment of inertia about x-axis
    Iy: float  # Moment of inertia about y-axis
    J: float   # Torsional constant

class ElementCreateModel(BaseModel):
    id: int
    node_i_id: int
    node_j_id: int
    material_id: int
    section_id: int

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to StruMind API"}

# --- Node Endpoints ---

@app.post("/nodes/", response_model=Node)
def create_node(node_data: NodeCreateModel):
    if model_data.get_node(node_data.id):
        raise HTTPException(status_code=400, detail=f"Node with id {node_data.id} already exists.")
    node = Node(id=node_data.id, coordinates=node_data.coordinates)
    model_data.add_node(node)
    return node

@app.get("/nodes/{node_id}", response_model=Node)
def get_node(node_id: int):
    node = model_data.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node with id {node_id} not found.")
    return node

@app.get("/nodes/", response_model=List[Node])
def get_all_nodes():
    return model_data.get_all_nodes()

# --- Material Endpoints ---

@app.post("/materials/", response_model=Material)
def create_material(material_data: MaterialCreateModel):
    if model_data.get_material(material_data.id):
        raise HTTPException(status_code=400, detail=f"Material with id {material_data.id} already exists.")
    material = Material(**material_data.dict())
    model_data.add_material(material)
    return material

@app.get("/materials/", response_model=List[Material])
def get_all_materials():
    return model_data.get_all_materials()

# --- Section Endpoints ---

@app.post("/sections/", response_model=Section)
def create_section(section_data: SectionCreateModel):
    if model_data.get_section(section_data.id):
        raise HTTPException(status_code=400, detail=f"Section with id {section_data.id} already exists.")
    section = Section(**section_data.dict())
    model_data.add_section(section)
    return section

@app.get("/sections/", response_model=List[Section])
def get_all_sections():
    return model_data.get_all_sections()

# --- Element Endpoints ---

@app.post("/elements/", response_model=Element)
def create_element(element_data: ElementCreateModel):
    if model_data.get_element(element_data.id):
        raise HTTPException(status_code=400, detail=f"Element with id {element_data.id} already exists.")

    node_i = model_data.get_node(element_data.node_i_id)
    if not node_i:
        raise HTTPException(status_code=404, detail=f"Node with id {element_data.node_i_id} not found.")

    node_j = model_data.get_node(element_data.node_j_id)
    if not node_j:
        raise HTTPException(status_code=404, detail=f"Node with id {element_data.node_j_id} not found.")

    material = model_data.get_material(element_data.material_id)
    if not material:
        raise HTTPException(status_code=404, detail=f"Material with id {element_data.material_id} not found.")

    section = model_data.get_section(element_data.section_id)
    if not section:
        raise HTTPException(status_code=404, detail=f"Section with id {element_data.section_id} not found.")

    element = Element(
        id=element_data.id,
        node_i=node_i,
        node_j=node_j,
        material=material,
        section=section
    )
    model_data.add_element(element)
    return element

@app.get("/elements/", response_model=List[Element])
def get_all_elements():
    return model_data.get_all_elements()

@app.post("/clear/")
def clear_model_data():
    """Clears all data from the model."""
    model_data.clear()
    return {"message": "Model data cleared."}
