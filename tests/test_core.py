import unittest
from migrationkit.core import CHECKS, Progress, analyze, make_plan, normalize, export_json

class MigrationTests(unittest.TestCase):
    def test_01_checks_count(self): self.assertEqual(len(CHECKS),10)
    def test_02_normalize_spaces(self): self.assertEqual(normalize('  NEW  IDE '),'new ide')
    def test_03_normalize_empty(self): self.assertEqual(normalize(' '),'')
    def test_04_wrong_text(self):
        with self.assertRaises(TypeError): normalize(None)
    def test_05_zero_progress(self): self.assertEqual(analyze([])['percent'],0)
    def test_06_zero_completed(self): self.assertEqual(analyze([])['completed'],0)
    def test_07_total_checks(self): self.assertEqual(analyze([])['total'],10)
    def test_08_all_complete(self): self.assertEqual(analyze([Progress(c,True) for c,_,_ in CHECKS])['percent'],100)
    def test_09_all_incomplete(self): self.assertEqual(analyze([Progress(c,False) for c,_,_ in CHECKS])['percent'],0)
    def test_10_one_completed(self): self.assertEqual(analyze([Progress('backup',True)])['completed'],1)
    def test_11_weighted_progress(self): self.assertGreater(analyze([Progress('backup',True)])['percent'],0)
    def test_12_unknown_code(self):
        with self.assertRaises(ValueError): analyze([Progress('oops',True)])
    def test_13_bad_progress_type(self):
        with self.assertRaises(TypeError): analyze('bad')
    def test_14_bad_item(self):
        with self.assertRaises(ValueError): analyze([{}])
    def test_15_duplicate(self):
        with self.assertRaises(ValueError): analyze([Progress('backup',True),Progress('backup',False)])
    def test_16_bool_required(self):
        with self.assertRaises(TypeError): analyze([Progress('backup',1)])
    def test_17_remaining_initial(self): self.assertEqual(len(make_plan([])),10)
    def test_18_remaining_one(self): self.assertEqual(len(make_plan([Progress('backup',True)])),9)
    def test_19_no_remaining(self): self.assertEqual(make_plan([Progress(c,True) for c,_,_ in CHECKS]),[])
    def test_20_priority_present(self): self.assertIn('priority',make_plan([])[0])
    def test_21_codes_unique(self): self.assertEqual(len({c for c,_,_ in CHECKS}),10)
    def test_22_weight_positive(self): self.assertTrue(all(w>0 for _,_,w in CHECKS))
    def test_23_has_tests(self): self.assertIn('tests',{c for c,_,_ in CHECKS})
    def test_24_has_debugger(self): self.assertIn('debugger',{c for c,_,_ in CHECKS})
    def test_25_order_stable(self): self.assertEqual(make_plan([])[0]['code'],'backup')
    def test_26_plan_excludes_done(self): self.assertNotIn('backup',[i['code'] for i in make_plan([Progress('backup',True)])])
    def test_27_json_works(self): self.assertIn('assessment',export_json([]))
    def test_28_json_unicode(self): self.assertIn('Сохранить',export_json([]))
    def test_29_assessment_range(self): self.assertLessEqual(analyze([Progress('tests',True)])['percent'],100)
    def test_30_report_remaining(self): self.assertIn('remaining',export_json([]))
    def test_31_complete_score(self): self.assertEqual(analyze([Progress(c,True) for c,_,_ in CHECKS])['complete_weight'],24)
    def test_32_total_weight(self): self.assertEqual(analyze([])['total_weight'],24)
    def test_33_false_not_completed(self): self.assertEqual(analyze([Progress('backup',False)])['completed'],0)
    def test_34_space_check_title(self): self.assertTrue(all(name.strip() for _,name,_ in CHECKS))
    def test_35_last_step(self): self.assertEqual(make_plan([])[-1]['code'],'docs')

if __name__=='__main__': unittest.main()
