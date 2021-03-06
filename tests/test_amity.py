import os
import unittest
from mock import patch

from app.amity import Amity
from app.livingspace import LivingSpace
from app.office import Office
from app.people import Person
from models.amity_database import Person as PersonModel, Session


test_session = Session().create_session('test_db.sqlite')


class TestAmity(unittest.TestCase):

    """Tests Class Amity"""

    def setUp(self):
        self.amity = Amity(test_session)

    def tests_amity_system_initializes_with_nothing(self):
        self.assertEqual(len(self.amity.rooms), 0)
        self.assertEqual(len(self.amity.persons), 0)

    @patch('app.amity.Room')
    def tests_amity_creates_room(self, mocked_room):
        """Tests amity creates a room object, and stores
        the room object in a tuple called rooms()"""

        old_rooms_total = len(self.amity.rooms)
        expected_return_value = True
        krypton_return_value = self.amity.create_room('Krypton', 'O')
        mocked_room.assert_called_with('Krypton', 'O', 0)

        ruby_return_value = self.amity.create_room('Ruby', 'L')
        mocked_room.assert_called_with('Ruby', 'L', 0)

        new_rooms_total = len(self.amity.rooms)

        self.assertEqual(krypton_return_value, expected_return_value)
        self.assertEqual(ruby_return_value, expected_return_value)
        self.assertEqual(new_rooms_total, old_rooms_total + 2)

    def tests_amity_adds_to_unallocated_if_no_rooms(self):
        with patch('app.amity.Amity.persons'):
            self.assertEqual(self.amity.add_person('Rose', 'Flowers', 'Staff'), None)
            self.assertEqual(self.amity.add_person('Benny', 'Flinn', 'Fellow', 'Y'), None)

    def tests_if_amity_adds_person(self):
        self.amity.add_person('Dido', 'Manjik', 'Fellow', 'Y')
        p = [p.full_name for p in Amity.persons if p.full_name == 'Dido Manjik'.upper()]
        self.assertIn('Dido Manjik'.upper(), p)

    def test_amity_prints_allocations_to_text_file(self):
        self.amity.create_room('Shire', 'o')
        self.amity.add_person('Fredd', 'Junito', 'Staff')
        self.amity.print_allocations('test_allocations')
        self.assertTrue(os.path.exists('test_allocations.txt'))

    def tests_amity_prints_unallocated_to_text_file(self):
        self.amity.add_person('Peter', 'Wright', 'Fellow')
        self.amity.print_unallocated('test_unallocated')
        self.assertTrue(os.path.exists('test_unallocated.txt'))

    def tests_amity_loads_people(self):
        self.assertEqual(self.amity.persons, [])
        self.amity.load_people('load.txt')
        self.assertEqual(len(self.amity.persons), 8)

    def tests_amity_reallocates_persons(self):
        self.amity.create_room('Hogspush', 'O')
        self.amity.add_person('Stella', 'Marks', 'Staff')
        self.amity.create_room('Stardom', 'O')
        self.amity.reallocate_person('MARKS', 'Stardom', 'O')
        x = [p.assigned_office for p in Amity.persons if p.full_name == 'STELLA MARKS']
        self.assertIn('Stardom'.upper(), x)

    def tests_amity_loads_state(self):
        self.amity.load_state()
        self.assertFalse(os.path.exists('alloamity_db.sqlite'))

    def tests_amity_saves_state(self):
        self.amity.create_room('Narnia', 'o')
        self.amity.add_person('Dandelion', 'Muku', 'Staff')
        self.amity.save_state()
        self.assertTrue(os.path.exists('alloamity_db.sqlite'))

    def tearDown(self):
        try:
            self.amity = None
            Amity.persons = []
            Amity.rooms = []
            os.remove('alloamity_db.sqlite')
            os.remove('test_allocations.txt')
            os.remove('test_unallocated.txt')
        except Exception:
            print('Error deleting test files.')
            return 'Error deleting test files.'

if __name__ == '__main__':
    unittest.main()
