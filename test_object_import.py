from tests import utils

import bmesh
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

    def test_import_uv(self):
        bpy.ops.xray_import.object(
            directory=self.relpath(),
            files=[{'name': 'test_import_uv.object'}],
        )
        self.assertReportsNotContains('WARNING')
        obj = bpy.data.objects['plobj']
        self.assertEqual(obj.material_slots[0].material.texture_slots[0].uv_layer, 'uvm')
        self.assertEqual(len(obj.data.uv_layers), 1)
        self.assertEqual(obj.data.uv_layers[0].name, 'uvm')
        self.assertEqual(len(obj.data.uv_textures), 1)
        self.assertEqual(obj.data.uv_textures[0].name, 'uvm')
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        uvl = bm.loops.layers.uv.verify()
        bm.faces.ensure_lookup_table()
        for l, e in zip(bm.faces[0].loops, [(1, 0), (0, 1), (0, 0)]):
            uv = l[uvl].uv
            self.assertEqual(uv.to_tuple(), e)
