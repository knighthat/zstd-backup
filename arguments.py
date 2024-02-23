from multiprocessing import cpu_count


class Arguments:
    def __init__(self, level: int, threads: int):
        # 'level' accepts any negative numbers but limits
        # to the level 22 on the positive end.
        self.level = min(level, 22)

        # If provided 'threads' exceeds valid value
        # (more than -1 and less than maximum available cpus)
        # then apply correction.
        if 0 <= threads <= cpu_count():
            self.threads = threads
        else:
            self.threads = 0

        # Set threads to the highest if current number is 0
        if self.threads == 0:
            self.threads = cpu_count()
