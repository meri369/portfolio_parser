import arcade
import random

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Работа со звуками"


class Penguin(arcade.AnimatedTimeBasedSprite):
    def __init__(self):
        super().__init__(scale=1)
        self.texture = arcade.load_texture('resources/penguin2.png')
        self.textures.append(arcade.load_texture("resources/penguin1.png"))
        self.textures.append(arcade.load_texture("resources/penguin2.png"))
        self.textures.append(arcade.load_texture("resources/penguin3.png"))
        self.cur_texture = 0

    def update(self):
        self.center_y += self.change_y
        self.angle += self.change_angle
        self.change_y -= 0.4
        if self.center_y < 0:
            self.center_y = 0
        if self.center_y > SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT

        self.change_angle -= 0.4
        if self.angle >= 40:
            self.angle = 40
        if self.angle <= -30:
            self.angle = -30

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture >= len(self.textures) * 5:
            self.cur_texture = 0
        frame = self.cur_texture // 5
        self.texture = self.textures[frame]
        print(self.cur_texture)


class ColumnTop(arcade.Sprite):
    def update(self):
        self.center_x -= self.change_x
        if self.center_x <= 0:
            self.center_x = SCREEN_WIDTH
            self.center_y = random.randint(390, 480)


class ColumnBottom(arcade.Sprite):
    def update(self):
        self.center_x -= self.change_x
        if self.center_x <= 0:
            self.center_x = SCREEN_WIDTH
            self.center_y = random.randint(0, 70)


class OurGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = arcade.load_texture("resources/space.png")
        self.player = None
        self.columns_list = None

        self.stop = False
        self.sound_lose = None
        self.sound = None
        self.music = None
        self.sound_wing = None

    def setup(self):
        self.player = Penguin()
        self.player.center_x = 100
        self.player.center_y = 180
        self.player.change_y = 0
        self.player.change_angle = 0

        self.columns_list = arcade.SpriteList()
        for i in range(5):
            column_top = ColumnTop("resources/column_top.png", 1)
            column_top.center_x = 130 * i + SCREEN_WIDTH
            column_top.center_y = 400
            column_top.change_x = 1
            self.columns_list.append(column_top)

            column_bottom = ColumnBottom("resources/column_bottom.png", 1)
            column_bottom.center_x = 130 * i + SCREEN_WIDTH
            column_bottom.center_y = 400
            column_bottom.change_x = 1
            self.columns_list.append(column_bottom)

        self.sound_lose = arcade.load_sound('resources/lose.wav')
        self.sound = arcade.load_sound('resources/music.mp3')
        self.music = arcade.play_sound(self.sound, volume=0.01, looping=True)
        self.sound_wing = arcade.load_sound('resources/sfx_wing.ogg')

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player.draw()
        self.columns_list.draw()

    def on_update(self, delta_time):
        if not self.stop:
            self.player.update()
            self.player.update_animation()
            self.columns_list.update()
            hit_list = arcade.check_for_collision_with_list(self.player, self.columns_list)
            if len(hit_list) > 0:
                self.player.stop()
                for column in self.columns_list:
                    column.stop()
                arcade.stop_sound(self.music)
                arcade.play_sound(self.sound_lose)
                self.stop = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.stop is False:
            self.player.change_y = 3
            self.player.change_angle = 5
            arcade.play_sound(self.sound_wing)

    def on_key_release(self, key, modifiers):
        pass


game = OurGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
game.setup()
arcade.run()
