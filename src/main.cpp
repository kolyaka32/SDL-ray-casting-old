#include <SDL2/SDL.h>
#include <cmath>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>

#define WIDTH 800
#define HEIGHT 600
#define FOVd 60  // Field of view in degrees

#define FOVr FOVd*3.14/180  // Field of view in radians

// Path to file
std::string path;

// Lists of drawing objects
int lenPoint; // Number of points in array
int *points;  // List of points of walls
int lenWalls; // Number of walls in array
int *walls;  // List of wall with points

// Rect-type to create floor
const SDL_Rect FLOOR_RECT = {0, HEIGHT/2, WIDTH, HEIGHT/2};

// Pointers
SDL_Renderer *renderer = NULL;      // Pointer for the renderer
SDL_Window *window = NULL;      // Pointer for the window

// Variables
float minR;  // R to closiest wall

// Class of player
class Player{
    public:
    // Initialising of player
    Player(){
        //
        x = 150; y = 150;
        ang = 0;
        dx = 0; dy = 0;
        boost = 1;
    }

    float x, y; // Coordinats of player
    float ang; // Angular of rotating od player
    int dx, dy; // Delta movements of player
    int boost; // Speed multipliyer
};

// Functions
// Function of initialasing of SDL and other libraries
void SDL_init(){
    if( SDL_Init(SDL_INIT_VIDEO) != 0)  // Initializing SDL as Video
    {std::cout << "SDL_INIT_VIDEO_ERROR" << SDL_Error; }  // Init 
           
    SDL_CreateWindowAndRenderer(WIDTH, HEIGHT, 0, &window, &renderer);
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);      // setting draw color
    SDL_RenderClear(renderer);      // Clear the newly created window
    SDL_RenderPresent(renderer);    // Reflects the changes done in the
                                        //  window
    SDL_SetWindowTitle(window, "Unperspective on SDL");
    SDL_ShowCursor(SDL_DISABLE);  // Unshow cusoir on screen
};

// Function of deinitialising of SDL
void SDL_del(){
    SDL_ShowCursor(SDL_ENABLE);  // Unshow cusoir on screen
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    // Deliting all dinamicle arrays
    delete points;
    delete walls;
};

// Function of reading map from file
void ReadMap(std::string name){

    std::string line;  // Outputing string format
    
    std::ifstream in(name); // Open file to read
    getline(in, line);  // Getting first line to number of points and walls
    
    lenPoint = std::stoi( line.substr(0, line.find(';')+1) );
    lenWalls = std::stoi( line.substr(line.find(';')+1, line.length()) );

    points = new int[lenPoint*2];
    walls = new int[lenWalls*2];

    for(int i = 0; i < lenPoint; ++i){
        getline(in, line);
        points[i*2] = std::stoi( line.substr(0, line.find(';')+1) );
        points[i*2+1] = std::stoi( line.substr(line.find(';')+1, line.length()) );
    }
    for(int i = 0; i < lenWalls; ++i){
        getline(in, line);
        walls[i*2] = std::stoi( line.substr(0, line.find(';')+1) );
        walls[i*2+1] = std::stoi( line.substr(line.find(';')+1, line.length()) );
    }
    
    in.close();  // Closing file
}

// Function of finding distans to wall or 0, if that isn't possible
int WallCross(int Ax, int Ay, int Bx, int By, int Cx, int Cy, int Dx, int Dy){
    int den = ( (Dx-Cx)*(By-Ay) - (Bx-Ax)*(Dy-Cy) );

    if(den == 0) return 0;
    float r = (float)((Bx - Ax) * (Cy - Ay) - (Cx - Ax) * (By - Ay)) / den;
    if(r<0) return 0;
    if(r>minR) return 0;
    float  s = (float)((Ax - Cx) * (Dy - Cy) - (Dx - Cx) * (Ay - Cy)) / den;
    if(s<0 || s>1) return 0;
    minR = r;
    return (WIDTH * 10 / sqrt(  pow(Cx - (s * (Bx - Ax) + Ax), 2) + pow(Cy - (s * (By - Ay) + Ay), 2) ) ); // Outputing distans to C
};

// Function of drawing wall at screen
void WallDraw(int x, int h){
    int y = (HEIGHT-h)/2;  // Position of vertical column coordinate
    // Drawing 2 pixels of black on top and bottom

    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);  // Setting color of black
    SDL_RenderDrawPoint(renderer, x, y);
    SDL_RenderDrawPoint(renderer, x, HEIGHT-y);

    SDL_SetRenderDrawColor(renderer, 10, 10, h * 256 / HEIGHT, 20);  // Setting color depens on height
    SDL_RenderDrawLine(renderer, x, y+1, x, (HEIGHT-y-1));
    
};

// Drawing map at screen
void MapDraw(int Headx, int Heady){
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);  // Setting color of map
    for(int i=0; i < lenWalls; ++i){
        SDL_RenderDrawLine(renderer, points[walls[i*2]*2], points[walls[i*2]*2+1], points[walls[i*2+1]*2], points[walls[i*2+1]*2+1]);
    }
    SDL_SetRenderDrawColor(renderer, 0, 255, 0, 0);  // Setting color of player
    SDL_RenderDrawPoint(renderer, Headx, Heady);  // Draw point at player center
}

// Main function
int main(int argc, char * argv[]){
    // Creating path to executable file
    std::string place = argv[0];  // Getting path to file
    path = place.substr(0, place.find_last_of('\\')+1);

    // Creating class objects
    Player Head; // Creating of new character - Head

    SDL_init(); // Initialising of libraries
    ReadMap(path + "walls1.txt");  // Reading map from file

    //SDL_SetWindowMouseGrab(window, SDL_TRUE);
    SDL_Event event;    // Event variable
    while(!(event.type == SDL_QUIT)){
        // New try cycle
        SDL_Delay(20);  // setting some Delay
        
        // Catching the poll event.
        while(SDL_PollEvent(&event) != 0) {
            if(event.type == SDL_QUIT) return 0;
            if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_w) {
                    Head.dy = -1;
                }
                if (event.key.keysym.sym == SDLK_s) {
                     Head.dy = 1;
                }
                if (event.key.keysym.sym == SDLK_d) {
                     Head.dx = 1;
                }
                if (event.key.keysym.sym == SDLK_a) {
                     Head.dx = -1;
                }
                if (event.key.keysym.sym == SDLK_LSHIFT){
                    Head.boost = 2;
                }
                if (event.key.keysym.sym == SDLK_1){
                    delete points; delete walls;  // Deliting old arrays
                    ReadMap(path + "walls1.txt");  // Reading new map
                }
                if (event.key.keysym.sym == SDLK_2){
                    delete points; delete walls;  // Deliting old arrays
                    ReadMap(path + "walls2.txt");  // Reading new map
                }
            }
            if (event.type == SDL_KEYUP) {
                if (event.key.keysym.sym == SDLK_w || event.key.keysym.sym == SDLK_s) {
                    Head.dy = 0;
                }
                if (event.key.keysym.sym == SDLK_d || event.key.keysym.sym == SDLK_a) {
                    Head.dx = 0;
                }
                if (event.key.keysym.sym == SDLK_LSHIFT){
                    Head.boost = 1;
                }
            }
        }
        // Get mouse position on the screen
        int MouseX, MouseY;
        SDL_GetMouseState(&MouseX, &MouseY);
        Head.ang += (float)(MouseX - WIDTH/2 ) / 200;
        SDL_WarpMouseInWindow(window, WIDTH/2, HEIGHT/2);

        // Movement of player
        Head.x += (-Head.dx * sin(Head.ang) - Head.dy * cos(Head.ang)) * Head.boost;
        Head.y += ( Head.dx * cos(Head.ang) - Head.dy * sin(Head.ang)) * Head.boost;

        // Renderer
        SDL_SetRenderDrawColor(renderer, 77, 143, 172, 0);  // Filling of sky
        SDL_RenderClear(renderer);
        SDL_SetRenderDrawColor(renderer, 127, 127, 127, 0);  // Filling of floor
        SDL_RenderFillRect(renderer, &FLOOR_RECT);

        // Cycle of drawing each column to create picture of graphics
        for(int x = 0; x<WIDTH; ++x){
            minR = 1000;  // Reseting of R
            float ang = Head.ang + (x*FOVr/WIDTH) - FOVr/2;
            int mDis = 0;  // Resseting of min distance
            // Calculating D-point
            int HeadX = Head.x+500*cos(ang);
            int HeadY = Head.y+500*sin(ang);
            // Finding closiest wall coordinat
            for(int i=0; i < lenWalls; i++){
                int d = WallCross(points[walls[i*2]*2], points[walls[i*2]*2+1], points[walls[i*2+1]*2], points[walls[i*2+1]*2+1], 
                Head.x, Head.y, HeadX, HeadY);
                if(d > mDis) mDis = d;
            }
            if(mDis >= HEIGHT-2) mDis = HEIGHT-2;  // Settig max h to WIDTH
            WallDraw(x, mDis); // Drawing closiest wall at screen
        }

        MapDraw(Head.x, Head.y);  // Drawing map

        SDL_RenderPresent(renderer);  // Show the change on the screen
    }
    SDL_del(); // Clear all data
    return 1;
}