from tests import utils

import bpy
import re


class TestObjectImport(utils.XRayTestCase):
    def test_import_broken(self):
        with utils.OpReportCatcher() as reports:
            bpy.ops.xray_import.object(
                directory=self.relpath(),
                files=[{'name': 'test_import_broken.object'}],
            )
            reports.assertContains('WARNING', re.compile('Unsupported bone (\w+) shape type'))
            reports.assertContains('WARNING', re.compile('Unsupported bone (\w+) ikjoint type'))
