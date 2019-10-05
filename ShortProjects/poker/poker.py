import pygame
import sys
import util
import random
from pygame.locals import QUIT
from pygame.rect import Rect

# 상수
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (90, 90, 90)
BLACK = (0, 0, 0)
CARD_SIZE = (80, 120)
CARD_0_POS = (80, 150)
CARD_1_POS = (180, 150)
CARD_2_POS = (280, 150)
CARD_3_POS = (380, 150)
CARD_4_POS = (480, 150)
CARD_POSITIONS = (CARD_0_POS, CARD_1_POS, CARD_2_POS, CARD_3_POS, CARD_4_POS)
GAME_STATE = ('START', 'GET_CARD', 'CHANGE_CARD', 'QUIT', 'RESTART', 'GUIDE')

# 변수
card0 = Rect(CARD_0_POS, CARD_SIZE)
card1 = Rect(CARD_1_POS, CARD_SIZE)
card2 = Rect(CARD_2_POS, CARD_SIZE)
card3 = Rect(CARD_3_POS, CARD_SIZE)
card4 = Rect(CARD_4_POS, CARD_SIZE)
chat = Rect((50, 300), (540, 160))
message_string = ''
result_message_string = ''
multiple = 1
running = True
is_game_end = False


class MyState:
    money = 100
    my_cards = []
    # 이번 게임에서 카드를 바꾼 횟수
    change_count = 0

    def init(self):
        self.my_cards = []
        self.change_count = 0


class GameState:
    state = 'START'
    # 게임 내 사용하는 카드 한 벌
    deck = list(range(52))

    def init(self):
        self.state = 'START'
        self.deck = list(range(52))


pygame.init()
pygame.font.init()

pygame.display.set_caption("poker")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
font = pygame.font.SysFont('nanummyeongjottc', 15)
money_font = pygame.font.SysFont('nanummyeongjottc', 25)


def show_ui(my_state):
    screen.fill(WHITE)

    # 카드가 놓일 빈 칸
    pygame.draw.rect(screen, GRAY, card0)
    pygame.draw.rect(screen, GRAY, card1)
    pygame.draw.rect(screen, GRAY, card2)
    pygame.draw.rect(screen, GRAY, card3)
    pygame.draw.rect(screen, GRAY, card4)

    # 대화창
    pygame.draw.rect(screen, DARK_GRAY, chat)
    # \n을 줄 단위로 보고 나눠서 출력
    message_lines = message_string.split('\n')
    line_pos = [320, 320]
    for line in message_lines:
        message = font.render(line, False, WHITE)
        message_rect = message.get_rect()
        message_rect.center = (line_pos[0], line_pos[1])
        screen.blit(message, message_rect)
        line_pos[1] += 30

    # 소지금 출력
    screen.blit(money_font.render('소지금: ' + str(my_state.money), False, BLACK), (10, 10))


def show_card(index, id):
    image = pygame.image.load("cards/" + util.get_sprite_name(id) + ".png")
    screen.blit(image, CARD_POSITIONS[index])


def set_message(str):
    global message_string
    message_string = str


def get_card(game_state, my_state):
    # 카드를 한 장 얻기
    get_random_id = random.choice(game_state.deck)
    my_state.my_cards.append(get_random_id)
    game_state.deck.remove(get_random_id)
    # print(str(get_random_id))


def change_card(game_state, my_state, index):
    # 인덱스에 해당하는 카드를 바꾸기
    my_state.change_count += 1
    price = 2 ** my_state.change_count
    my_state.money -= price
    get_random_id = random.choice(game_state.deck)
    my_state.my_cards[index] = get_random_id
    game_state.deck.remove(get_random_id)
    # print(str(get_random_id))


def exchange(game_state, my_state, is_forced_exchange=False):
    global result_message_string
    money = util.get_exchange_money(my_state.my_cards)
    result_message_string = ''
    if is_forced_exchange:
        result_message_string += '더 카드를 바꿀 수 없어 강제로 패가 계산되었습니다.\n'
    result_message_string += '패를 계산합니다.\n'
    result_message_string += '당신은 ' + str(money) + '원을 환전받았습니다.'
    my_state.money += money
    game_state.state = 'QUIT'


def handle_input(game_state, my_state, key):
    global running

    if key == pygame.K_ESCAPE:
        running = False

    if is_game_end:
        return

    if game_state.state == 'START' or game_state.state == 'RESTART':
        # 1: 게임 시작, 0: 게임 종료
        if key == pygame.K_KP1 or key == pygame.K_1:
            my_state.init(my_state)
            game_state.init(game_state)
            my_state.money -= 1
            game_state.state = 'GET_CARD'
        elif key == pygame.K_KP0 or key == pygame.K_0:
            running = False
    elif game_state.state == 'GET_CARD':
        # 1: 카드 한 장 받기, 0: 환전하기
        if key == pygame.K_KP1 or key == pygame.K_1:
            my_state.money -= 1
            get_card(game_state, my_state)
            # 카드를 모두 받았으면 CHANGE_CARD 스테이트로
            if len(my_state.my_cards) == 5:
                game_state.state = 'CHANGE_CARD'
        elif key == pygame.K_KP0 or key == pygame.K_0:
            exchange(game_state, my_state)
    elif game_state.state == 'CHANGE_CARD':
        # 1~5: 카드 한 장 바꾸기, 0: 환전하기
        if key == pygame.K_KP1 or key == pygame.K_1:
            change_card(game_state, my_state, 0)
        elif key == pygame.K_KP2 or key == pygame.K_2:
            change_card(game_state, my_state, 1)
        elif key == pygame.K_KP3 or key == pygame.K_3:
            change_card(game_state, my_state, 2)
        elif key == pygame.K_KP4 or key == pygame.K_4:
            change_card(game_state, my_state, 3)
        elif key == pygame.K_KP5 or key == pygame.K_5:
            change_card(game_state, my_state, 4)
        elif key == pygame.K_KP0 or key == pygame.K_0:
            exchange(game_state, my_state)


def get_exchange_state_message(my_state):
    message = ''
    if len(my_state.my_cards) < 5:
        return message
    made = util.get_made(my_state.my_cards)
    if util.is_made(my_state.my_cards):
        message += 'Made! '
    message += made + ' -> ' + str(util.get_exchange_money(my_state.my_cards)) + '원\n'
    if made == '트리플':
        message += '(풀하우스: 250원, 포카드: 1000원)\n'
    elif made == '투페어':
        message += '(풀하우스: 250원)\n'
    elif made == '원페어':
        message += '(투페어: 25원, 트리플: 40원)\n'
    return message


def update_ui(game_state, my_state):
    global result_message_string
    # 대화창의 글 설정하기
    if game_state.state == 'START':
        set_message(
            '규칙은 간단해. 카드 다섯 장까지는 1만 받아\n' +
            '다섯 장을 받고 나면 한 장씩 바꿀때마다 2배로 돈을 지불하면 돼\n' +
            '그리고 돈이 부족하거나 그만 바꾸고 싶을 때, 패를 돈으로 환전하면 돼. 간단하지\n' +
            '[1] 시작한다(1원)        [0] 나간다'
        )
    elif game_state.state == 'RESTART':
        set_message(result_message_string + '\n게임을 다시 시작하겠나?\n[1] 시작한다(1원)        [0] 나간다')
    elif game_state.state == 'GET_CARD':
        set_message(get_exchange_state_message(my_state) + '[1] 한 장을 받는다(1원)        [0] 패 환전하기')
    elif game_state.state == 'CHANGE_CARD':
        price = 2 ** (my_state.change_count + 1)
        set_message(get_exchange_state_message(my_state) + '[1~5] 한 장을 바꾼다(' + str(price) + ')        [0] 패 환전하기')

    # 카드 그려주기
    index = 0
    for card in my_state.my_cards:
        show_card(index, card)
        index += 1


def win_game():
    global is_game_end
    set_message('축하합니다! 10,000원을 벌어 게임을 승리했습니다.')
    is_game_end = True


def fail_game():
    global is_game_end
    set_message('당신은 파산했습니다.')
    is_game_end = True


def main():
    game_state = GameState
    my_state = MyState

    """메인 루프"""
    while running:
        clock.tick(10)
        show_ui(my_state)

        # 이벤트
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                handle_input(game_state, my_state, event.key)

        update_ui(game_state, my_state)

        # 현재 판 종료 조건
        if game_state.state == 'QUIT':
            if my_state.money > 5:
                game_state.state = 'RESTART'
            else:
                fail_game()
        elif len(my_state.my_cards) == 5 and my_state.money < 2 ** (my_state.change_count + 1):
            # 카드를 바꿀 돈이 없으면 강제 환전
            exchange(game_state, my_state, True)

        # 게임 종료 조건
        if my_state.money < 0:
            fail_game()
        elif my_state.money > 10000:
            win_game()

        pygame.display.update()


if __name__ == '__main__':
    main()

# 이미지 출처(오픈소스) : https://code.google.com/archive/p/vector-playing-cards/