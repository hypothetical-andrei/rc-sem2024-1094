from ftplib import FTP

def main():
  ftp = FTP()
  ftp.connect('localhost', 2121)
  ftp.login()
  with open('a.txt', 'wb') as fp:
    ftp.retrbinary('retr a.txt', fp.write)

if __name__ == '__main__':
  main()