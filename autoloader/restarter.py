import os
import signal
import stat
import sys
import subprocess
import time


THIS_SCRIPTS_DIR = os.path.realpath(os.path.dirname(__file__))
GAME_ROOT_DIR = os.path.join(THIS_SCRIPTS_DIR, os.pardir)


def launch_game():
  game_main = os.path.join(GAME_ROOT_DIR, 'main.py')
  if not os.path.exists(game_main):
    raise FileNotFoundError('Expected game main at %s' % game_main)

  python = sys.executable
  proc = subprocess.Popen([python, game_main])
  return proc


def kill_game(pid_filename):
  if not os.path.exists(pid_filename):
    return
  with open(pid_filename, 'r') as pidfile:
    pid = pidfile.read()
  os.remove(pid_filename)
  try:
    os.kill(int(pid), signal.SIGTERM)
  except OSError:
    print('Failed to kill pid=%s, probably already dead' % pid)


def write_pidfile(proc, pid_filename):
  with open(pid_filename, 'w') as pidfile:
    pidfile.write(str(proc.pid))


def list_game_files():
  # Notably, leaves out .pyc files. Does not recurse into dirs.
  files = sorted([f for f in os.listdir(GAME_ROOT_DIR)
                  if f.endswith('.py')])
  return [os.path.join(GAME_ROOT_DIR, f) for f in files]


def get_modified_times(paths):
  return [os.stat(path).st_mtime for path in paths]


def start_fresh_game():
  print('Restarting!')
  pid_filename = 'game.pid'

  kill_game(pid_filename)
  proc = launch_game()
  write_pidfile(proc, pid_filename)


def main():
  start_fresh_game()
  game_files = list_game_files()
  modified_times = get_modified_times(game_files)
  while True:
    files_now = list_game_files()
    if files_now != game_files:
      game_files = files_now
      modified_times = get_modified_times(game_files)
      start_fresh_game()
    modified_times_now = get_modified_times(game_files)
    if modified_times_now != modified_times:
      modified_times = modified_times_now
      start_fresh_game()

    time.sleep(2)


if __name__ == '__main__':
  sys.exit(main())
