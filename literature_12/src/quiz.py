from bs4 import BeautifulSoup
import requests
import random

def getSoup(url):
    html = requests.get(url).text
    return BeautifulSoup(html, "html.parser")


def r():
    return random.randint(0, 100)

def randomOp():
    operations = ['+', '-', '*', '/']

    return operations[random.randint(0, len(operations) - 1)]


equations = []

for i in range(100):
    equation = f'{r()} {randomOp()} {r()} {randomOp()} {r()} {randomOp()} {r()}'

    if equation in equations:
        continue

    equations.append(equation)

for eq in equations:
    print(eq)