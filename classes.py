from vars import *
# from pygame import display

import math
import random



class Ball():
	def __init__(self, 
		x: float = 0.0, 
		y: float = 0.0, 
		vx: float = 0.0, 
		vy: float = 0.0
		):

		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy

		self.initial_x = x
		self.initial_y = y
		self.initial_vx = vx
		self.initial_vy = vy

#—————————————————————————————————————————————————————————————————————————————————————————————————

		
	def update_position(self, 
		current_timescale: float = timescale, 
		current_framerate: float = framerate,
		paddles: list = []
		):


		if current_framerate == 0:
			current_framerate = framerate
		time = current_timescale / current_framerate
		accelerationX = 0
		accelerationY = 0

		next_x = self.x + self.vx * time + (accelerationX * (time ** 2)) / 2
		next_y = self.y + self.vy * time + (accelerationY * (time ** 2)) / 2

		# BOUNDARY COLLISION
		if next_y - ball_radius < boundary_upper:
			self.vy = -self.vy
			next_y = boundary_upper + ball_radius
		elif self.y + ball_radius > screen_height - boundary_lower:
			self.vy = -self.vy
			next_y = screen_height - boundary_lower - ball_radius
		self.y = next_y

		# PADDLE COLLISION, should rebound like Pong and Breakout instead of perfectly bouncing
		if next_y + ball_radius > paddles[0].y and next_y - ball_radius < paddles[0].y + paddle_height:
			if next_x - ball_radius < goal_width:
				next_x = goal_width + ball_radius
				self.vx *= -velocity_increment
				self.vy *= velocity_increment
		if next_y + ball_radius > paddles[1].y and next_y - ball_radius < paddles[1].y + paddle_height:
			if next_x + ball_radius > screen_width - goal_width:
				next_x = screen_width - goal_width - ball_radius
				self.vx *= -velocity_increment
				self.vy *= velocity_increment

		self.x = next_x

	

#—————————————————————————————————————————————————————————————————————————————————————————————————


	def reset(self):
		self.x = self.initial_x		
		self.y = self.initial_y
		self.vx = self.initial_vx
		self.vy = self.initial_vy

#—————————————————————————————————————————————————————————————————————————————————————————————————
#—————————————————————————————————————————————————————————————————————————————————————————————————


class Paddle():
	def __init__(self, 
		controller: str = 'Player',
		x: float = 0.0, 
		y: float = 0.0,
		score: int = 0
		):

		self.controller = controller
		self.x = x
		self.y = y
		self.score = score

		self.initial_x = x
		self.initial_y = y

#—————————————————————————————————————————————————————————————————————————————————————————————————


	def update_position(self, 
		increment: float = 0.0
		):
		paddle_bottom = self.y + paddle_height

		if self.y + increment < boundary_upper:
			self.y = boundary_upper
		elif paddle_bottom + increment > screen_height - boundary_lower:
			self.y = screen_height - boundary_lower - paddle_height
		else:
			self.y += increment

#—————————————————————————————————————————————————————————————————————————————————————————————————


	def reset(self):
		self.x = self.initial_x
		self.y = self.initial_y
		self.score = 0