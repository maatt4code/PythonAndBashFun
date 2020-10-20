from datetime import datetime


def now() -> datetime:
    return datetime.utcnow()


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
