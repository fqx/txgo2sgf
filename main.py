#!/usr/bin/python3
import requests, sys, re
from sgfmill import sgf
players_info = ('PB', 'BR', 'PW', 'WR')
id_re = re.compile('chessid=(\d+)')


def error_func(error_code):
    error_codes = {
        100: "输入错误，按任意键退出。"
    }
    input(error_codes[error_code])
    exit(error_code)


def get_sgfid(url):
    try:
        sgfid = int(id_re.search(url).groups()[0])
    except (IndexError, AttributeError):
        error_func(100)
    return sgfid


def get_sgf(sgfid:int):
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    data = 'command=1&url=https%3A%2F%2Fcgi.huanle.qq.com%2Fhappyapp%2Fcgi-bin%2FCommonMobileCGI%2FTXWQFetchChess%3Fchessid%3D{}'.format(sgfid)
    r = requests.post('https://h5.txwq.qq.com/txwqshare/static/php/jsonp.php', data=data, headers=headers, timeout=5)
    r.encoding = 'utf-8'
    sgf = r.json()['chess']

    return sgf


def modify_sgf(sgf_str):
    game = sgf.Sgf_game.from_string(sgf_str)
    if game.get_komi == 375:
        game.get_root().set('KM', '7.5')
    return game


def get_players(game):
    d = list()
    for i in players_info:
        d.append(game.get_root().get(i))
    return d


if __name__ == '__main__':
    # assert sys.argv[1], "You didn't add any sgfid as argument."
    try:
        sgfid = int(sys.argv[1])
    except ValueError:
        sgfid = get_sgfid(sys.argv[1])
    except IndexError:
        link = input('请输入腾讯围棋分享链接或chessid：')
        try:
            sgfid = int(link)
        except ValueError:
            sgfid = get_sgfid(link)
        except:
            error_func(100)
    sgf_str = get_sgf(sgfid)
    game = modify_sgf(sgf_str)
    players = get_players(game)
    filename = '{}「{}」 VS {}「{}」{}.sgf'.format(*players, sgfid)
    with open(filename, 'wb') as f:
        f.write(game.serialise())


