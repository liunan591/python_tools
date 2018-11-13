import pygame
#1.初始化
pygame.init()
#2.创建游戏的窗口 480 * 700
screen = pygame.display.set_mode((480, 700))
#3.创建时钟对象
clock = pygame.time.Clock()
#4.游戏内容，可以在之前创建精灵和精灵族
while True:
	#指定刷新帧率，只有在循环中指定有效
	clock.tick(1)
	#更新/绘制精灵组
	#事件监听/碰撞检测
	#可以在所有绘制工作完成之后，统一调用update方法
	pygame.display.update()
#5.结束游戏
pygame.quit()

#%%功能代码
#1.绘制图像
	# 1> 加载图像数据
	bg = pygame.image.load("./images/background.png")
	# 2> blit 绘制图像
	screen.blit(bg, (0, 0))	#0，0分别表示距离左上角水平和垂直方向的像素
	# 3> update 更新屏幕显示
	pygame.display.update()
#2.创建游戏精灵
	pygame.sprite.Sprite:
		image图像数据，rect屏幕位置，update更新位置方法，kill从所有组中删除
	pygame.sprite.Group：用多个精灵做初始化
		update调用所有精灵的update方法，draw(screen)绘制所有精灵的image，pygame.display.update()更新画面，不可省略
#3.定时器的功能pygame.time.set_timer(HERO_FIRE_EVENT, 500)
	HERO_FIRE_EVENT表示常量定义的事件类型，500表示500ms间隔产生一次事件
#4.获取按键元组pygame.key.get_pressed()，若某个键被按下，则对应数值为1
	可以产生连续按键效果
#5.碰撞检测pygame.sprite.groupcollide，判断两个精灵组间是否有碰撞
	pygame.sprite.spritecollide,判断某个精灵与精灵组间是否有碰撞 