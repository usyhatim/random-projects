#include <iostream>
#include <cstdlib>
#include <ctime>
#include <conio.h> // For Windows _kbhit() and _getch()

using namespace std;

bool gameover;
const int width = 20;
const int height = 17;
int x, y, fruitX, fruitY, score;
int tailX[100], tailY[100]; // Snake coordinates
int nTail;

enum eDirection { STOP = 0, LEFT, RIGHT, UP, DOWN }; // Controls
eDirection dir;

void Setup() {
    gameover = false;
    dir = STOP;
    x = width / 2;
    y = height / 2;

    srand(time(0)); // Random seed for different fruit positions
    fruitX = rand() % width;
    fruitY = rand() % height;

    score = 0;
    nTail = 0;
}

void Draw() {
    system("cls"); // Clear the console (Windows-specific)

    // Top border
    for (int i = 0; i < width + 2; i++) cout << "#";
    cout << endl;

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (j == 0) cout << "#"; // Left wall

            if (i == y && j == x)
                cout << "*"; // Snake head
            else if (i == fruitY && j == fruitX)
                cout << "%"; // Fruit
            else {
                bool print = false;
                for (int k = 0; k < nTail; k++) {
                    if (tailX[k] == j && tailY[k] == i) {
                        cout << "*"; // Snake tail
                        print = true;
                        break;
                    }
                }
                if (!print) cout << " ";
            }

            if (j == width - 1) cout << "#"; // Right wall
        }
        cout << endl;
    }

    // Bottom border
    for (int i = 0; i < width + 2; i++) cout << "#";
    cout << endl;

    cout << "Score: " << score << endl;
}

void Input() {
    if (_kbhit()) {
        switch (_getch()) {
            case 'a': dir = LEFT; break;
            case 'd': dir = RIGHT; break;
            case 'w': dir = UP; break;
            case 's': dir = DOWN; break;
            case 'x': gameover = true; break;
        }
    }
}

void Algorithm() {
    // Update tail positions
    int prevX = tailX[0];
    int prevY = tailY[0];
    int prev2X, prev2Y;
    tailX[0] = x;
    tailY[0] = y;

    for (int i = 1; i < nTail; i++) {
        prev2X = tailX[i];
        prev2Y = tailY[i];
        tailX[i] = prevX;
        tailY[i] = prevY;
        prevX = prev2X;
        prevY = prev2Y;
    }

    // Move the snake head
    switch (dir) {
        case LEFT: x--; break;
        case RIGHT: x++; break;
        case UP: y--; break;
        case DOWN: y++; break;
        default: break;
    }

    // Wrap around if the snake hits the edge
    if (x >= width) x = 0;
    else if (x < 0) x = width - 1;

    if (y >= height) y = 0;
    else if (y < 0) y = height - 1;

    // Check for collision with the tail
    for (int i = 0; i < nTail; i++) {
        if (tailX[i] == x && tailY[i] == y) {
            gameover = true;
        }
    }

    // Check if the snake eats the fruit
    if (x == fruitX && y == fruitY) {
        score += 10;
        fruitX = rand() % width;
        fruitY = rand() % height;
        nTail++;
    }
}

int main() {
    Setup();

    while (!gameover) {
        Draw();
        Input();
        Algorithm();
    }

    return 0;
}
