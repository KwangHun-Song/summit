import util


def get_sprite_name(id):
    suit = util.suit(id)
    if suit == 0:
        suitName = 'spades'
    elif suit == 1:
        suitName = 'diamonds'
    elif suit == 2:
        suitName = 'hearts'
    else:
        suitName = 'clubs'

    rank = util.rank(id)
    if rank == 14:
        rankName = 'ace'
    elif rank == 11:
        rankName = 'jack'
    elif rank == 12:
        rankName = 'queen'
    elif rank == 13:
        rankName = 'king'
    else:
        rankName = rank

    return str(rankName) + '_of_' + suitName


def suit(id):
    return int(id / 13)


def rank(id):
    rank = id % 13
    if rank == 1:
        rank = 14
    elif rank == 0:
        rank = 13
    return rank


def is_straight_flush(cards):
    return is_straight(cards) and is_flush(cards)


def is_four_card(cards):
    return get_pair_status(cards) == [3]


def is_full_house(cards):
    return get_pair_status(cards) == [1, 2]


def is_flush(cards):
    suits = list(map(util.suit, cards))
    suit = util.suit
    if (suits[0] == suits[1] and
            suits[1] == suits[2] and
            suits[2] == suits[3] and
            suits[3] == suits[4]):
        return True
    return False


def is_straight(cards):
    ranks = list(map(util.rank, cards))
    if (ranks[0] == ranks[1] - 1 and
            ranks[1] == ranks[2] - 1 and
            ranks[2] == ranks[3] - 1 and
            ranks[3] == ranks[4] - 1):
        return True
    elif (ranks[0] == 14 and
          ranks[1] == 2 and
          ranks[2] == 3 and
          ranks[3] == 4 and
          ranks[4] == 5):
        return True

    return False


def is_triple(cards):
    return get_pair_status(cards) == [2]


def is_two_pair(cards):
    return get_pair_status(cards) == [1, 1]


def is_one_pair(cards):
    return get_pair_status(cards) == [1]


def get_pair_status(cards):
    # 1 -> 2장짜리 페어, 2 -> 3장짜리 페어, 3 -> 4장짜리 페어
    print('cards: ' + str(cards))
    ranks = list(map(util.rank, cards))
    print('ranks: ' + str(ranks))
    pairs = []
    prev_rank = -1
    pair_number = 0
    # 같은 숫자가 연속되면 다른 숫자가 나올 때까지 pair_number에 1을 더해서 pairs에 추가하기
    for rank in ranks:
        if prev_rank == -1:
            prev_rank = rank
            continue
        elif prev_rank == rank:
            pair_number += 1
        elif pair_number > 0:
            pairs.append(pair_number)
            pair_number = 0
            prev_rank = rank
        else:
            prev_rank = rank
    if pair_number > 0:
        pairs.append(pair_number)

    print('pairs: ' + str(pairs))
    print('sorted: ' + str(sorted(pairs)))
    return sorted(pairs)


def get_made(cards):
    if len(cards) < 5:
        return '탑'
    # 카드 랭크로 정렬
    sorted_cards = sorted(cards, key=lambda card: rank(card))
    if is_straight_flush(sorted_cards):
        return '스트레이트플러시'
    elif is_four_card(sorted_cards):
        return '포카드'
    elif is_full_house(sorted_cards):
        return '풀하우스'
    elif is_flush(sorted_cards):
        return '플러시'
    elif is_straight(sorted_cards):
        return '스트레이트'
    elif is_triple(sorted_cards):
        return '트리플'
    elif is_two_pair(sorted_cards):
        return '투페어'
    elif is_one_pair(sorted_cards):
        return '원페어'
    return '탑'


def get_exchange_money(cards):
    if len(cards) < 5:
        return 0
    made = get_made(cards)
    if made == '스트레이트플러시':
        return 5000
    elif made == '포카드':
        return 1000
    elif made == '풀하우스':
        return 250
    elif made == '플러시':
        return 120
    elif made == '스트레이트':
        return 80
    elif made == '트리플':
        return 40
    elif made == '투페어':
        return 25
    elif made == '원페어':
        return 13
    return 0


def is_made(cards):
    if len(cards) < 5:
        return False
    elif get_made(cards) == '탑':
        return False
    else:
        return True
