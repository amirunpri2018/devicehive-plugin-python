from plugin import Plugin, Handler


access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJwYXlsb2FkIjp7ImEiOlswXSwiZSI6MjA4MzY3NDI1ODc4MiwidCI6MSwidHBjIjoicGx1Z2luX3RvcGljXzgxNTkwNGNmLWU1YzUtNGViYy04NjNkLTUyYjNmOTNmMGNmMCJ9fQ.52qdDOSDWfr-PiI68R-MZjCV1MIOOAaI0AXEThlRyoQ'


def main():
    p = Plugin(Handler, access_token)
    p.connect('ws://127.0.0.1:3000')


if __name__ == '__main__':
    main()
