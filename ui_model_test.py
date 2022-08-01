import unittest

import ui_model


class ColourStateTest(unittest.TestCase):
    def test_colour_uodate(self):
        model = ui_model.UiModel(initial_colours=["red"])
        self.assertEqual(model.get_colours(), ["red"])

        model.update_colours(["green", "red", "blue"])
        self.assertEqual(model.get_colours(), ["green", "red", "blue"])
    
    def test_get_colour_for_index(self):
        model = ui_model.UiModel(initial_colours=["green", "red", "blue"])
        self.assertEqual(model.get_colour_for_index(1), "red")


class BoardStateTest(unittest.TestCase):
    def test_add_tube(self):
        model = ui_model.UiModel(initial_colours=[])
        self.assertEqual(len(model.get_tube_board().tubes), 1)

        model.add_tube()

        self.assertEqual(len(model.get_tube_board().tubes), 2)
        self.assertEqual(
            model.get_tube_board().tubes[1].state,
            [0, 0, 0, 0])

    def test_update_state(self):
        model = ui_model.UiModel(initial_colours=[])
        model.add_tube()
        model.add_tube()

        model.update_tube_state(2, [0, 1, 2, 3])

        self.assertEqual(
            model.get_tube_board().tubes[0].state,
            [0, 0, 0, 0])
        self.assertEqual(
            model.get_tube_board().tubes[2].state,
            [0, 1, 2, 3])
    
    def test_delete_tube(self):
        model = ui_model.UiModel(initial_colours=[])
        model.add_tube()
        model.add_tube()

        model.update_tube_state(2, [0, 1, 2, 3])
        model.delete_tube(1)

        self.assertEqual(len(model.get_tube_board().tubes), 2)
        self.assertEqual(
            model.get_tube_board().tubes[0].state,
            [0, 0, 0, 0])
        self.assertEqual(
            model.get_tube_board().tubes[1].state,
            [0, 1, 2, 3])


if __name__ == '__main__':
    unittest.main()
