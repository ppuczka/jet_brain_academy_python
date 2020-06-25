# from sql_alchemy_db import Table, Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

Session = sessionmaker(bind=engine)


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today())

    @staticmethod
    def create_table():
        Base.metadata.create_all(engine)

    def __repr__(self):
        return self.task


Table.create_table()
session = Session()

# task_list = ['Do yoga', 'Make breakfast', 'Learn basics of SQL', 'Learn what is ORM']
# counter = 1
# print('Today:')
# for task in task_list:
#     print(f'{counter}) {task}')
#     counter += 1


def add_new_task(task_name):
    new_row = Table(task=task_name)
    session.add(new_row)
    session.commit()
    print('The task have been added!')


main_menu = ["Today's tasks", 'Add task', 'Exit']
counter = 1

for position in main_menu:
    if position == 'Exit':
        print(f'0) {position}')
    else:
        print(f'{counter}) {position}')
    counter += 1

user_input = ''
while True:
    user_input = input()
    if user_input == '1':
        to_do_list = session.query(Table).all()
        print('Today:')
        if len(to_do_list) == 0:
            print('Nothing to do!')
        else:
            for task in to_do_list:
                print(task)
    elif user_input == '2':
        task = input('Enter task:\n')
        add_new_task(task)
    elif user_input == '0':
        print('Bye')
        break

