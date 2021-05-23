from datetime import datetime


def now() -> datetime:
    return datetime.utcnow()


def timestamp_to_microsec(ts: str, fmt: str = "%Y-%m-%d %H:%M:%S.%f") -> int:
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.strptime(ts, fmt)
    delta = (now - epoch).total_seconds()
    delta *= 1000000
    return int(delta)


def info(msg):
    print("[%s] INFO : %s" % (now(), msg))


def warn(msg):
    print("[%s] WARN : %s" % (now(), msg))


def err(msg):
    print("[%s] ERRO : %s" % (now(), msg))


def die(msg):
    err(msg)
    exit(-1)


def main():
    info("Test")


if __name__ == '__main__':
    main()
