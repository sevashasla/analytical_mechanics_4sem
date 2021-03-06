from modeling import Model
import argparse

def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Hello! You are trying to run my project of analytic mechanics"
    )
    parser.add_argument("-m", dest="m", default=1, type=float, help="mass of every body")
    parser.add_argument("-b", dest="b", default=1, type=float, help="dissipation coefficient")
    parser.add_argument("-c", dest="c", default=1, type=float, help="stiffness coefficient")
    parser.add_argument("-t", dest="timedelta", default=1.0, type=float, help="how many seconds in one real second") # or make per iteration?
    parser.add_argument("-r", dest="r", default=200, type=float, help="radius of the main circle")
    parser.add_argument('--q0', dest="q0", action='store', type=float, help='initial state', nargs=4)
    args = parser.parse_args()

    model = Model(args.m, args.c, args.b, args.timedelta, args.q0, args.r)
    model.run()

if __name__ == "__main__":
    main()
