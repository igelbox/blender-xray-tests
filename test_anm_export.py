from tests import utils

import bpy


class TestAnmExport(utils.XRayTestCase):
    blend_file = 'test_object_export.blend'

    def test_error(self):
        bpy.context.scene.objects.active = bpy.context.scene.objects['Cube1']
        with self.assertRaisesRegex(Exception, "Animation: rotation mode must be 'YXZ'"):
            bpy.ops.xray_export.anm(
                filepath=self.outpath('Cube1.anm'),
            )

    def test_ok(self):
        bpy.context.scene.objects.active = bpy.context.scene.objects['Cube2']
        bpy.ops.xray_export.anm(
            filepath=self.outpath('Cube2.anm'),
        )
        self.assertFileExists(self.outpath('Cube2.anm'))
