import sqlite3


def main():
  connection = sqlite3.connect('library.db')
  cursor = connection.cursor()
  
  
if __name__ == '__main__':
  main()
