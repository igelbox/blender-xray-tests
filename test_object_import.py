from tests import utils

import bpy
import re


class TestObjectImport(utils.XRayTestCase):
    def test_import_broken(self):
        bpy.ops.xray_import.object(
            directory=self.relpath(),
            files=[{'name': 'test_import_broken.object'}],
        )
        self.assertReportsContains('WARNING', re.compile('Unsupported bone (\w+) shape type'))
        self.assertReportsContains('WARNING', re.compile('Unsupported bone (\w+) ikjoint type'))

    def test_import_normal(self):
        bpy.ops.xray_import.object(
            directory=self.relpath(),
            files=[{'name': 'test_import.object'}],
        )
        self.assertReportsNotContains('WARNING')
        self.assertIsNotNone(bpy.context.active_object.pose.bones[0].custom_shape)

    def test_import_no_bone_shapes(self):
        bpy.ops.xray_import.object(
            directory=self.relpath(),
            files=[{'name': 'test_import.object'}],
            shaped_bones=False
        )
        self.assertReportsNotContains('WARNING')
        self.assertIsNone(bpy.context.active_object.pose.bones[0].custom_shape)
