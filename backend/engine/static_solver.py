from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np


@dataclass
class Node:
    """Represents a node in the structural model."""
    id: int
    coordinates: Tuple[float, float, float]  # (x, y, z)
    dof: List[int] = field(default_factory=list)  # Degrees of Freedom


@dataclass
class Material:
    """Represents a material with its properties."""
    id: int
    name: str
    E: float  # Young's Modulus
    nu: float  # Poisson's Ratio
    density: float


@dataclass
class Section:
    """Represents a cross-section with its properties."""
    id: int
    name: str
    A: float  # Area
    Ix: float # Moment of inertia about x-axis
    Iy: float # Moment of inertia about y-axis
    J: float  # Torsional constant


@dataclass
class Element:
    """Represents a frame element in the structural model."""
    id: int
    node_i: Node
    node_j: Node
    material: Material
    section: Section

    @property
    def length(self) -> float:
        """Calculates the length of the element."""
        return np.linalg.norm(np.array(self.node_j.coordinates) - np.array(self.node_i.coordinates))

    def get_stiffness_matrix(self):
        """Placeholder for stiffness matrix calculation."""
        # This will be implemented later
        return np.zeros((12, 12))
