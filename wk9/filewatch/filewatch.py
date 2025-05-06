import inotify.adapters

def main():
  notifier = inotify.adapters.Inotify()

  notifier.add_watch('./temp')

  for event in notifier.event_gen(yield_nones=False):
    (_, type_names, path, filename) = event
    print(f"path=[{path}] filename=[{filename}] events=[{type_names}]")

if __name__ == '__main__':
  main()