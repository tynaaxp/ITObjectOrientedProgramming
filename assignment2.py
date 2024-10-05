#Phuong Thai
#U32184606
#phuongtranxuanthai

class Person:
    """
    this class represents a person with attributes like person_id, name and date of birth,
    the person class has a method called person_details.
    """
    def __init__(self, person_id, name, dob):
        """
        assign attributes to person_id, name and dob.
        """
        self.person_id = person_id
        self.name = name
        self.dob = dob

    def person_details(self):
        """
        this method returns the person's information.
        """
        return f"Person ID: {self.person_id}\nName: {self.name}\nDOB: {self.dob}"
    
class Task:
    """
    this class represents a task with a task id, title, required taskers
    this class has four methods: task_details, add_tasker, remove_tasker, and total_taskers
    """
    def __init__(self, task_id, title, required_taskers):
        """
        set the attribute for task id, title, required taskers and create an empty list
        of who are doing the task
        """
        self.task_id = task_id
        self.title = title
        self.required_taskers = required_taskers
        self.list_taskers = []

    def task_details(self):
        """
        this method return the task details and the tasker who is doing the task
        """

        details = f"Task ID: {self.task_id}\nTitle: {self.title}\nRequired taskers: {self.required_taskers}\n\n"
        for tasker in self.list_taskers:
            details += f"Person ID: {tasker.person_id}\nName: {tasker.name}\nDOB: {tasker.dob}\n\n"
        return details
    
    def add_tasker(self,person):
        """
        this method add tasker to the list 
        if they are not on the list yet and
        if the list have less or enough the required taskers
        """
        if person not in self.list_taskers and len(self.list_taskers) < self.required_taskers:
            self.list_taskers.append(person)
            return True
        else:
            return f"Invalid operation"
        
    def remove_tasker(self, person):
        """
        if the tasker is on the list, this method remove the person 
        """
        if person in self.list_taskers:
            self.list_taskers.remove(person)
            return True
        else: 
            return f"Invalid operation"
        
    def total_taskers(self):
        """
        return the number of taskers that are doing the task
        """
        return len(self.list_taskers)

person1 = Person(1, "John Doe", "1990-05-15")
print(person1.person_details())

person2 = Person(2, "Jane Smith", "1985-10-20")
person3 = Person(3, "Tim Brown", "2000-03-06")
task1 = Task(1, "Task1", 2)
print(task1.task_details())

print(task1.remove_tasker(person1))
print(task1.add_tasker(person1))
print("Number of Taskers = ", task1.total_taskers())

print(task1.add_tasker(person2))
print(task1.add_tasker(person3))


task2 = Task(2, "Task2", 5)

