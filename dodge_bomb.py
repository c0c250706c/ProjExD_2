import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_RIGHT: (5, 0),
    pg.K_LEFT:(-5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横判定結果、縦判定結果）
    Turu：画面内/False：画面外
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    # 1.黒い矩形を描画するための空のSurface
    go_img = pg.Surface((WIDTH, HEIGHT))
    go_img.fill((0, 0, 0))
    # 2. 1のSurfaceの透明度を設定
    go_img.set_alpha(150)
    # 3. 白文字でGame Overと書かれたフォントSurfaceを作り，1のSurfaceにblit
    ob_f = pg.font.Font(None, 80)
    text_surf = ob_f.render("Game Over", True, (255, 255, 255))
    text_rct = text_surf.get_rect()
    text_rct.center = (WIDTH // 2, HEIGHT // 2)
    go_img.blit(text_surf, text_rct)
    # 4. こうかとん画像をロードし，こうかとんSurfaceを作り，1のSurfaceにblit
    kk_img2 = pg.image.load("fig/8.png") # 泣いているこうかとん（1.pngなど）に変えてもOKです
    kk_rct_l = kk_img2.get_rect()
    kk_rct_r = kk_img2.get_rect()
    kk_rct_l.center = (text_rct.left - 100, HEIGHT // 2)
    kk_rct_r.center = (text_rct.right + 100, HEIGHT // 2)
    go_img.blit(kk_img2, kk_rct_l)
    go_img.blit(kk_img2, kk_rct_r)
    # 5. 1のSurfaceをscreen Surfaceにblit
    screen.blit(go_img, (0, 0))
    # 6. pg.display.update()したら，time.sleep(5)する
    pg.display.update()
    time.sleep(5)

def muki_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    # ベース画像
    base_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
# 左右反転したベース画像
    flip_img = pg.transform.flip(base_img, True, False)
    # 移動量タプル : rotozoomしたSurface の辞書を作成
    kk_imgs = {
        (0, 0):   base_img,                                   #静止時
        (-5, 0):  base_img,                                   # 左
        (-5, -5): pg.transform.rotozoom(base_img, -45, 1.0),  # 左上
        (0, -5):  pg.transform.rotozoom(flip_img, 90, 1.0),   # 上
        (+5, -5): pg.transform.rotozoom(flip_img, 45, 1.0),   # 右上
        (+5, 0):  flip_img,                                   # 右
        (+5, +5): pg.transform.rotozoom(flip_img, -45, 1.0),  # 右下
        (0, +5):  pg.transform.rotozoom(flip_img, -90, 1.0),  # 下
        (-5, +5): pg.transform.rotozoom(base_img, 45, 1.0),   # 左下
    }
    return kk_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    # こうかとんの初期化
    kk_imgs = muki_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の初期化
    clock = pg.time.Clock()
    bb_img = pg.Surface((20, 20))  # 爆弾用の空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0))  
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 横初期座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦初期座標
    vx, vy = +5, +5 

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # こうかとんRectと爆弾Rectが重なったら
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の処理
                sum_mv[1] += mv[1]  # 縦方向の処理

        sum_mv_tuple = tuple(sum_mv)
        if sum_mv_tuple in kk_imgs:
            kk_img = kk_imgs[sum_mv_tuple]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 動きをなかったことにする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出ていたら
            vx *= -1
        if not tate:  # 縦にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
