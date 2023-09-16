from _finders import BookFinder
import argparse


def run():
    parser = argparse.ArgumentParser(
        description='Find a top N books from the Glasgow University library\n'
                    '(specify title and the desired number of results as the command arguments)'
    )
    parser.add_argument('title', type=str)
    parser.add_argument('number', nargs='?', type=int, default=20)

    args = parser.parse_args()

    finder = BookFinder(args.title, args.number)
    print(f'Finding top {args.number} books with title {args.title}...')
    finder.find_books()
    print('Successfully found books!')
    finder.send_books()
    print('Successfully sent books to the server!')


if __name__ == '__main__':
    run()
