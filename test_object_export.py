from tests import utils

import bpy


class TestObjectExport(utils.XRayTestCase):
    blend_file = 'test_object_export.blend'

    def test_export_single(self):
        bpy.ops.xray_export.object(
            object='Cube1', filepath=self.outpath('Cube1.object'),
            texture_name_from_image_path=False
        )
        self.assertFileExists(self.outpath('Cube1.object'))

    def test_export_multi(self):
        bpy.ops.export_object.xray_objects(
            objects='Cube1,Cube2', directory=self.outpath(),
            texture_name_from_image_path=False
        )
        self.assertFileExists(self.outpath('Cube1.object'))
        self.assertFileExists(self.outpath('Cube2.object'))
