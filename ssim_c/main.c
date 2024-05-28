//#include <SDL2/SDL.h>
#include <stdlib.h>
#include <time.h>

#define SCREEN_WIDTH 1366
#define SCREEN_HEIGHT 768

typedef struct {
    int x, y;
} Position;

typedef struct 
{
    int amount;
    int size;
    //SDL_Color color;
    int perception_radius[2];
} BirdOptions;

typedef struct {
    int radius;
    //SDL_Color color;
    Position *positions;
    int num_positions;
} ObstacleOptions;

typedef struct {
    //SDL_Window *window;
    //SDL_Renderer *renderer;
    //SDL_bool running;
    //SDL_Event event;
    BirdOptions bird_options;
    ObstacleOptions obstacle_options;
} Environment;

//region
void init_env(Environment *env) {
    //env->window = SDL_CreateWindow("Bird Simulation", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SCREEN_WIDTH, SCREEN_HEIGHT, 0);
    //env->renderer = SDL_CreateRenderer(env->window, -1, SDL_RENDERER_ACCELERATED);
    //env->running = SDL_TRUE;

    // Initializing bird options
    env -> bird_options.amount = 2;
    env -> bird_options.size = 5;
    //env -> bird_options.color = (SDL_Color)(255, 0, 0, 255);
    env -> bird_options.perception_radius[0] = 25;
    env -> bird_options.perception_radius[1] = 75;

    // Initializing obstacle options
    env -> obstacle_options.radius = 50;
    //env -> obstacle_options.color = (SDL_Color)(0, 255, 0, 255);
    env -> obstacle_options.num_positions = 10;
    env -> obstacle_options.positions = malloc(env -> obstacle_options.num_positions * sizeof(Position));

    for (int i = 0; i < env -> obstacle_options.num_positions; i++) {
        env -> obstacle_options.positions[i].x = rand() % SCREEN_WIDTH;
        env -> obstacle_options.positions[i].y = rand() % SCREEN_HEIGHT;
    }
}

void env_cleanup(Environment *env) {
    free(env -> obstacle_options.positions);
    //SDL_DestroyRenderer(env->renderer);
    //SDL_DestroyWindow(env->window);
    //SDL_Quit();
}

/*
void handle_events(Environment *env) {
    while (SDL_PollEvent(&env -> event)) {
        if (env -> event.type == SDL_QUIT) {
            env -> running = SDL_FALSE;
        } 
    }
}

void draw_obstacles(Environment *env) {
    SDL_SetRenderDrawColor(env->renderer, env->obstacle_options.color.r, env->obstacle_options.color.g, env->obstacle_options.color.b, env->obstacle_options.color.a);
    for (int i = 0; i < env -> obstacle_options.num_positions; i++) {
        SDL_Rect obstacle_rect = { env->obstacle_options.positions[i].x - env->obstacle_options.radius,
                                   env->obstacle_options.positions[i].y - env->obstacle_options.radius,
                                   env->obstacle_options.radius * 2,
                                   env->obstacle_options.radius * 2 };

        SDL_RenderFillRect(env->renderer, &obstacle_rect);
    }
}

void draw_birds(Environment *env) {
    SDL_SetRenderDrawColor(env->renderer, env->bird_options.color.r, env->bird_options.color.g, env->bird_options.color.b, env->bird_options.color.a);
    
    // Placeholder for bird drawing logic
    for (int i = 0; i < env->bird_options.amount; i++) {
        SDL_Rect bird_rect = { 100 + i * 20, 100, env->bird_options.size, env->bird_options.size };
        SDL_RenderFillRect(env->renderer, &bird_rect);
    }
}
*/
int main(int argc, char *argv[]) {
    // SDL_Init(SDL_INIT_VIDEO);
    srand(time(NULL));

    Environment env;
    init_env(&env);
    /*
    while (env.running) {
        handle_events(&env);

        SDL_SetRenderDrawColor(env.renderer, 0, 0, 0, 255);
        SDL_RenderClear(env.renderer);

        draw_obstacles(&env);
        draw_birds(&env);

        SDL_RenderPresent(env.renderer);
        SDL_Delay(1000 / 60); // Cap at 60 FPS
    }
    */

   env_cleanup(&env);
    return 0;  
}
