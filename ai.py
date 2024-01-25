# ---------------------------------
# AWS CodeWhisper ai code generated
# ---------------------------------
from django.core.cache import cache

def factorial(n):\
    if n in cache:
        return cache[n]
    else:
        cache[n] = n * factorial(n - 1)
        return cache[n]

# fibonacci function with cache
def fibonacci(n):
    if n in cache:
        return cache[n]
    else:
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]


# -----------------------------    
# Google Bard AI code generated
# -----------------------------
class Emailer:
    def __init__(self, email_address):
        self.email_address = email_address

    def generate_email_body(self, name, message):
        body = f"Hi {name},\n\n{message}\n\nSincerely,\nThe Team"
        return body

    def send_email(self, body):
        # Email sending logic using an external library
        return True

emailer = Emailer("example@domain.com")
body = emailer.generate_email_body("John", "This is a test email")
emailer.send_email(body)

class EmailBodyGenerator:
    def generate_email_body(self, name, message):
        body = f"Hi {name},\n\n{message}\n\nSincerely,\nThe Team"
        return body

class EmailSender:
    def __init__(self, email_service):
        self.email_service = email_service

    def send_email(self, email_address, body):
        self.email_service.send_email(email_address, body)

email_body_generator = EmailBodyGenerator()
body = email_body_generator.generate_email_body("John", "This is a test email")
email_sender = EmailSender(EmailService())  # Replace with actual service
email_sender.send_email("example@domain.com", body)


class Shape:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_area(self):
        raise NotImplementedError

class Square(Shape):
    def calculate_area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return 3.14 * self.radius**2

square = Square(5, 5)
circle = Circle(10)

# New shapes require extending existing classes which might not be ideal

print(square.calculate_area())
print(circle.calculate_area())


from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def calculate_area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return 3.14 * self.radius**2

# Extend functionality without modifying existing classes
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def calculate_area(self):
        return 0.5 * self.base * self.height


square = Rectangle(5, 5)
circle = Circle(10)
triangle = Triangle(5, 10)

print(square.calculate_area())
print(circle.calculate_area())
print(triangle.calculate_area())
