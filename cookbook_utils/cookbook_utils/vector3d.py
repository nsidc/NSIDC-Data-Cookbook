"""Class for three-dimensional vectors"""

from numbers import Number

import numpy as np
import matplotlib.pyplot as plt


CARDINAL_AXES = {
    "x": [1, 0, 0],
    "y": [0, 1, 0],
    "z": [0, 0, 1],
}


class Vector3D():

    def __init__(self, x, y, z, origin=(0,0,0), vtype='column', name=""):
        self.x = x
        self.y = y
        self.z = z
        self.origin = origin
        self.vtype = vtype
        self.name = name
        if vtype in ['col', 'column']:
            self.vector = np.array([x, y, z]).T
        else:
            self.vector = np.array([x, y, z])


    def __str__(self):
        if self.vtype in ['col', 'column']:
            return f"{self.name} = ({self.x} {self.y} {self.z}).T"
        else:
            return f"{self.name} = ({self.x} {self.y} {self.z})"

    def __repr__(self):
        return f"Vector({self.x} {self.y} {self.z}, name=`{self.name}`)"
        
    @property
    def magnitude(self):
        """Returns the magnitude of the vector object"""
        return np.sqrt(np.dot(self.vector, self.vector))
        
    @property
    def unit(self):
        """Returns the unit vector"""
        return self / self.magnitude
        
    @property
    def to_spherical(self):
        """Converts 3d cartesian coordinates to spherical
        coordinates.

        Returns:
          r, theta, phi
        """
        return xyz2sphere(self.x, self.y, self.z)

    @property
    def to_geographic(self):
        """Converts 3D cartesian coordinates to geographic coordinates

        Returns:
        lat, lon, r
        """
        r, theta, phi = xyz2sphere(self.x, self.y, self.z)
        return 90 - np.rad2deg(phi), np.rad2deg(theta), r

    def project(self, plane):
        """Returns a new `Vector` with a projection onto `plane`,
        where `plane` can be "xy", "xz", "yz"

        Arguments:
          plane : plane to project onto, accepts "xy", "xz" or "yz"

        Return:
          A new `Vector` object.
        """
        if plane == "xy":
            return Vector(self.x, self.y, 0, origin=self.origin, name=f"self.name_{plane}")
        elif plane == "xz":
            return Vector(self.x, 0, self.z, origin=self.origin, name=f"self.name_{plane}")
        elif plane == "yz":
            return Vector(0, self.y, self.z, origin=self.origin, name=f"self.name_{plane}")
        else:
            raise ValueError(f"Unknown plane: expects one of 'xy', 'xz', or 'yz'")
            
    def plot(self, ax=None, 
             add_label=False, label_position='end', label=None, 
             xoffset=0.0, yoffset=0.0, zoffset=0.0,
             show_angle=False, angle_name=None, angle_plane=None,
             **kwargs):
        """Plots vector on axis `ax` or current axis

        Arguments:
          ax : matplotlib.pyplot.Axis object
          add_label : display vector name (Default False)
          label_position : position of vector label; 'end', 'middle'
          label : name of vector.  If None then uses name assigned for instance
          xoffset : offset for label on x-axis (Default 0.0)
          yoffset : offset for label on y-axis (Default 0.0)
          zoffset : offset for label on z-axis (Default 0.0)
          show_angle : add angle arc on plot
          angle_name : string for angle name.  Not shown if None
          angle_plane : horizontal (xy) or vertical (xz)
          **kwargs : keyword arguments for matplotlib.pyplot.plot

        Returns:
          matplotlib.pyplot.Axis object
        """
        ax = plt.gca()

        xv = (self.origin[0], self.x)
        yv = (self.origin[1], self.y)
        zv = (self.origin[2], self.z)
        ax.plot(xv, yv, zv, **kwargs)

        # TODO a smart way to locate label
        if add_label or label:
            xt, yt, zt = self._get_label_pos(label_position)
            ax.text(xt, yt, zt, self.name, ha="left")

        if show_angle:
            raise NotImplemented
            
        return ax
        
    def _get_label_pos(self, label_position: str) -> tuple:
        """Returns coordinates tuple for positioning label"""
        if label_position == "end":
            return (self.x, self.y, self.z)
        elif label_position == "middle":
            return (self.x/2., self.y/2., self.z/2.)
            
    @classmethod
    def from_spherical(cls, phi: float, theta: float, r: float=1, degrees=True, name: str=None) -> Vector:
        """creates a 3D vector in Euclidean space from
        spherical coordinates.

        Arguments:
          phi : polar angle (also zenith angle or colatitude from the positive z-axis
                in degrees (0 <= phi <= 180).
          theta : azimuthal angle in the x-y plane from the x-axis (0 <= theta < 360).
                  Equvalent to longitude.
          r : distance from point to origin.  Default is 1 for a unit sphere.
          degrees : phi and theta are provided in degrees when True.  Radians when false.
          name : name of point or vector

        Returns:
          Vector object
        """
        if degrees:
            phi = np.radians(phi)
            theta = np.radians(theta)
        return cls(*sphere2xyz(phi, theta, r), name=name)

    @classmethod
    def from_geographic(cls, lat: float, lon: float, r: float=1, name: float=None) -> Vector:
        """Creates a 3D cartesian vector from geographic coordinates.

        Arguments:
          lat : latitude in degrees (-90 <= lat <+ 90)
          lon : longitude in degrees (0 <= lon < 360 or -180 <= lon < 180)
          r : radius of unit sqphere for testing but should be radius of Earth
          name : name of point or vector

        Returns:
          Instance of Vector class
        """
        phi = np.radians(90. - lat)
        if (lon >= 0.) & (lon < 360.):
            theta = np.radians(lon)
        elif (lon < 0):
            print(360 + lon)
            theta = np.radians(360 + lon)
            print(theta)
        else:
            raise ValueError(f"Expected 0 <= lon < 360 or -180 <= lon < 180, got {lon} instead")

        return cls(*sphere2xyz(phi, theta, r), name=name)

    @classmethod
    def from_numpy(cls, arr, origin=(0,0,0), name="") -> Vector:
        """Creates a 3D cartesian vector from a numpy array or array like object

        Arguments:
          arr : list like object
          origin : origin of vector.  By default this is (0,0,0)
          name : name of vector

        Returns:
          Vector object
        """
        return cls(*arr, origin=origin, name=name)
        
    def __add__(self, other: Vector) -> Vector:
        """Adds to vector objects and returns a new vector object"""
        if isinstance(other, Vector):
            if self.name and other.name:
                name = f"{self.name} + {other.name}"
            return Vector(
                self.x + other.x, self.y + other.y, self.z + other.z, 
                origin=self.vector, name=name)
        else:
            raise NotImplemented("Only supports addition of Vector objects")

    def __sub__(self, other: Vector) -> Vector:
        """Subtract two Vector objects"""
        if isinstance(other, Vector):
            if self.name and other.name:
                name = f"{self.name} - {other.name}"
            return Vector(
                self.x - other.x, self.y - other.y, self.z - other.z, 
                origin=self.vector, name=name)
        else:
            raise NotImplemented("Only supports subtraction of Vector objects")

    def __truediv__(self, other: Number) -> Vector:
        """Scalar division for Vector object.  Not defined for two vectors"""
        if isinstance(other, Number):
            return Vector(*(self.vector / other), origin=self.origin)
        else:
            raise NotImplemented("Only supports scalar division Vector objects")

    def __mul__(self, other: Number) -> Vector:
        """Scalar multiplication for Vector object. Only defined for scaler multiplication"""
        if isinstance(other, Number):
            return Vector(*(self.vector * other), origin=self.origin)
        else:
            raise NotImplemented("Only supports scalar multiplication Vector objects")

    def dot(self, other: Vector) -> Number:
        """Returns the dot product of self and other.  Wrapper for numpy.dot

        Arguments:
          other : Vector object

        Returns:
          dot product of self and other.  Scalar 
        """
        if isinstance(other, Vector):
            return np.dot(self.vector, other.vector)
        else:
            raise NotImplemented("Only supports Vector objects")

    def cross(self, other: Vector, name=None) -> Vector:
        """Returns the cross product of two Vector objects"""
        if isinstance(other, Vector):
            if not name:
                if self.name and other.name:
                    name = f"{self.name} x {other.name}"
                    
            return Vector.from_numpy(np.cross(self.vector, other.vector), name=name)

    def rotate(self, axis, angle: float, degrees: bool=False, name: str=None) -> Vector:
        """Rotate Vector about axis by angle

        Arguments:
          axis : either named axis (x, y, z) or list-like or Vector to rotate about
          angle : angle of rotation.  By default angle in radians but degrees if degrees=False
          degrees : if True, angle is in degrees
          name : name of new vector

        Returns:
          Vector object rotated about axis by angle
        """
        if isinstance(axis, str):
            if axis in CARDINAL_AXES:
                axis_arr = CARDINAL_AXES[axis]
            else:
                raise KeyError(f"String instance of axis expected as one of `x`, `y`, or `z`, for `{axis}` instead")
        elif isinstance(axis, Vector):
            axis_arr = axis.vector
        elif isinstance(axis, (np.array, list, tuple)):
            axis_arr = axis
        else:
            raise TypeError(f"Got unexpected type for axis, got {axis.type}")

        if degrees:
            angle = np.radians(angle)

        m = transforms3d.axangles.axangle2aff(axis_arr, angle, point=self.origin)
        q = np.dot(m, np.append(self.vector, 1))
        
        return Vector.from_numpy(q[:3], origin=self.origin, name=name)


def sphere2xyz(phi, theta, r=1.):
    """Converts spherical coordinates to 3D cartesian coordinates

    Arguments:
        phi : polar angle (also zenith angle or colatitude from the positive z-axis
            in radians (0 <= phi <= pi).
        theta : azimuthal angle in the x-y plane from the x-axis (0 <= theta < 2pi).
            Equvalent to longitude.
        r : distance from point to origin.  Default is 1 for a unit sphere.
      
    Returns:
      x, y, z
    """
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)
    return x, y, z


def xyz2sphere(x, y, z):
    """Converts 3D cartesian coordinates to spherical coordinates

    Arguments:
      x, y, z : components of cartesian position vector

    Returns:
      radial, polar and azimuthal coordinates (r, phi, theta)
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arctan(y / x)
    phi = np.arccos(z / r)
    return r, theta, phi
