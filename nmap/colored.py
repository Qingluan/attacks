#!/usr/bin/env python3


def console_format():
    import sys
    from termcolor import colored
    from qlib.text import mark
    from qlib.io import GeneratorApi
    import os


    BLUE='\033[0;34m'
    GREEN='\033[0;32m'
    CYAN='\033[0;35m'
    RED='\033[0;31m'
    YELLOW='\033[0;36m'
    NC='\033[0m'

    args = GeneratorApi({
            'key':'set special key',
            'style':'set style',
        })

    paragraph = []
    dis = False
    for l in sys.stdin:
        

        cons = l.split()
        if not l.strip():
            dis = True
        for i,v in enumerate(cons):
            if v.endswith(":"):
                cons[i] = colored(cons[i],"red")
                try:
                    cons[i+1] = GREEN + cons[i+1]
                except IndexError:
                    pass
            if v.startswith("http"):
                cons[i] = colored(cons[i], attrs=['underline'])
        
        line = NC + ' '.join(cons)
        if args.key:
            line = mark(line, args.key, attrs=['bold','blink'])

        print(line)
    #     paragraph.append(line)
    #     if dis:
    #         colmT = True
    #         for l in paragraph:

    #             fe =  l.split()[0].strip()
    #             print(fe, len(fe),fe.find(":"))
    #             if fe.find(":") <=4 and len(fe) > 4:
    #                 colmT = False
    #         if colmT:
    #             print("---- form")
    #             res = os.popen("column -t  <<< '%s'" % '\n'.join(paragraph)).read()
    #         else:
    #             res = '\n'.join(paragraph)
    #         print(res)
    #         paragraph = []
    #         dis = False

    # if paragraph:
    #     res = '\n'.join(paragraph)
    #     print(res)
    #     dis = False
    #     paragraph = []


if __name__ == '__main__':
    console_format()