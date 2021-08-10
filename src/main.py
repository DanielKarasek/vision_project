from controller import Controller
from model import Model
from view import View


def main():
  C = Controller(Model(), View())
  C.run()


if __name__ == '__main__':
  main()
