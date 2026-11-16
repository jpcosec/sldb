"""`sldb bench`: the fixed speed benchmark (V0).

It copies desks into a work directory, runs the sldb and deskops commands on the copies in
cold and warm mode, and measures each child process with `os.wait4`: wall time, CPU and
maximum RSS. deskops is measured as an external CLI (a consumer), never imported.
"""
