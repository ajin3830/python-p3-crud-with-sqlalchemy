#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
        + f"{self.name}, " \
        + f"Grade {self.grade}"
    
# ---Creating Records

# This method helps make an object's standard output human-readable
if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name='Albert Einstein',
        email='albert.einstein@zurich.edu',
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    # session.add(albert_einstein)
    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    print(f'New student ID is {albert_einstein.id}.')
    print(f'New student ID is {alan_turing.id}.')

# ---Read Records

    # Data type query() returns records in is tuple!!!!

    students = session.query(Student)
    print([student for student in students])

    students = session.query(Student).all()
    print(students)

    names = session.query(Student.name).all()
    print(names)

    # results from any database query are ordered by their primary key. 
    # The order_by() method allows us to sort by any column
    students_by_name = session.query(
        Student.name).order_by(Student.name).all()
    print(students_by_name)
    # [('Alan Turing',), ('Albert Einstein',)]

    # sort results in descending order
    students_by_grade_desc=session.query(
        Student.name, Student.grade).order_by(desc(Student.grade)).all()
    print(students_by_grade_desc)

    # limit the result to 1 record
    # What does Student.grade have to do w anything here:
    # we're query all the students, returning their name and birthday, 
    # and ordering them in descending order by their grade, 
    # limiting our return to one student, and that's what we get.
    oldest_student=session.query(
        Student.name, Student.birthday).order_by(desc(Student.grade)).limit(1).all()
    print(oldest_student)

    oldest_student=session.query(
        Student.name, Student.birthday).order_by(desc(Student.grade)).first()
    print(oldest_student)

    # func from sqlalchemy act upon columns, 
    # so wrapp a Column obj passed to the query()method
    # also call it as function.operations, if just func(Student.id) will have 
    # conflicts with functions in python library like sum()
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    # Retrieving specific records requires use of the filter() method. 
    # A typical filter() statement has a column, a standard operator, 
    # and a value. It is possible to chain multiple filter() statements 
    # together, though it is typically easier to read with 
    # comma-separated clauses inside of one filter() statement.
    query = session.query(Student).filter(
        Student.name.like('%Alan%'),Student.grade == 11).all()
    for record in query:
        print(record.name)

#---Updating Data

    # The simplest is to use Python to modify objects directly and 
    # then commit those changes through the session.
    for student in session.query(Student):
        student.grade += 1

    session.commit()
    print([(student.name, student.grade) for student in session.query(Student)])
    
    # The update() method updates records without creating objects beforehand. 
    # Here's how we would carry out the same statement with update():
    session.query(Student).update({Student.grade : Student.grade+1})
    print([(student.name, student.grade) for student in session.query(Student)])

#---Deleting Data

    #  If you have an object in memory that you want to delete, 
    # you can call the delete() method on the object from your session:
    query = session.query(Student).filter(Student.name == 'Albert Einstein')
    # retrieve first matching record as object
    albert_einstein = query.first()
    # delete record
    session.delete(albert_einstein)
    session.commit()
    # try to retrieve deleted record
    albert_einstein = query.first()
    print(albert_einstein)

    # If you don't have a single object ready for deletion but you know 
    # the criteria for deletion, you can call the delete() method 
    # from your query instead:
    query= session.query(Student).filter(Student.name=='Albert Einstein')
    query.delete()
    albert_einstein=query.first()
    print(albert_einstein)
