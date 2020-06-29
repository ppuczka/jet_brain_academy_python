from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


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
Session = sessionmaker(bind=engine)
session = Session()

user_date_format = '%Y-%m-%d'
date_format = '%A %d %b'
day_month_date_format = '%d %b'

today_date = datetime.today()
formatted_today_day_month_date = today_date.__format__(day_month_date_format)
formatted_today_date = today_date.__format__(date_format)


def main_menu():
    menu = ["Today's tasks", "Week's tasks", 'All tasks', 'Add task', 'Exit']
    counter_ = 1
    for position in menu:
        if position == 'Exit':
            print(f'0) {position}')
        else:
            print(f'{counter_}) {position}')
        counter_ += 1


def query_daily_task(formatted_date):
    return session.query(Table).filter(Table.deadline == formatted_date).all()


def add_new_task(task_name, date):
    deadline_date_format = datetime.strptime(date, user_date_format)
    print(deadline_date_format)
    new_row = Table(task=task_name, deadline=deadline_date_format)
    session.add(new_row)
    session.commit()
    print('The task have been added!')


def weekly_tasks_overview():
    for j in range(7):
        deadline = today_date + timedelta(days=j)
        rows = session.query(Table).filter(Table.deadline == deadline.date()).all()
        count = 1
        print(datetime.strftime(deadline, '%A %d %b:'))
        if len(rows) <= 0:
            print("Nothing to do!")
        for i in range(len(rows)):
            print(str(count) + '. ' + rows[i].task)
            count += 1
        print()


def print_all_tasks():
    counter_ = 1
    all_tasks = session.query(Table).all()
    if len(all_tasks) == 0:
        print('Nothing to do!')
    else:
        for task_ in all_tasks:
            print(f'{counter_}. {task_}')
            counter_ += 1


def print_today_tasks():
    print(f'Today {formatted_today_day_month_date}:')
    print_all_tasks()


main_menu()
user_input = ''

while True:
    user_input = input()
    if user_input == '1':
        print_today_tasks()
        main_menu()
    elif user_input == '2':
        weekly_tasks_overview()
        main_menu()
    elif user_input == '3':
        print_all_tasks()
        main_menu()
    elif user_input == '4':
        task = input('Enter task: ')
        deadline = input('Enter date in yyyy-MM-dd format: ')
        add_new_task(task, deadline)
        main_menu()
    elif user_input == '0':
        print('Bye')
        break
