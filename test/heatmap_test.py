import unittest
import writers


class HeatmapTest(unittest.TestCase):
    def test_heatmap(self):
        html_row = ''
        html_row += writers.distrpercent_to_heatmap_cells\
            ([('02', 15.3222211), ('03', 0), ('13', 33.33), ('16', 66), ('18',99)])
        with open('heatmap.html', 'w') as f:
            f.write(f'<table style="font-variant-numeric: tabular-nums;"><tr>{html_row}</tr></table>')
