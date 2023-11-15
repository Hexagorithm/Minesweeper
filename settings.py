screen_size = 800, 850

curr_dir = '' # sciezka powinna zaczynac sie od /home i konczyc sie \ '

if curr_dir == '':
    raise Exception('Prosze w pliku settings.py przypisac zmiennej \'curr_dir\' absolutna sciezka do foldera \'Minesweeper\'')

bomb_amount = 99
tile_amount = 25
icon =                  curr_dir + 'textures/bomb/bomb.png'
play_again_button_path =curr_dir + 'textures/button/play_again_button.png'
bomb_path =                     curr_dir + 'textures/bomb/bomb.png'
flag_path =                     curr_dir + 'textures/flag/flag.png'
pause_path =                    curr_dir + 'textures/pause/pause.png'
opened_tile_dark =                  curr_dir + 'textures/tiles/opened_tile1.png'
opened_tile_light =                     curr_dir + 'textures/tiles/opened_tile2.png'
unopened_tile_dark =                    curr_dir + 'textures/tiles/unopened_tile1.png'
unopened_tile_light =                   curr_dir + 'textures/tiles/unopened_tile2.png'
lmao1_path =                    curr_dir + 'textures/loss/Lmao1.png'
lmao2_path =                    curr_dir + 'textures/loss/lmao2.png'
lmao3_path =                    curr_dir + 'textures/loss/lmao3.png'
gj1_path =                  curr_dir + 'textures/win/good_job1.png'
gj2_path =                  curr_dir + 'textures/win/good_job2.png'
gj3_path =                  curr_dir + 'textures/win/good_job3.png'
font_name = None
font_color = {'B':    (0,0,0),
              '1':    (25,118,210),
              '2':    (64, 144, 64),
              '3':    (212, 83, 75),
              '4':    (134, 8, 0),
              '5':    (245, 136, 0),
              '6':    (5, 0, 175),
              '7':    (89, 255, 99),
              '8':    (255, 255, 255),
              'ending': (0,0,0),
              'flags': (255,255,255),
              'message':(255,255,255)}
tile_multiplier = (screen_size[0]) // tile_amount
menu_bar_size = tile_multiplier
