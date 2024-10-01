#include <SDL.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

// Window options
#define WINDOW_WIDTH 800
#define WINDOW_HEIGHT 600

// Bird movement
#define SHIFT_VEC_LEN 10
#define SHIFT_VEC_MODIFIER 50.0f - 1
#define MAX_SPEED 0.1f

// Global bird options
#define BIRD_AMOUNT 50
#define BIRD_SIZE 10
#define BIRD_COLOR {255, 0, 0}
#define BIRD_PERCEPTION_RADIUS {50, 50}

// Global obstacle options
#define OBSTACLE_AMOUNT 10
#define OBSTACLE_SIZE 25
#define OBSTACLE_COLOR {0, 255, 0}

// Flocking
#define COHESION_FACTOR 0.01f
#define SEPARATION_FACTOR 0.01f
#define ALIGNMENT_FACTOR 0.01f
#define SEPARATION_DISTANCE 5

typedef struct {
   int32_t amount;
   int32_t size;
   uint8_t color[3];
} BirdOptions;

typedef struct {
   float pos_x;
   float pos_y;
   float dx;
   float dy;
   int32_t size;
   int perception_radius_flock;
   int perception_radius_obstacle;
} Bird;

typedef struct {
   int32_t amount;
   int32_t size;
   uint8_t color[3];
} ObstacleOptions;

typedef struct {
   float pos_x;
   float pos_y;
   float size;
} Obstacle;

void cohesion(
   Bird *bird, 
   Bird *flock, 
   int bird_count,
   float *avg_pos_x,
   float *avg_pos_y
   ) {
      int count = 0;
      *avg_pos_x = 0;
      *avg_pos_y = 0;

      for (int i = 0; i < bird_count; i++) {
         float dx = flock[i].pos_x - bird->pos_x;
         float dy = flock[i].pos_y - bird->pos_y;
         float distance_squared = dx * dx + dy * dy;

         if (distance_squared < bird->perception_radius_flock * bird->perception_radius_flock && distance_squared > 0) {
            *avg_pos_x += flock[i].pos_x;
            *avg_pos_y += flock[i].pos_y;
            count++;
        }
      }

      if (count > 0) {
         *avg_pos_x /= count;
         *avg_pos_y /= count;

         bird->dx += (*avg_pos_x - bird->pos_x) * COHESION_FACTOR;
         bird->dy += (*avg_pos_y - bird->pos_y) * COHESION_FACTOR;
      }
   }

void separation(
   Bird *bird, 
   Bird *flock, 
   int bird_count, 
   float *separation_x, 
   float *separation_y
   ) {
      int count = 0;
      *separation_x = 0;
      *separation_y = 0;

      for (int i = 0; i < bird_count; i++) {
         float dx = bird->pos_x - flock[i].pos_x;
         float dy = bird->pos_y - flock[i].pos_y;
         float distance_squared = dx * dx + dy * dy;

         if (distance_squared < SEPARATION_DISTANCE * SEPARATION_DISTANCE && distance_squared > 0) {
            *separation_x += dx;
            *separation_y += dy;
            count++;
         }
      }

      if (count > 0) {
         *separation_x /= count;
         *separation_y /= count;

         bird->dx += *separation_x * SEPARATION_FACTOR;
         bird->dy += *separation_y * SEPARATION_FACTOR;
      }
   }

void alignment(
   Bird *bird, 
   Bird *flock, 
   int bird_count, 
   float *avg_dx, 
   float *avg_dy
   ) {
      int count = 0;
      *avg_dx = 0;
      *avg_dy = 0;

      for (int i = 0; i < bird_count; i++) {
         float dx = flock[i].pos_x - bird->pos_x;
         float dy = flock[i].pos_y - bird->pos_y;
         float distance_squared = dx * dx + dy * dy;

         if (distance_squared < bird->perception_radius_flock * bird->perception_radius_flock && distance_squared > 0) {
            *avg_dx += flock[i].dx;
            *avg_dy += flock[i].dy;
            count++;
         }
      }

      if (count > 0) {
         *avg_dx /= count;
         *avg_dy /= count;

         bird->dx += (*avg_dx - bird->dx) * ALIGNMENT_FACTOR;
         bird->dy += (*avg_dy - bird->dy) * ALIGNMENT_FACTOR;
      }
   }

bool check_collision(Bird *bird, Obstacle *obstacle) {
   float dx = bird->pos_x - obstacle->pos_x;
   float dy = bird->pos_y - obstacle->pos_y;

   float distance_squared = dx * dx + dy * dy;
   float radius_sum = bird->size / 2 + obstacle->size;

   return distance_squared <= radius_sum * radius_sum;
}

void spawn_birds(BirdOptions birdOptions, Bird *birds) {
   for (int i = 0; i < birdOptions.amount; i++) {
      birds[i].pos_x = rand() % WINDOW_WIDTH;
      birds[i].pos_y = rand() % WINDOW_HEIGHT;
      birds[i].dx = ((rand() % SHIFT_VEC_LEN) / SHIFT_VEC_MODIFIER) * MAX_SPEED;
      birds[i].dy = ((rand() % SHIFT_VEC_LEN) / SHIFT_VEC_MODIFIER) * MAX_SPEED;
      birds[i].size = birdOptions.size;
   }
}

void spawn_obstacles(ObstacleOptions obstacleOptions, Obstacle *obstacles) {
   for (int i = 0; i < obstacleOptions.amount; i++) {
         obstacles[i].pos_x = rand() % WINDOW_WIDTH;
         obstacles[i].pos_y = rand() % WINDOW_HEIGHT;
         obstacles[i].size = obstacleOptions.size;
      }
}

void move_birds(Bird *birds, int *bird_count, Obstacle *obstacles, int obstacle_count) {
   for (int i = 0; i < *bird_count; i++) {
      float avg_pos_x = 0, avg_pos_y = 0;
      float separation_x = 0, separation_y = 0;
      float avg_dx = 0, avg_dy = 0;

      cohesion(&birds[i], birds, *bird_count, &avg_pos_x, &avg_pos_y);
      separation(&birds[i], birds, *bird_count, &separation_x, &separation_y);
      alignment(&birds[i], birds, *bird_count, &avg_dx, &avg_dy);

      birds[i].pos_x += birds[i].dx;
      birds[i].pos_y += birds[i].dy;

      if (birds[i].pos_x < 0) birds[i].pos_x = WINDOW_WIDTH;
      if (birds[i].pos_x > WINDOW_WIDTH) birds[i].pos_x = 0;
      if (birds[i].pos_y < 0) birds[i].pos_y = WINDOW_HEIGHT;
      if (birds[i].pos_y > WINDOW_HEIGHT) birds[i].pos_y = 0;

      for (int j = 0; j < obstacle_count; j++) {
         if (check_collision(&birds[i], &obstacles[j])) {
            birds[i].size = 0; 
               break;
         }  
      }
   }  
}

void draw_birds(SDL_Renderer *renderer, Bird *birds, int amount, uint8_t color[3]) {
   SDL_SetRenderDrawColor(renderer, color[0], color[1], color[2], 255);

   for (int i = 0; i < amount; i++) {
      SDL_Rect birdRect = {
         (int) birds[i].pos_x,
         (int) birds[i].pos_y,
         birds[i].size,
         birds[i].size
      };
      SDL_RenderFillRect(renderer, &birdRect);
   }
}

void draw_obstacles(SDL_Renderer *renderer, Obstacle *obstacles, int amount, uint8_t color[3]) {
   SDL_SetRenderDrawColor(renderer, color[0], color[1], color[2], 255);

   for (int i = 0; i < amount; i++) {
      SDL_Rect obstacleRect = {
         (int) obstacles[i].pos_x,
         (int) obstacles[i].pos_y,
         (int) obstacles[i].size,
         (int) obstacles[i].size,
      };
      SDL_RenderFillRect(renderer, &obstacleRect);
   }
}

int main(int argc, char* argv[]) {
   srand(time(NULL));
   
   if (SDL_Init(SDL_INIT_VIDEO) < 0) {
      printf("SDL_Init failed: %s\n", SDL_GetError());
      return 1;
   }

   SDL_Window* window = SDL_CreateWindow(
      "SDL Window",
      SDL_WINDOWPOS_CENTERED,
      SDL_WINDOWPOS_CENTERED,
      800,
      600,
      SDL_WINDOW_SHOWN
   );

   if (window == NULL) {
      printf("Window could not be created: SDL_Error: %s\n", SDL_GetError());
      SDL_Quit();
      return 1;
   }

   SDL_Renderer *renderer = SDL_CreateRenderer(
      window,
      -1,
      SDL_RENDERER_ACCELERATED
   );

   if (renderer == NULL) {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

   BirdOptions birdOptions = {
      .amount = BIRD_AMOUNT,
      .size = BIRD_SIZE,
      .color = BIRD_COLOR,
   };

   Bird *birds = (Bird *)malloc(birdOptions.amount * sizeof(Bird));
   spawn_birds(birdOptions, birds);

   ObstacleOptions obstacleOptions = {
      .amount = OBSTACLE_AMOUNT,
      .size = OBSTACLE_SIZE,
      .color = OBSTACLE_COLOR
   };

   Obstacle *obstacles = (Obstacle *)malloc(obstacleOptions.amount * sizeof(Obstacle));
   spawn_obstacles(obstacleOptions, obstacles);

   int running = 1;
   SDL_Event event;

   while (running) {
      while (SDL_PollEvent(&event)) {
         if (event.type == SDL_QUIT) {
            running = 0;
         }
      }
      int bird_count = birdOptions.amount;
      move_birds(birds, &bird_count, obstacles, obstacleOptions.amount);
      
      SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
      SDL_RenderClear(renderer);

      draw_birds(renderer, birds, birdOptions.amount, birdOptions.color);
      draw_obstacles(renderer, obstacles, obstacleOptions.amount, obstacleOptions.color);

      SDL_RenderPresent(renderer);
   }

   free(birds);
   free(obstacles);
   SDL_DestroyRenderer(renderer);
   SDL_DestroyWindow(window);
   SDL_Quit();

   return 0;
}