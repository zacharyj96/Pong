import sys
import pygame
from random import randint

WINDOWWIDTH = 750
WINDOWHEIGHT = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class SidePaddle(pygame.sprite.Sprite):

    def __init__(self, w, h):
        super().__init__()

        self.image = pygame.Surface([w, h])

        self.image = pygame.image.load("paddle_side_bg.png").convert_alpha()

        self.rect = self.image.get_rect()

    def up(self, distance):
        self.rect.y -= distance
        if self.rect.y < 0:
            self.rect.y = 0

    def down(self, distance):
        self.rect.y += distance
        if self.rect.y > 425:
            self.rect.y = 425


class TopBottomPaddle(pygame.sprite.Sprite):
    def __init__(self, w, h):
        super().__init__()

        self.image = pygame.Surface([w, h])

        self.image = pygame.image.load("paddle_top_bottom_bg.png").convert_alpha()

        self.rect = self.image.get_rect()

    def left(self, distance):
        self.rect.x -= distance
        if self.rect.x < (WINDOWWIDTH - 2) / 2:
            self.rect.x = (WINDOWWIDTH - 2) / 2

    def right(self, distance):
        self.rect.x += distance
        if self.rect.x > 675:
            self.rect.x = 675


class Ball(pygame.sprite.Sprite):

    def __init__(self, w, h):
        super().__init__()

        self.image = pygame.Surface([w, h])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.ellipse(self.image, WHITE, [0, 0, w, h])

        self.vX = randint(5, 10)
        self.vY = randint(-10, 10)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.vX
        self.rect.y += self.vY

    def bounceside(self):
        self.vX = -self.vX

    def bouncetopbottom(self):
        self.vY = -self.vY


pygame.init()

window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


pygame.display.set_caption('Pong')

collisionSound = pygame.mixer.Sound('collision.wav')
victoryMatch = pygame.mixer.Sound('victory_match.wav')
victoryGame = pygame.mixer.Sound('victory_game.wav')
defeatGame = pygame.mixer.Sound('defeat_game.wav')
defeatMatch = pygame.mixer.Sound('defeat_match.wav')

font = pygame.font.Font(None, 20)

playerPaddleRight = SidePaddle(2, 75)
computerPaddleLeft = SidePaddle(2, 75)
playerPaddleTop = TopBottomPaddle(75, 2)
playerPaddleBottom = TopBottomPaddle(75, 2)
computerPaddleTop = TopBottomPaddle(75, 2)
computerPaddleBottom = TopBottomPaddle(75, 2)


playerPaddleRight.rect.x = WINDOWWIDTH - 2 - 15
playerPaddleRight.rect.y = (WINDOWHEIGHT - 75) / 2

computerPaddleLeft.rect.x = 15
computerPaddleLeft.rect.y = (WINDOWHEIGHT - 75) / 2

playerPaddleTop.rect.x = (WINDOWWIDTH - 37) / 4 * 3
playerPaddleTop.rect.y = 15
playerPaddleBottom.rect.x = (WINDOWWIDTH - 37) / 4 * 3
playerPaddleBottom.rect.y = WINDOWHEIGHT - 2 - 15

computerPaddleTop.rect.x = (WINDOWWIDTH - 74) / 4
computerPaddleTop.rect.y = 15
computerPaddleBottom.rect.x = (WINDOWWIDTH - 74) / 4
computerPaddleBottom.rect.y = WINDOWHEIGHT - 2 - 15

ball = Ball(10, 10)
ball.rect.x = (WINDOWWIDTH - 10) / 2
ball.rect.y = (WINDOWHEIGHT - 10) / 2

spriteList = pygame.sprite.Group()

spriteList.add(ball)

spriteList.add(playerPaddleRight)
spriteList.add(playerPaddleTop)
spriteList.add(playerPaddleBottom)

spriteList.add(computerPaddleLeft)
spriteList.add(computerPaddleTop)
spriteList.add(computerPaddleBottom)

playerScore = 0
playerWins = 0

cpuScore = 0
cpuWins = 0

clock = pygame.time.Clock()

endGame = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if endGame:
        text = font.render("Play Again? Y/N", 1, (200, 200, 200))
        window.blit(text, ((WINDOWWIDTH / 2) - 40, (WINDOWHEIGHT / 2) + 50))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_y]:
            playerScore = 0
            cpuScore = 0
            playerWins = 0
            cpuWins = 0
            endGame = False

    else:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            playerPaddleTop.left(5)
            playerPaddleBottom.left(5)
        if keys[pygame.K_RIGHT]:
            playerPaddleTop.right(5)
            playerPaddleBottom.right(5)
        if keys[pygame.K_UP]:
            playerPaddleRight.up(5)
        if keys[pygame.K_DOWN]:
            playerPaddleRight.down(5)

        if ball.rect.x > (WINDOWWIDTH - 10) / 2:
            if computerPaddleTop.rect.x > (WINDOWWIDTH - 74) / 4:
                computerPaddleTop.rect.x -= min(5, int(computerPaddleTop.rect.x - ((WINDOWWIDTH - 74) / 4)))
                computerPaddleBottom.rect.x = computerPaddleTop.rect.x
            elif computerPaddleTop.rect.x < (WINDOWWIDTH - 74) / 4:
                computerPaddleTop.rect.x += min(5, int(((WINDOWWIDTH - 74) / 4) - computerPaddleTop.rect.x))
                computerPaddleBottom.rect.x = computerPaddleTop.rect.x

            if computerPaddleLeft.rect.y > (WINDOWHEIGHT - 75) / 2:
                computerPaddleLeft.rect.y -= min(5, int(computerPaddleLeft.rect.y - ((WINDOWHEIGHT - 75) / 2)))
            elif computerPaddleLeft.rect.y < (WINDOWHEIGHT - 75) / 2:
                computerPaddleLeft.rect.y += min(5, int(((WINDOWHEIGHT - 75) / 2) - computerPaddleLeft.rect.y))
        else:
            if computerPaddleTop.rect.x + 37 > ball.rect.x + 5:
                computerPaddleTop.rect.x -= min(5, int((computerPaddleTop.rect.x + 37) - (ball.rect.x + 5)))
                computerPaddleBottom.rect.x = computerPaddleTop.rect.x
            elif computerPaddleTop.rect.x + 37 < ball.rect.x + 5:
                computerPaddleTop.rect.x += min(5, int((ball.rect.x + 5) - (computerPaddleTop.rect.x + 37)))
                computerPaddleBottom.rect.x = computerPaddleTop.rect.x

            if computerPaddleLeft.rect.y + 37 > ball.rect.y + 5:
                computerPaddleLeft.rect.y -= min(5, int((computerPaddleLeft.rect.y + 37) - (ball.rect.y + 5)))
            elif computerPaddleLeft.rect.y + 37 < ball.rect.y + 5:
                computerPaddleLeft.rect.y += min(5, int((ball.rect.y + 5) - (computerPaddleLeft.rect.y + 37)))

        spriteList.update()

        if ball.rect.x < 0:
            playerScore = playerScore + 1
            # reset game
            ball.rect.x = (WINDOWWIDTH - 10) / 2
            ball.rect.y = (WINDOWHEIGHT - 10) / 2
            ball.vX = randint(5, 10)
            ball.vY = randint(-10, 10)
        if ball.rect.x > WINDOWWIDTH:
            cpuScore = cpuScore + 1
            ball.rect.x = (WINDOWWIDTH - 10) / 2
            ball.rect.y = (WINDOWHEIGHT - 10) / 2
            ball.vX = randint(5, 10)
            ball.vY = randint(-10, 10)
        if ball.rect.y < 0:
            if ball.rect.x < (WINDOWWIDTH - 10) / 2:
                playerScore = playerScore + 1
                ball.rect.x = (WINDOWWIDTH - 10) / 2
                ball.rect.y = (WINDOWHEIGHT - 10) / 2
                ball.vX = randint(5, 10)
                ball.vY = randint(-10, 10)
            else:
                cpuScore = cpuScore + 1
                ball.rect.x = (WINDOWWIDTH - 10) / 2
                ball.rect.y = (WINDOWHEIGHT - 10) / 2
                ball.vX = randint(5, 10)
                ball.vY = randint(-10, 10)
        if ball.rect.y > WINDOWHEIGHT:
            if ball.rect.x < (WINDOWWIDTH - 10) / 2:
                playerScore = playerScore + 1
                ball.rect.x = (WINDOWWIDTH - 10) / 2
                ball.rect.y = (WINDOWHEIGHT - 10) / 2
                ball.vX = randint(5, 10)
                ball.vY = randint(-10, 10)
            else:
                cpuScore = cpuScore + 1
                ball.rect.x = (WINDOWWIDTH - 10) / 2
                ball.rect.y = (WINDOWHEIGHT - 10) / 2
                ball.vX = randint(5, 10)
                ball.vY = randint(-10, 10)

        if pygame.sprite.collide_mask(ball, playerPaddleRight) or pygame.sprite.collide_mask(ball, computerPaddleLeft):
            ball.bounceside()
            collisionSound.play()

        if pygame.sprite.collide_mask(ball, playerPaddleTop) or pygame.sprite.collide_mask(ball, playerPaddleBottom):
            ball.bouncetopbottom()
            collisionSound.play()

        if (pygame.sprite.collide_mask(ball, computerPaddleTop) or
                pygame.sprite.collide_mask(ball, computerPaddleBottom)):
            ball.bouncetopbottom()
            collisionSound.play()

        if abs(playerScore - cpuScore) >= 2 and max(playerScore, cpuScore) >= 11:
            if playerScore > cpuScore:
                playerWins = playerWins + 1
                playerScore = 0
                cpuScore = 0
                if playerWins < 3:
                    victoryGame.play()
            else:
                cpuWins = cpuWins + 1
                playerScore = 0
                cpuScore = 0
                if cpuWins < 3:
                    defeatGame.play()

        window.fill(BLACK)

        for i in range(1, 25):
            pygame.draw.line(window, WHITE, ((WINDOWWIDTH / 2), WINDOWHEIGHT / 25 * i),
                             ((WINDOWWIDTH / 2), (WINDOWHEIGHT / 25 * i) + 15), 2)

        spriteList.draw(window)

        requiredScoreText = "11 Points to Win a Game"
        text = font.render(requiredScoreText, 1, WHITE)
        window.blit(text, ((WINDOWWIDTH / 2) - 70, 0))

        cpuScoreText = "Computer Game:" + str(cpuScore) + " Match:" + str(cpuWins)
        text = font.render(cpuScoreText, 1, WHITE)
        window.blit(text, (0, 0))

        playerScoreText = "Player Game:" + str(playerScore) + " Match:" + str(playerWins)
        text = font.render(playerScoreText, 1, WHITE)
        window.blit(text, (WINDOWWIDTH - 200, 0))

        if playerWins >= 3:
            text = font.render("Player Wins", 1, (200, 200, 200))
            window.blit(text, ((WINDOWWIDTH / 2) - 40, WINDOWHEIGHT / 2))
            endGame = True
            victoryMatch.play()
            playerWins = 0
            cpuWins = 0
        elif cpuWins >= 3:
            text = font.render("Computer Wins", 1, (200, 200, 200))
            window.blit(text, ((WINDOWWIDTH / 2) - 62, WINDOWHEIGHT / 2))
            endGame = True
            defeatMatch.play()
            playerWins = 0
            cpuWins = 0

    pygame.display.flip()
    clock.tick(30)
