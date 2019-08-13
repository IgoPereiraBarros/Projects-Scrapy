# <><><> Movimentos do robo será 0 < x, y < 10

import random


class Point(object):

    """
        Determina a coordenação do robo
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Posição atual: [{}, {}]'.format(self.x, self.y)

class Reward(Point):

    """
        Determina a recompensa do robo
    """

    def __init__(self, x, y, name):
        super(Reward, self).__init__(x, y)
        self.name = name
    
    def __str__(self):
        return '[{}, {}: {}]'.format(self.x, 
                                     self.y, 
                                     self.name)
    
    def __repr__(self):
        return 'Reward {}'.format(str(self))


class Robot(Point):

    """
        Movimenta o robo
    """

    def move_up(self):
        if self.y < 10:
            self.y += 1
        else:
            print('Movimento proibido')
    
    def move_down(self):
        if self.y > 0:
            self.y -= 1
        else:
            print('Movimento proibido')
    
    def move_left(self):
        if self.x > 0:
            self.x -= 1
        else:
            print('Movimento proibido')
    
    def move_right(self):
        if self.x < 10:
            self.x += 1
        else:
            print('Movimento proibido')



def check_reward(robot, rewards):
    """
        Verifica a posição do robo, para ver se houve recompensa
    """
    is_reward = False
    for reward in rewards:
        if reward.x == robot.x and reward.y == robot.y:
            print('Recompensa: %s' % reward.name)
            is_reward = True
    return is_reward

def generate_number_random():
    """
        Gera números aleatórios inteiros entre 0 e 10
    """
    return random.randint(0, 10)

if __name__ == '__main__':
    robot = Robot(generate_number_random(),
                  generate_number_random())
    
    rewards = [
        Reward(generate_number_random(),
               generate_number_random(), 
               'bitcoin'),
        Reward(generate_number_random(),
                generate_number_random(), 
                'Euro'),
        Reward(generate_number_random(),
               generate_number_random(), 
               'Dolar')
    ]
    print(rewards)
    print('### Possíveis posições: up, down, left, right ###\n')

    for i in range(10):
        moviment = input('>: ').lower()

        if moviment == 'up':
            robot.move_up()
        elif moviment == 'down':
            robot.move_down()
        elif moviment == 'right':
            robot.move_right()
        elif moviment == 'left':
            robot.move_left()
        else:
            print('INFO: Movimente seu robô apenas com <up, down, left, right>')
            continue
        print(robot)
        check_reward(robot, rewards)


