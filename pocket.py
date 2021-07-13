
# 60초의 시간안에 최대한 피카츄를 키워서 점수를 얻는 게임
# 잠자기 선택시 체력 10 증가, 4초간 대기
# 먹기 선택시 체력 5증가, 3초간 대기
# 운동하기 선택시 체력 10감소, 경험치 20증가, 점수 20점 증가, 4초간 대기
# 놀기 선택시 체력 5감소, 경험치 10증가, 점수 10점 증가 3초간 대기
# 레벨업 했을시 직전 레벨x100 점 증가 
# 죽었을때 경험치 10감소, 점수 50점 감소 6초간 대기
# 경험치와 체력은 음수가 되지 않음
# 초과 경험치로 레벨업 했을시 초과 경험치 이전됨

import pygame
import os

hp_max = 30               # 최대 체력, 더이상 증가하지 않음
hp = 30                   
exp = 0
exp_max = 50              # 레벨업을 하기위한 요구 경험치, 레벨업하면 직전 레벨x10 만큼 증가함
lev = 1
score = 0

def HpCheck(a) :           # 생명체크 함수
    global hp
    global exp
    global score
    if hp <= 0:
        exp -= 10          # 죽으면 경험치 감소
        if exp <= 0:       # 경험치가 음수가 되는 것을 방지
            exp = 0

        score -= 50        # 죽으면 점수 감소
        if score < 0 :
            score = 0
        return False       # 죽었을때 false값을 반환
    else :
        if a == 1 :
            score += 20    # 운동했을때 20점 증가
        elif a == 2 :
            score += 10    # 놀았을때 10점 증가
        return True        # 죽지않고 활동을 했을때 true 값을 반환
        

def LevCheck() :           # 레벨체크 함수
    global exp
    global exp_max
    global lev
    global hp
    global score
    if exp >= exp_max :     
        iAlpha = exp - exp_max  # 초과 경험치 부과
        exp = iAlpha
        exp_max += lev * 10     # 레벨업 요구 경험치 증가
        score += lev * 100
        lev += 1
        hp = hp_max     # 레벨업시 체력 충전
        
        

if __name__ == '__main__' :
    pygame.init()
    
    screen_width = 640     # 게임 창의 가로 크기
    screen_height = 480    # 게임 창의 세로 크기
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pikachu Game")     # 타이틀 이름

    current_path = os.path.dirname(__file__)      # 현재 파일의 위치 
    image_path = os.path.join(current_path, "images")   # 이미지 파일이 모여있는 위치

    background = pygame.image.load(os.path.join(image_path, "background.png"))   # 배경이미지
    initial_image = pygame.image.load(os.path.join(image_path, "initial_image.png"))   # 초기화면 메인이미지
    initial_image_size = initial_image.get_rect().size    # 초기화면 메인이미지 크기
    start_image = pygame.image.load(os.path.join(image_path, "start.png"))   # 초기화면 선택 이미지
    start_image_size = start_image.get_rect().size   # 초기화면 선택(start) 이미지 크기, 선택이미지 크기는 모두 같으므로 항상 이것으로 사용
    end_image = pygame.image.load(os.path.join(image_path, "end.png"))   # 초기화면 선택(end) 이미지, 크기는 위에걸로 이용
    select_image = pygame.image.load(os.path.join(image_path, "select.png"))  # 초기화면 선택을 하는 화살표 이미지
    select_image_size = select_image.get_rect().size    # 초기화면 선택을 하는 화살표 이미지 크기
    select_image_pos = [initial_image_size[1] + 25, initial_image_size[1] + start_image_size[1] + 25]  # 화살표의 위치, 무엇을 선택했는지 알기 위해 
    pika_image = pygame.image.load(os.path.join(image_path, "pika.png"))  # 피카츄 기본이미지
    pika_sleep_image = pygame.image.load(os.path.join(image_path, "sleep.png"))   # 피카츄 자는 이미지
    pika_eat_image = pygame.image.load(os.path.join(image_path, "eat.png"))   # 피카츄 식사 이미지
    pika_exercise_image = pygame.image.load(os.path.join(image_path, "exercise.png"))   # 피카츄 운동 이미지
    pika_play_image = pygame.image.load(os.path.join(image_path, "play.png"))    # 피카츄 놀기 이미지
    pika_size = pika_image.get_rect().size  # 피카츄 이미지의 크기, 피카츄 모든 이미지의 크기는 이것으로 사용
    pika_pos = (screen_width / 4 - pika_size[0] / 2, screen_height / 4 * 3 - pika_size[1] - 10)  # 피카츄 이미지 위치
    menu_image1 = pygame.image.load(os.path.join(image_path, "csleep.png"))   # 게임모드에서 선택 이미지
    menu_image2 = pygame.image.load(os.path.join(image_path, "ceat.png"))
    menu_image3 = pygame.image.load(os.path.join(image_path, "cexercise.png"))
    menu_image4 = pygame.image.load(os.path.join(image_path, "cplay.png"))
    menu_pos = [25, 50 + start_image_size[0], 75 + start_image_size[0] * 2, 100 + start_image_size[0] * 3] # 선택이미지의 위치들의 저장
    menu_select_image = pygame.image.load(os.path.join(image_path, "check.png"))  # 선택메뉴를 고르는 체크이미지
    menu_select_image_size = menu_select_image.get_rect().size # 선택메뉴를 고르는 체크이미지 크기
    # 선택이미지의 위치들을 저장, 무엇을 선택했는지 위치크기로 받아오기 위해서
    menu_select_image_pos = [menu_pos[i] + start_image_size[0] / 2 - menu_select_image_size[0] / 2 for i in range(0, len(menu_pos))]
    state_image = pygame.image.load(os.path.join(image_path, "state.png")) # 상태창 이미지
    state_image_size = state_image.get_rect().size # 상태창 이미지 크기
    heart_image = pygame.image.load(os.path.join(image_path, "heart.png"))  # 체력 이미지
    heart_image_size = heart_image.get_rect().size # 체력 이미지 크기, 체력과 경험치 크기를 다 이것으로 사용
    # 체력 이미지 위치들 저장
    heart_image_pos = [pika_pos[0] + pika_size[0] + 70, pika_pos[0] + pika_size[0] + heart_image_size[0] + 70,\
        pika_pos[0] + pika_size[0] + heart_image_size[0] * 2 + 70, pika_pos[0] + pika_size[0] + heart_image_size[0] * 3 + 70,\
            pika_pos[0] + pika_size[0] + heart_image_size[0] * 4 + 70, pika_pos[0] + pika_size[0] + heart_image_size[0] * 5 + 70]
    exp_image = pygame.image.load(os.path.join(image_path, "exp.png"))  # 경험치 이미지
    add_image = pygame.image.load(os.path.join(image_path, "add.png"))  # 더하기 이미지
    substract_image = pygame.image.load(os.path.join(image_path, "substract.png"))  # 빼기 이미지
    pika_die_image = pygame.image.load(os.path.join(image_path, "die.png"))  # 피카츄 죽었을때 이미지



    game_font = pygame.font.Font(None, 40)  # 게임 모드에서 쓰는 폰트
    game_font2 = pygame.font.Font(None, 100)  # 게임 끝나고 점수를 나타낼때 쓰는 폰트
    total_time = 60  # 전체 게임 제한시간
    initial_mode = True   # 초기화면 모드
    game_mode = False  # 게임화면 모드
    activity_mode = False  # 활동 모드
    die_check = False  # 죽었을때 화면 전환을 위해 체크
    initial_select_pos = select_image_pos[0]  # 초기화면에서 화살표 위치 설정
    game_select_pos = menu_select_image_pos[0]  # 게임화면에서 체크표시 위치 설정
    running = True # 피카츄게임을 실행할지 체크
    while running :
        
        screen.blit(background, (0, 0))  # 배경 출력

        for event in pygame.event.get() :   # 키보드 입력을 받기 위해 반복
            if event.type == pygame.QUIT :  # 게임창의 엑스표시를 누르면 게임 종료
                running = False

                
            if event.type == pygame.KEYDOWN :   # 키보드를 눌렀을때
                if initial_mode :
                    if event.key == pygame.K_UP :   # 업버튼
                        initial_select_pos = select_image_pos[0]  # 초기화면의 화살표 위치 변경
                    if event.key == pygame.K_DOWN :      # 다운 버튼 눌렀을때
                        initial_select_pos = select_image_pos[1]  # 초기화면의 화살표 위치 변경
                if game_mode and not activity_mode :
                    if event.key == pygame.K_LEFT :  # 왼쪽 버튼
                        if game_select_pos == menu_select_image_pos[3] :   # 게임화면의 선택 메뉴 변경
                            game_select_pos = menu_select_image_pos[2]
                        elif game_select_pos == menu_select_image_pos[2] :
                            game_select_pos = menu_select_image_pos[1]
                        elif game_select_pos == menu_select_image_pos[1] :
                            game_select_pos = menu_select_image_pos[0]
                    if event.key == pygame.K_RIGHT :  # 오른쪽 버튼
                        if game_select_pos == menu_select_image_pos[0] :   # 게임화면의 선택 메뉴 변경
                            game_select_pos = menu_select_image_pos[1]
                        elif game_select_pos == menu_select_image_pos[1] :
                            game_select_pos = menu_select_image_pos[2]
                        elif game_select_pos == menu_select_image_pos[2] :
                            game_select_pos = menu_select_image_pos[3]
                if event.key == pygame.K_SPACE :  # 스페이스 바
                    if initial_mode :  # 초기화면일 경우
                        if initial_select_pos == select_image_pos[0] :  # 시작을 선택
                            initial_mode = False  # 초기화면 끄기
                            game_mode = True  # 게임화면 켜기
                            start_ticks = pygame.time.get_ticks()  # 게임 시작 시간 체크
                            score = 0  # 게임 시작시 점수 설정
                        elif initial_select_pos == select_image_pos[1] :  # 게임 종료 선택
                            running = False
                    elif game_mode :   # 게임 모드일때
                        activity_mode = True  # 활동 선택함
                        temp_time = pygame.time.get_ticks()  # 활동을 시작한 시간 체크
                        
            if event.type == pygame.KEYUP :  # 키보드 누른것을 땠을때 
                if event.key == pygame.K_SPACE :  # 스페이스바를 땠을때
                    if game_select_pos == menu_select_image_pos[0] :  # 잠자기 선택했을때
                        hp += 10
                        if hp > hp_max :       # 최대 체력을 초과하면 최대 체력으로
                            hp = hp_max
                    elif game_select_pos == menu_select_image_pos[1] :  # 먹기를 선택했을때
                        hp += 5
                        if hp > hp_max :      # 최대 체력을 초과하면 최대 체력으로
                            hp = hp_max   
                    elif game_select_pos == menu_select_image_pos[2] :  # 운동하기를 선택했을때
                        hp -= 10
                        if hp > 0 :
                            exp += 20
                        if not HpCheck(1) :  # 운동하기를 알려주기 위해 매개변수 1을 대입, 생명체크를 해서 false값을 받아오면
                            die_check = True  # 죽은 이미지로 변경을 위해 죽음체크 true
                        LevCheck() # 레벨업 체크
                    elif game_select_pos == menu_select_image_pos[3] :  # 놀기를 선택했을때
                        hp -= 5
                        if hp > 0 :
                            exp += 10
                        if not HpCheck(2) :  # 놀기를 알려주기 위해 매개변수 2를 대입, 생명체크를 해서 false값을 받아오면
                            die_check = True  # 죽은 이미지로 변경을 위해 죽음체크 true
                        LevCheck()  # 레벨업 체크

        
        if initial_mode : # 초기화면일때
            screen.blit(initial_image, (screen_width / 2 - initial_image_size[0] / 2, 20)) # 초기화면 메인이미지 출력
            screen.blit(start_image, (screen_width / 2 - start_image_size[0] / 2, initial_image_size[1] + 20))  # 시작메뉴 이미지 출력
            screen.blit(end_image, (screen_width / 2 - start_image_size[0] / 2, initial_image_size[1] + start_image_size[1] + 20))  # 종료메뉴 이미지 출력
            screen.blit(select_image, (screen_width / 2 - start_image_size[0] / 2 - select_image_size[0], initial_select_pos)) # 선택화살표 이미지 출력
        elif game_mode :  # 게임화면일때
            if not activity_mode :  # 활동모드가 아니면
                screen.blit(pika_image, (pika_pos[0], pika_pos[1]))  # 기본 피카츄이미지 출력
                screen.blit(menu_image1, (menu_pos[0], pika_pos[1] + pika_size[1] + 20))  # 활동메뉴 이미지 출력
                screen.blit(menu_image2, (menu_pos[1], pika_pos[1] + pika_size[1] + 20))
                screen.blit(menu_image3, (menu_pos[2], pika_pos[1] + pika_size[1] + 20))
                screen.blit(menu_image4, (menu_pos[3], pika_pos[1] + pika_size[1] + 20))
                screen.blit(menu_select_image, (game_select_pos, pika_pos[1] + pika_size[1])) # 활동 선택 체크 이미지 출력
            elif activity_mode :  # 활동모드 일때
                if game_select_pos == menu_select_image_pos[0] :  # 잠자기일때
                    screen.blit(pika_sleep_image, (pika_pos[0], pika_pos[1])) # 잠자는 피카츄 이미지 출력
                    text = game_font.render("Pikachu is sleeping... Wait a minute.", True, (0, 0, 0)) # 자고 있다는 문구 출력
                    screen.blit(text, (menu_pos[0], pika_pos[1] + pika_size[1] + 20))  
                    update = game_font.render("HP   ", True, (0, 0, 0))  # 설명창 구성멤버들 출력
                    screen.blit(update, (menu_pos[0], pika_pos[1] + pika_size[1] + 60))
                    screen.blit(add_image, (menu_pos[0] + 50, pika_pos[1] + pika_size[1] + 60))
                    screen.blit(heart_image, (menu_pos[0] + heart_image_size[0] + 45, pika_pos[1] + pika_size[1] + 58))
                    screen.blit(heart_image, (menu_pos[0] + heart_image_size[0] * 2 + 45, pika_pos[1] + pika_size[1] + 58))
                    

                elif game_select_pos == menu_select_image_pos[1] :  # 먹기 일때
                    screen.blit(pika_eat_image, (pika_pos[0], pika_pos[1]))  # 식사중인 피카츄 이미지 출력
                    text = game_font.render("Pikachu is eating... Wait a minute.", True, (0, 0, 0)) # 식사중이라는 문구 출력
                    screen.blit(text, (menu_pos[0], pika_pos[1] + pika_size[1] + 20))  
                    update = game_font.render("HP   ", True, (0, 0, 0))  # 설명창 구성멤버들 출력
                    screen.blit(update, (menu_pos[0], pika_pos[1] + pika_size[1] + 60))
                    screen.blit(add_image, (menu_pos[0] + 50, pika_pos[1] + pika_size[1] + 60))
                    screen.blit(heart_image, (menu_pos[0] + heart_image_size[0] + 45, pika_pos[1] + pika_size[1] + 58))
                    

                elif game_select_pos == menu_select_image_pos[2] :  # 운동하기 일때
                    if not die_check : # 죽지 않았을때
                        screen.blit(pika_exercise_image, (pika_pos[0], pika_pos[1]))  # 운동하는 피카츄 이미지 출력
                        text = game_font.render("Pikachu is exercising... Wait a minute.", True, (0, 0, 0)) # 운동중이라는 문구 출력
                        screen.blit(text, (menu_pos[0], pika_pos[1] + pika_size[1] + 20))  
                        update1 = game_font.render("HP   ", True, (0, 0, 0))  # 설명창 구성멤버들 출력
                        screen.blit(update1, (menu_pos[0], pika_pos[1] + pika_size[1] + 60))
                        screen.blit(substract_image, (menu_pos[0] + 50, pika_pos[1] + pika_size[1] + 60))
                        screen.blit(heart_image, (menu_pos[0] + heart_image_size[0] + 45, pika_pos[1] + pika_size[1] + 58))
                        screen.blit(heart_image, (menu_pos[0] + heart_image_size[0] * 2+ 45, pika_pos[1] + pika_size[1] + 58))
                        update2 = game_font.render("EXP   ", True, (0, 0, 0))
                        screen.blit(update2, (menu_pos[0] + heart_image_size[0] * 3 + 55, pika_pos[1] + pika_size[1] + 60))
                        screen.blit(add_image, (menu_pos[0] + heart_image_size[0] * 5 + 60, pika_pos[1] + pika_size[1] + 60))
                        screen.blit(exp_image, (menu_pos[0] + heart_image_size[0] * 6 + 55, pika_pos[1] + pika_size[1] + 58))
                        screen.blit(exp_image, (menu_pos[0] + heart_image_size[0] * 7 + 55, pika_pos[1] + pika_size[1] + 58))
                    
                    if die_check :  # 죽었을때
                        screen.blit(pika_die_image, (pika_pos[0], pika_pos[1]))  # 죽은 피카츄 이미지 출력
                        text = game_font.render("Pikachu is dead... Wait a minute.", True, (0, 0, 0))  # 피카츄가 부활중 문구 출력
                        screen.blit(text, (menu_pos[0], pika_pos[1] + pika_size[1] + 20))

                elif game_select_pos == menu_select_image_pos[3] :  # 놀기 선택했을때
                    if not die_check : # 죽지 않았을때
                        screen.blit(pika_play_image, (pika_pos[0], pika_pos[1]))  # 노는 피카츄 이미지 출력
                        text = game_font.render("Pikachu is playing... Wait a minute.", True, (0, 0, 0)) # 노는중 이라는 문구 출력
                        screen.blit(text, (menu_pos[0], pika_pos[1] + pika_size[1] + 20))  
                        update1 = game_font.render("HP   ", True, (0, 0, 0))  # 설명창 구성멤버들 출력
                        screen.blit(update1, (menu_pos[0], pika_pos[1] + pika_size[1] + 60))
                        screen.blit(substract_image, (menu_pos[0] + 50, pika_pos[1] + pika_size[1] + 60))
                        screen.blit(heart_image, (menu_pos[0] + heart_image_size[0] + 45, pika_pos[1] + pika_size[1] + 58))
                        update2 = game_font.render("EXP   ", True, (0, 0, 0))
                        screen.blit(update2, (menu_pos[0] + heart_image_size[0] * 2 + 55, pika_pos[1] + pika_size[1] + 60))
                        screen.blit(add_image, (menu_pos[0] + heart_image_size[0] * 4 + 60, pika_pos[1] + pika_size[1] + 60))
                        screen.blit(exp_image, (menu_pos[0] + heart_image_size[0] * 5 + 55, pika_pos[1] + pika_size[1] + 58))
                    if die_check : # 죽었을때
                        screen.blit(pika_die_image, (pika_pos[0], pika_pos[1]))  # 죽은 피카츄 이미지 출력
                        text = game_font.render("Pikachu is dead... Wait a minute.", True, (0, 0, 0)) # 부활중이라는 문구 출력
                        screen.blit(text, (menu_pos[0], pika_pos[1] + pika_size[1] + 20))

            screen.blit(state_image, (pika_pos[0] + pika_size[0] + 20, pika_pos[1] - 40))  # 상태창 출력
            
            
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000  # 경과시간, 현재시간 - 게임시작시간
            timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (0, 0, 0)) # 남은시간 출력, 총제한시간 - 경과시간
            screen.blit(timer, (screen_width / 2 - 50, 20))
            score_output = game_font.render("Score : {}" .format(score), True, (0, 0, 0))  # 점수 출력
            screen.blit(score_output, (20, 20))
            if activity_mode == True :  # 활동모드 일때
                if game_select_pos == menu_select_image_pos[1] or game_select_pos == menu_select_image_pos[3] : # 식사나 놀기 일때
                    if die_check : # 죽었을때
                        if (pygame.time.get_ticks() - temp_time) / 1000 >= 6 :  # 6초간 대기
                            die_check = False
                            hp += 10  
                            exp -= 10
                            if exp <= 0 :
                                exp = 0                   
                    elif (pygame.time.get_ticks() - temp_time) / 1000 >= 3 :  # 식사나 놀기 일때 3초간 대기
                        activity_mode = False # 활동 끝
                elif game_select_pos == menu_select_image_pos[0] or game_select_pos == menu_select_image_pos[2] : # 잠자기나 운동일때
                    if die_check : # 죽었을때
                        if (pygame.time.get_ticks() - temp_time) / 1000 >= 6 :  # 6초간 대기
                            die_check = False 
                            hp += 10 
                            exp -= 10
                            if exp <= 0 :
                                exp = 0
                    elif (pygame.time.get_ticks() - temp_time) / 1000 >= 4 :  # 잠자기나 운동일때 4초간 대기
                        activity_mode = False 
                

            name = game_font.render("PIKACHU", True, (0, 0, 0))  # 상태창 출력
            screen.blit(name, (pika_pos[0] + pika_size[0] + 70, pika_pos[1]))
            LEV = game_font.render("LEV   {}" .format(lev), True, (0, 0, 0))
            screen.blit(LEV, (pika_pos[0] + pika_size[0] + 70, pika_pos[1] + 30))
            HP = game_font.render("HP", True, (0, 0, 0))
            screen.blit(HP, (pika_pos[0] + pika_size[0] + 70, pika_pos[1] + 60))
            for i in range(0, int(hp / 5)) :
               screen.blit(heart_image, (heart_image_pos[i], pika_pos[1] + 90))
            EXP = game_font.render("EXP   {}  /  {}" .format(exp, exp_max), True, (0, 0, 0))
            screen.blit(EXP, (pika_pos[0] + pika_size[0] + 70, pika_pos[1] + 125))
            for i in range(0, int(exp / 10)) :
                if i < 5 :
                    screen.blit(exp_image, (heart_image_pos[i], pika_pos[1] + 155))
                if 5 <= i < 10 :
                    screen.blit(exp_image, (heart_image_pos[i % 5], pika_pos[1] + 185))
                if 10 <= i < 15 :
                    screen.blit(exp_image, (heart_image_pos[i % 5], pika_pos[1] + 215))    
                        

            if total_time - elapsed_time <= 0 :  # 제한시간이 경과했을때
                screen.blit(background, (0, 0))
                msg1 = game_font2.render("Game Over", True, (200, 150, 0)) # 게임오버 문구 출력
                msg_rect = msg1.get_rect(center = (int(screen_width / 2), int(screen_height / 2) - 60))
                screen.blit(msg1, msg_rect)
                msg2 = game_font2.render("Score  {}" .format(score), True, (200, 150, 0))  # 총 점수 출력
                msg_rect = msg2.get_rect(center = (int(screen_width / 2), int(screen_height / 2) + 20))
                screen.blit(msg2, msg_rect)

                pygame.display.update()
                pygame.time.delay(3000)  # 게임 끝나고 3초간 대기

                initial_mode = True  # 초기 화면으로 전환
                game_mode = False

        pygame.display.update()

    pygame.quit()