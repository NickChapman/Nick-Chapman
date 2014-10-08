//Defines
#define _USE_MATH_DEFINES
#define WINDOW_WIDTH 800.0
#define WINDOW_HEIGHT 800.0

//Game mechanics
#define COLLISION_DAMPENING_FACTOR .9 //The amount of energy which is maintained during collisions
#define TIME_STEP 30.0 //Number of milliseconds to wait between frames
#define STEPS_PER_SECOND 50.0 //The number of time steps per game second
#define NUMBER_OF_ASTEROIDS 5
#define NUMBER_OF_ROCKETS 3
#define ROCKET_SPEED -5.0 //Negative so that rockets move up the screen
/*
Having TIME_STEP and STEPS_PER_SECOND allows for the speed of the asteroids to be globally adjusted
while also maintaining a silky smooth frame rate
*/

//Includes
#include "SFML\Graphics.hpp"
#include <iostream>
#include <random>
#include <cmath>
#include <Windows.h>

using namespace std;

//Distribution short-hand functions
uniform_int_distribution<> distribution(int min, int max){
	return uniform_int_distribution<>(min, max);
}
uniform_real_distribution<> distribution(double min, double max){
	return uniform_real_distribution<>(min, max);
}

struct ASTEROID{
	sf::Sprite visual;
	double speed;
	double direction_angle; //radians
	double mass;
	double KE; //Kinetic energy
	double momentum;
	double width;
	double height;
	double x_position;
	double y_position;
	bool active;

	ASTEROID(){
		//Blank constructor for no args
	}

	//Builds an asteroid with a number of random properties
	ASTEROID(sf::Texture &asteroid_texture, double sprite_width, double sprite_height, double min_mass = 1.0, double max_mass = 100.0, double max_speed = 10.0){
		
		//Load a twist engine for distribution computations
		std::random_device rd;
		std::mt19937 twist_engine(rd());
		
		//Set sprite texture
		visual.setTexture(asteroid_texture);

		//Pick a random color out of the list of colors
		sf::Color colors[] = {sf::Color::Blue, sf::Color::Cyan, sf::Color::Green, sf::Color::Magenta, sf::Color::Red, sf::Color::White, sf::Color::Yellow };
		//Create a distribution which runs from 0 to Length of colors[] - 1. Minus 1 because array index starts at 0
		auto color_choices = distribution(0, sizeof(colors) / sizeof(colors[0]) - 1);
		//Pick a random number, plug it into the colors array, finally set the visual color the chosen color
		sf::Color asteroid_color = colors[color_choices(twist_engine)];
		visual.setColor(asteroid_color);

		//Generate a random mass for the asteroid
		auto mass_distribution = distribution(min_mass, max_mass);
		mass = mass_distribution(twist_engine);

		//Generate a random speed and direction angle
		auto angle_distribution = distribution(0.0, M_PI);
		auto speed_distribution = distribution(1.0, max_speed); //Minimum speed of 1 so that the asteroid is always initialized as moving
		direction_angle = angle_distribution(twist_engine);
		speed = speed_distribution(twist_engine);

		//Set the physical quantities
		momentum = mass*speed; //Newtonian momentum formula
		KE = .5 * mass * speed * speed; //Newtonian kinetic energy formula

		//Get the width and the height of the sprite
		sf::FloatRect visual_dimensions = visual.getLocalBounds();

		width = sprite_width;
		height = sprite_height;

		//Scale the sprite to the desired dimensions - desired / actual
		visual.setScale(width / visual_dimensions.width, height / visual_dimensions.height);

		//Generate a random starting position for the asteroid
		//Uses the #define'd WINDOW_WIDTH and WINDOW_HEIGHT
		//Arguably there's no point to displaying fractional position parts but for computation the fractional parts are useful
		auto horizontal_positions = distribution(0.0, WINDOW_WIDTH);
		auto vertical_positions = distribution(0.0, WINDOW_HEIGHT);
		x_position = horizontal_positions(twist_engine);
		y_position = vertical_positions(twist_engine);
		visual.setPosition(x_position, y_position);

		active = true;
	}

	void move(){
		double delta_x, delta_y, time;
		time = TIME_STEP / STEPS_PER_SECOND; // 100 for the time step would mean 1 second
		//Each delta equals the component of the velocity in its respective direction * the time. Distance = rate * time, simple stuff
		//Cos(direction_angle) for x and sin(direction_angle) for y
		delta_x = cos(direction_angle) * speed * time;
		delta_y = sin(direction_angle) * speed * time;
		x_position += delta_x;
		y_position += delta_y;
		
		/* 
			Now check to see if this moved the asteroid off the screen
			Use.getPosition to get the x and y values of the asteroids upper left hand corner
				If(x position + width) < 0:
					The object has gone off the left side of the screen
					Move it to the right side of the screen
				If(x position > window width) :
					Object off the right side of the screen
					Move to the left side
						- asteroid width so that it doesnt start right on the edge, but rather a little off
				If(y position + height) < 0 :
					Object gone off top
					Move to bottom
				If(y position > window height) :
					Object gone off bottom
					Move to top
						- asteroid height so that it doesn't start right on the edge but rather a little off
				If all is good:
					just .move(dx, dy)
		*/
		double x = visual.getPosition().x;
		double y = visual.getPosition().y;
		if (x + width < 0)
			visual.setPosition(WINDOW_WIDTH, y);
		else if (x > WINDOW_WIDTH)
			visual.setPosition(-1.0 * width, y);
		else if (y + height < 0)
			visual.setPosition(x, WINDOW_HEIGHT);
		else if (y > WINDOW_HEIGHT)
			visual.setPosition(x, -1.0 * height);
		else
			visual.move(delta_x, delta_y);
	}

	/*
		Moves the asteroid 1000 pixels off screen in both directions and sets its speed, width, and height to 0
		This makes it impossible for anything to collide with the asteroid
	*/
	void kill(){
		visual.setPosition(WINDOW_WIDTH + 1000, WINDOW_HEIGHT + 1000);
		speed = 0;
		width = 0;
		height = 0;
		active = false;
	}
};

//Asteroid Comparison functions
bool operator==(const ASTEROID& lhs, const ASTEROID& rhs)
{
	if (lhs.direction_angle == rhs.direction_angle && lhs.height == rhs.height && lhs.KE == rhs.KE && lhs.mass == rhs.mass
		&& lhs.momentum == rhs.momentum && lhs.speed == rhs.speed  && lhs.width == rhs.width){
		return true;
	}
	else{
		return false;
	}
}

//Game functions

bool is_collision(ASTEROID &ast1, ASTEROID &ast2){
	//Position shorthands
	double a1x = ast1.visual.getPosition().x;
	double a1y = ast1.visual.getPosition().y;
	double a2x = ast2.visual.getPosition().x;
	double a2y = ast2.visual.getPosition().y;

	/*
		Check for collision by checking if each asteroids top left corner falls within side the position box of the other
		Position box x:
			From: Top left coordinate 
			To: Top left coordinate + width
		Position box y:
			From: Top left coordinate
			To: Top left coordinate + height

		Note: comparisons use < and > instead of <= and >= because the asteroids are INSIDE the rectangles
		A collision at the edge of the rectangle doesn't really mean the asteroids touched. They won't appear to touch on screen at least.
	*/
	if (((a1x > a2x && a1x < (a2x + ast2.width)) && (a1y > a2y && a1y < (a2y + ast2.height))) ||
		((a2x > a1x && a2x < (a1x + ast1.width)) && (a2y > a1y && a2y < (a1y + ast1.height))))
		return true;
	else
		return false;
}

//Check for collision between rocket and asteroid. Same principle as before
bool is_collision(ASTEROID &ast, sf::Sprite &rocket){
	double r_width = rocket.getLocalBounds().width;
	double r_height = rocket.getLocalBounds().height;
	double ast_x = ast.visual.getPosition().x;
	double ast_y = ast.visual.getPosition().y;
	double r_x = rocket.getPosition().x;
	double r_y = rocket.getPosition().y;

	if (((ast_x > r_x && ast_x < (r_x + r_width)) && (ast_y > r_y && ast_y < (r_y + r_height))) ||
		((r_x > ast_x && r_x < (ast_x + ast.width)) && (r_y > ast_y && r_y < (ast_y + ast.height))))
		return true;
	else
		return false;
}

void collision_physics(ASTEROID &ast1, ASTEROID &ast2){
	double total_x_momentum, total_y_momentum, total_energy;
	//Sum of each asteroid_mass * asteroid_speed * COS(asteroid_direction_angle)
	total_x_momentum = ast1.momentum * cos(ast1.direction_angle) + ast2.momentum * cos(ast2.direction_angle);
	//Sum of each asteroid_mass * asteroid_speed * SIN(asteroid_direction_angle)
	total_y_momentum = ast1.momentum * sin(ast1.direction_angle) + ast2.momentum * sin(ast2.direction_angle);
	//Total energy is simply the sum of both energies
	total_energy = ast1.KE + ast2.KE;

	/*
	Momentum is always conserved
	Energy is conserved to the extent of the COLLISION_DAMPENING_FACTOR
	The CDF is what percentage of the starting energy is conserved

	The following equations are based on solving the equations for momentum and energy.
	The math is complicated and based on the assumption that:
	Both asteroids have a mass greater than 0
	The CDF is greater than 0
	For full explanation email nlc35@georgetown.edu
	**I'm sorry for magic numbers used here but they are equation coefficients not made up nonsense**
	*/

	double CDF = COLLISION_DAMPENING_FACTOR;
	double ast1_x_speed = (ast1.mass * CDF * total_x_momentum - sqrt(ast1.mass * ast2.mass * CDF *
		(2 * ast1.mass * total_energy + 2 * ast2.mass * total_energy - CDF * pow(total_x_momentum, 2.0))))
		/ (ast1.mass * CDF * (ast1.mass + ast2.mass));
	double ast2_x_speed = (sqrt(ast1.mass * ast2.mass * CDF * (2 * ast1.mass * total_energy +
		2 * ast2.mass * total_energy - CDF *pow(total_x_momentum, 2.0))) + ast2.mass * CDF * total_x_momentum)
		/ (ast2.mass * CDF * (ast1.mass + ast2.mass));
	double ast1_y_speed = (ast1.mass * CDF * total_y_momentum - sqrt(ast1.mass * ast2.mass * CDF *
		(2 * ast1.mass * total_energy + 2 * ast2.mass * total_energy - CDF * pow(total_y_momentum, 2.0))))
		/ (ast1.mass * CDF * (ast1.mass + ast2.mass));
	double ast2_y_speed = (sqrt(ast1.mass * ast2.mass * CDF * (2 * ast1.mass * total_energy +
		2 * ast2.mass * total_energy - CDF *pow(total_y_momentum, 2.0))) + ast2.mass * CDF * total_y_momentum)
		/ (ast2.mass * CDF * (ast1.mass + ast2.mass));
	//Pythag to get resultant speeds
	ast1.speed = sqrt(pow(ast1_x_speed, 2.0) + pow(ast1_y_speed, 2.0));
	ast2.speed = sqrt(pow(ast2_x_speed, 2.0) + pow(ast2_y_speed, 2.0));
	//Inverse tangent to get new direction angles
	ast1.direction_angle = atan(ast1_y_speed / ast1_x_speed);
	ast2.direction_angle = atan(ast2_y_speed / ast2_x_speed);
	//The asteroids now need to be moved so they are not colliding.
	while (is_collision(ast1, ast2)){
		ast1.move();
		ast2.move();
	}

}

/*
	Loop through every asteroid
	For every asteroid loop through and see if it touches another asteroid
		BUT check to make sure the asteroid you're checking against is not itself
*/
void check_for_collisions(ASTEROID asteroids[], sf::Sprite rockets[]){
	for (int i = 0; i < NUMBER_OF_ASTEROIDS; i++){
		for (int j = 0; j < NUMBER_OF_ASTEROIDS; j++){
			//Check for asteroid asteroid collisions
			if (asteroids[i] == asteroids[j]){
				continue;
			}
			else{
				if (is_collision(asteroids[i], asteroids[j])){
					cout << "COLLISION!" << endl;
					collision_physics(asteroids[i], asteroids[j]);
				}
			}
		}
		//Check for rocket asteroid collisions
		for (int j = 0; j < NUMBER_OF_ROCKETS; j++){
			if (is_collision(asteroids[i], rockets[j])){
				//TODO
				//Move the rocket off screen to some factor of its position in the array so that they don't touch each other
				rockets[j].setPosition(WINDOW_WIDTH + 1000 * j, WINDOW_HEIGHT + 1000 * j);
				//Call the .kill method on the asteroid 
				asteroids[i].kill();
			}
		}
	}
}

int main()
{
	//Create the asteroids
	//Load their texture
	sf::Texture asteroid_texture, rocket_texture;
	asteroid_texture.loadFromFile("C:/Users/Nick/Documents/Visual Studio 2013/Projects/Assn2B/Assn2B/sprites/asteroid.gif");
	rocket_texture.loadFromFile("C:/Users/Nick/Documents/Visual Studio 2013/Projects/Assn2B/Assn2B/sprites/rocket.png");
	
	ASTEROID asteroids[NUMBER_OF_ASTEROIDS];
	//Create 5 asteroids
	for (int i = 0; i < NUMBER_OF_ASTEROIDS; i++){
		asteroids[i] = ASTEROID(asteroid_texture, 30, 30);
	};

	//Create the rockets
	sf::Sprite rockets[NUMBER_OF_ROCKETS];
	for (int i = 0; i < NUMBER_OF_ROCKETS; i++){
		rockets[i].setTexture(rocket_texture);
		//Position the rockets off the bottom of the screen where they wait to be fired
		rockets[i].setPosition(0, WINDOW_HEIGHT + 1000);
	}

	//Fill the rocket speeds array with 0 so the rockets don't move onto the screen
	//We need this array so we can still the rockets later
	double rocket_speeds[NUMBER_OF_ROCKETS] = {0};
	

	//Some game variables
	bool rockets_left = true;
	int current_rocket_index = 0; //The index of the next rocket to fire


	sf::RenderWindow window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Assignment 2B - Asteroid Game");

	//TODO: DELETE THIS
	sf::RectangleShape dot(sf::Vector2f(3, 3));
	dot.setFillColor(sf::Color::Yellow);

	while (window.isOpen())
	{
		sf::Event event;
		while (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				window.close();
		}

		window.clear();

		//Check if there are rockets left
		if (!rockets_left){
			//See if the last rocket is still on the screen
			if (rockets[NUMBER_OF_ROCKETS - 1].getPosition().y + rockets[NUMBER_OF_ROCKETS].getLocalBounds().height < 0){
				//Last rocket is off screen, game is over.
				break;
			}
		}

		//If space is pressed fire the current rocket
		if (sf::Keyboard::isKeyPressed(sf::Keyboard::Space)){
			/* .setPosition the rocket at the bottom middle:
			x position:
			(window width - rocket width) / 2
			Y position:
			(window height - rocket height) */
			//Getting the rocket height and width
			if (rockets_left){
				sf::FloatRect rocket_bounds = rockets[current_rocket_index].getLocalBounds();
				rockets[current_rocket_index].setPosition((WINDOW_WIDTH - rocket_bounds.width) / 2.0, WINDOW_HEIGHT - rocket_bounds.height);
				//Set this rockets speed to ROCKET_SPEED
				rocket_speeds[current_rocket_index] = ROCKET_SPEED;
				//Incrase the rocket index counter
				current_rocket_index += 1;
				if (current_rocket_index == NUMBER_OF_ROCKETS){
					rockets_left = false;
				}
			}
		}


		//Draw all of the asteroids
		for (int i = 0; i < NUMBER_OF_ASTEROIDS; i++)
		{
			if (asteroids[i].active){
				window.draw(asteroids[i].visual);
			}
			//TODO: DELETE THIS
			/*
			dot.setPosition(asteroids[i].visual.getPosition().x, asteroids[i].visual.getPosition().y);
			window.draw(dot);
			dot.move(asteroids[i].width, asteroids[i].height);
			window.draw(dot);
			*/
		}
		//Draw all of the rockets, though they spend most of their life off screen
		for (int i = 0; i < NUMBER_OF_ROCKETS; i++){
			window.draw(rockets[i]);
		}
		window.display();

		//Move all of the asteroids
		for (int i = 0; i < (sizeof(asteroids) / sizeof(asteroids[0])); i++)
		{
			asteroids[i].move();
		}
		//Move all of the rockets their speed
		for (int i = 0; i < NUMBER_OF_ROCKETS; i++){
			rockets[i].move(0, TIME_STEP / STEPS_PER_SECOND * rocket_speeds[i]); // 0 for x change because rockets fire straight up
			//Check if any of the rockets have gone off the top of the screen, if so put em in the graveyard
			if (rockets[i].getPosition().y + rockets[i].getLocalBounds().height < 0){
				//Rocket is off screen
				//Move the rocket off screen to some factor of its position in the array so that they don't touch each other, this is to prevent future collision weirdness
				rockets[i].setPosition(WINDOW_WIDTH + 1000 * i, WINDOW_HEIGHT + 1000 * i);
				//Set the speed to 0 so it doesn't move any more
				rocket_speeds[i] = 0;
			}
		}
		check_for_collisions(asteroids, rockets);
		Sleep(TIME_STEP);
	}
	
	return 0;
}

//TODO: For future versions the asteroids should have different radii depending on their mass so that its clear when one has more mass
//The collisions looks wonky right now because certain asteroids are more massive but they all look the same.