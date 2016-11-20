from tests import utils

import bpy
import re


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
        self.assertFileExists(self.outpath('a/b/Cube2.object'))

    def test_export_multi_notusing_paths(self):
        bpy.ops.export_object.xray_objects(
            objects='Cube1,Cube2', directory=self.outpath(),
            use_export_paths=False,
            texture_name_from_image_path=False
        )
        self.assertFileExists(self.outpath('Cube1.object'))
        self.assertFileExists(self.outpath('Cube2.object'))

    def test_obsolete_bones(self):
        bpy.ops.export_object.xray_objects(
            objects='ObsoleteBones', directory=self.outpath(),
            texture_name_from_image_path=False,
            export_motions=False,
        )
        self.assertFileExists(self.outpath('ObsoleteBones.object'))
        self.assertReportsContains('WARNING', re.compile('bone .* edited with .* version of this plugin'))
