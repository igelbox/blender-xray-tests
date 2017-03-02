from tests import utils

import bpy


class TestAnmExport(utils.XRayTestCase):
    blend_file = 'test_object_export.blend'

    def test_error_no_anim(self):
        bpy.context.scene.objects.active = bpy.context.scene.objects['Cube1']
        with self.assertRaisesRegex(Exception, 'Animation: object doesn\'t any animation data'):
            bpy.ops.xray_export.anm(
                filepath=self.outpath('Cube1.anm'),
            )

    def test_error_yxz(self):
        obj = bpy.context.scene.objects['Cube1']
        obj.animation_data_create().action = bpy.data.actions[0]
        bpy.context.scene.objects.active = obj
        with self.assertRaisesRegex(Exception, "Animation: rotation mode must be 'YXZ'"):
            bpy.ops.xray_export.anm(
                filepath=self.outpath('Cube1.anm'),
            )

    def test_ok(self):
        bpy.context.scene.objects.active = bpy.context.scene.objects['Cube2']
        bpy.ops.xray_export.anm(
            filepath=self.outpath('Cube2.anm'),
        )
        self.assertOutputFiles({
            'Cube2.anm'
        })
