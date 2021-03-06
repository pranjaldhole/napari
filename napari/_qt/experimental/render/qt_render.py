"""QtRender widget.
"""
from qtpy.QtWidgets import QVBoxLayout, QWidget

from ....components.experimental.monitor import monitor
from ....layers.image import Image
from ....layers.image.experimental.octree_image import OctreeImage
from .qt_frame_rate import QtFrameRate
from .qt_image_info import QtImageInfo
from .qt_octree_info import QtOctreeInfo
from .qt_test_image import QtTestImage


class QtRender(QWidget):
    """Dockable widget for render controls.

    Parameters
    ----------
    viewer : Viewer
        The napari viewer.
    layer : Optional[Layer]
        Show controls for this layer. If no layer show minimal controls.
    """

    def __init__(self, viewer, layer=None):
        """Create our windgets.
        """
        super().__init__()
        self.viewer = viewer
        self.layer = layer

        layout = QVBoxLayout()

        # Basic info for any image layer.
        if isinstance(layer, Image):
            layout.addWidget(QtImageInfo(layer))

        if isinstance(layer, OctreeImage):
            # Octree specific controls and widgets.
            layout.addWidget(QtOctreeInfo(layer))

            self.viewer.camera.events.center.connect(self._on_camera_move)

        # Controls to create a new test image.
        layout.addStretch(1)
        layout.addWidget(QtTestImage(viewer))

        # Frame rate meter.
        self.frame_rate = QtFrameRate()
        layout.addWidget(self.frame_rate)

        self.setLayout(layout)

    def _on_camera_move(self, _event=None):
        """Called when the camera was moved."""
        self.frame_rate.on_camera_move()

        if monitor:
            intersection = self.layer.get_intersection()
            monitor.add(intersection.tile_config)
            monitor.add(intersection.tile_state)
