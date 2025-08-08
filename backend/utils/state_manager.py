from typing import Dict, List

from engine.static_solver import Node, Material, Section, Element


class ModelData:
    """A class to hold the state of the structural model."""

    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.materials: Dict[int, Material] = {}
        self.sections: Dict[int, Section] = {}
        self.elements: Dict[int, Element] = {}

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def get_node(self, node_id: int) -> Node:
        return self.nodes.get(node_id)

    def get_all_nodes(self) -> List[Node]:
        return list(self.nodes.values())

    def add_material(self, material: Material):
        self.materials[material.id] = material

    def get_material(self, material_id: int) -> Material:
        return self.materials.get(material_id)

    def get_all_materials(self) -> List[Material]:
        return list(self.materials.values())

    def add_section(self, section: Section):
        self.sections[section.id] = section

    def get_section(self, section_id: int) -> Section:
        return self.sections.get(section_id)

    def get_all_sections(self) -> List[Section]:
        return list(self.sections.values())

    def add_element(self, element: Element):
        self.elements[element.id] = element

    def get_element(self, element_id: int) -> Element:
        return self.elements.get(element_id)

    def get_all_elements(self) -> List[Element]:
        return list(self.elements.values())

    def clear(self):
        """Clears all data from the model."""
        self.nodes.clear()
        self.materials.clear()
        self.sections.clear()
        self.elements.clear()


# Global instance of the model data, acting as a singleton
model_data = ModelData()
