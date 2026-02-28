import unittest
from tramdata import *

TRAM_FILE = './tramnetwork.json'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            self.tramdict = json.loads(trams.read())
            self.stopdict = self.tramdict['stops']
            self.linedict = self.tramdict['lines']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

    def test_query_via(self):
        ans = answer_query(self.tramdict, "via Chalmers")
        self.assertEqual(ans, ['6', '7', '8', '10', '13'])

    def test_lines_between_chalmers_valand(self):
        # example from lab description
        ans = lines_between_stops(self.linedict, "Chalmers", "Valand")
        self.assertEqual(ans, ['7', '10'])

    def test_distance_example_from_lab_text(self):
        # lab example: Chalmers → Järntorget == 1.628 km
        d = distance_between_stops(self.stopdict, "Chalmers", "Järntorget")
        self.assertAlmostEqual(d, 1.628, places=3)

    def test_time_is_symmetric(self):
        # time from A→B should equal time from B→A on same line
        t1 = time_between_stops(self.linedict, self.tramdict["times"], "6", "Chalmers", "Järntorget")
        t2 = time_between_stops(self.linedict, self.tramdict["times"], "6", "Järntorget", "Chalmers")
        self.assertEqual(t1, t2)

    def test_query_case_insensitive(self):
        # extra feature: case insensitive queries
        r1 = answer_query(self.tramdict, "via Chalmers")
        r2 = answer_query(self.tramdict, "via chalmers")
        r3 = answer_query(self.tramdict, "via CHALMERS")
        self.assertEqual(r1, r2)
        self.assertEqual(r1, r3)

    def test_query_frolunda_normalization(self):
        # extra feature: normalize å ä ö
        r1 = answer_query(self.tramdict, "via Frölunda Torg Spårvagn")
        r2 = answer_query(self.tramdict, "via frolunda torg")
        r3 = answer_query(self.tramdict, "via frolunda")
        self.assertEqual(r1, r2)
        self.assertEqual(r1, r3)

if __name__ == '__main__':
    unittest.main()

