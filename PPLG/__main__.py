# PPLG.__main__.py
# CodeWriter21

import traceback
import importlib_resources
from log21 import get_logger, ColorizingArgumentParser, get_colors as gc
from PPLG.lib.Generate import extend_words_iter, generate

logger = get_logger('PyPassListGen', show_level=False)

with importlib_resources.path('PPLG', 'm1.txt') as ph:
    methods1_path = str(ph)
with importlib_resources.path('PPLG', 'm2.txt') as ph:
    methods2_path = str(ph)


# Main function
def main():
    global methods1_path, methods2_path
    parser = ColorizingArgumentParser()
    parser.add_argument('mode', type=str, choices=['ExtendWords', 'Gen', 'e', 'g'],
                        help=f'{gc("lg")}ExtendWords{gc("lr")}({gc("lg")}e{gc("lr")}):{gc("lb")} ' +
                             'Makes new words using the built-in methods' + gc('rst') + ' - ' +
                             f'{gc("lg")}Gen{gc("lr")}({gc("lg")}g{gc("lr")}):{gc("lb")} Generates passwords' +
                             gc("rst"))
    parser.add_argument('wordlist', type=str, help=gc('lb') + 'The path to the wordlist file.' + gc('rst'))
    parser.add_argument('savepath', type=str, help=gc('lb') + 'The path to save the results.' + gc('rst'))
    parser.add_argument('--methods1', '-m', type=str, dest='methods1',
                        help=gc('lb') + f'The path to the file containing methods to be used{gc("lr")}({gc("lb")}' +
                             f'Default: {gc("y")}{methods1_path}{gc("lr")})' + gc('rst'),
                        default=methods1_path)
    parser.add_argument('--methods2', '-M', type=str, dest='methods2',
                        help=gc('lb') + f'The path to the file containing methods to be used{gc("lr")}({gc("lb")}' +
                             f'Default: {gc("y")}{methods2_path}{gc("lr")})' + gc('rst'),
                        default=methods2_path)
    args = parser.parse_args()

    if args.methods1:
        methods1_path = args.methods1
    if args.methods2:
        methods2_path = args.methods2

    with open(args.wordlist, 'r') as file:
        words = set(file.read().split('\n'))
    logger.info(f'Loaded {len(words)} words!')
    with open(methods1_path, 'r') as file:
        methods1 = set(file.read().split('\n'))
    with open(methods2_path, 'r') as file:
        methods2 = set(file.read().split('\n'))

    logger.info('Starting...')
    if args.mode == 'ExtendWords' or args.mode == 'e':
        with open(args.savepath, 'w') as file:
            for word in extend_words_iter(words):
                logger.info('\r' + word, end='')
                file.write(word + '\n')
        logger.info('')
        logger.info('Done!')
    elif args.mode == 'Gen' or args.mode == 'g':
        logger.info(f'Loaded {len(methods1)} methods!')
        logger.info(f'Loaded {len(methods2)} methods!')
        logger.info('Generating Passwords...')
        output = generate(words, methods1, methods2, max_threads=1)
        if output[0]:
            print(traceback.format_exception_only(type(output[0]), output[0])[0])
        logger.info(f'Generated {len(output[1])} passwords!')
        logger.info('Saving...')
        with open(args.savepath, 'w') as file:
            for password in output[1]:
                file.write(password + '\n')
        logger.info('Done!')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.error('\033[91mKeyboardInterrupt: Cancelled!')
