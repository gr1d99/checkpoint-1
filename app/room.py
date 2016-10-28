from app.amity import Amity
from models.amity_database import Room as RoomModel, Person as PersonModel, DC
from sqlalchemy.orm.exc import NoResultFound
from pathlib import Path
import os
import random

rooms, persons = Amity().load_state() 

class Room(object):

    """ 
    Class that create rooms, randomly adds people to rooms,
    check rooms for available space and reallocate people to different
    rooms 
    """
    
    list_of_offices = []
    list_of_living_spaces = []

    def create_room(self, room_name, room_type):
        try:
            new_room = RoomModel()
            new_room.room_name = room_name
            new_room.room_type = room_type
            new_room.room_occupants = 0
            DC.session.add(new_room)
        except:
        

    def space_available(self, room_name):
        try:
            sa = rooms.filter_by(room_name=room_name).one()
            if sa.room_type == 'O':
                room_capacity = 6
            elif sa.room_type == 'L':
                room_capacity = 4

        except NoResultFound:
            """Handle exception"""

        if sa.room_occupants < room_capacity:
            return True  # There is space
        return False  # No space available

    def add_person(self, first_name, last_name, job_group, want_accomodation, gender):
        new_person = PersonModel()
        new_person.first_name = first_name
        new_person.last_name = last_name
        new_person.job_group = job_group
        new_person.want_accomodation = want_accomodation
        new_person.gender = gender

        self.add_person_to_office(new_person)
        if new_person.job_group == 'Fellow' and new_person.want_accomodation == 'Y':
            self.add_person_to_living_space(new_person)

        DC.session.add(new_person)
        
        DC.session.commit()

    def add_person_to_office(self, new_person):
        the_offices = []
        self.list_of_offices = rooms.filter_by(room_type='O').all()

        for office in self.list_of_offices:
            is_there_office_space = self.space_available(office.room_name)
            if is_there_office_space:
                the_offices.append(office)

        new_person.assigned_office = random.choice(the_offices).room_name
        # Is assigning an object from list of room objects query to
        # new_person.assigned_office

        rooms.filter_by(room_name=new_person.assigned_office)\
            .update({'room_occupants': RoomModel.room_occupants+1})

    def add_person_to_living_space(self, new_person):
        the_living = []
        self.list_of_living_spaces = rooms.filter_by(room_type='L').all()

        for living_space in self.list_of_living_spaces:
            is_there_living_space = self.space_available(
                living_space.room_name)
            if is_there_living_space:
                the_living.append(living_space)

        new_person.assigned_living_space = random.choice(
            self.list_of_living_spaces).room_name
        rooms.filter_by(room_name=new_person.assigned_living_space)\
            .update({'room_occupants': RoomModel.room_occupants+1})

    def reallocate_person(self, person_id, room_name):
        try:
            person_details = persons.filter_by(person_id=person_id).one()
            room_details = rooms.filter_by(room_name=room_name).one()
            room_type = room_details.room_type
            space_status = self.space_available(room_name)
            if space_status:
                if room_type == 'O':
                    current_room = person_details.assigned_office
                    persons.filter_by(person_id=person_id).update(
                        {'assigned_office': room_name})
                    rooms.filter_by(room_name=room_name).update(
                        {'room_occupants': room_details.room_occupants+1})
                    rooms.filter_by(room_name=current_room).update(
                        {'room_occupants': RoomModel.room_occupants-1})

                elif room_type == 'L':
                    current_room = person_details.assigned_living_space
                    persons.filter_by(person_id=person_id).update(
                        {'assigned_living_space': room_name})
                    rooms.filter_by(room_name=room_name).update(
                        {'room_occupants': room_details.room_occupants+1})
                    rooms.filter_by(room_name=current_room).update(
                        {'room_occupants': RoomModel.room_occupants-1})

        except NoResultFound:
            '''Record not found'''
        DC.session.commit()

    @staticmethod
    def load_people(txt_file):
        file_name = txt_file
        with open(file_name) as file:
            for line in file.readlines():
                person = line.replace('\n', '').split()
                print(person)
                Room().add_person(*person) 
                # Using python splat to add members of list as arguments to add_person()

    def print_room(self, room_name):
        members_in_office = persons.filter_by(
            assigned_office=room_name).all()
        members_in_living_space = persons.filter_by(
            assigned_living_space=room_name).all()
        members_in_room = members_in_office + members_in_living_space

        [print(member.first_name + ' ' + member.last_name)
         for member in members_in_room]

    def remove_person_from_room(self, person_id, room_name):
        # checker = DC.session.query(RoomMembers).filter_by(person_id=person_id, room_name=room_name).first()
        # .delete()
        # DC.session.commit()
        pass


# r1 = Room()
# r1.create_room('New', 'L')
# r2 = Room()
# r2.create_room('Narnia', 'O')
# r1.print_room('Narnia')
# Room.load_people('input1')
# r9 = Room()
# # r9.add_person('Neema', 'Bora', 'Fellow', 'Y', 'F')
# r9.reallocate_person('8', 'rom4')
Room.load_people('input3')