//standard libraries
#include <iostream>
using namespace std;

//opengl headers
#include <GL/glew.h>
#include <GL/freeglut.h>

//opengl mathematics
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/matrix_inverse.hpp>

//functions for shader compilation and linking
#include "shaderhelper.h"
//object for drawing
#include "Branch.h"
#include "Leaf.h"
#include "Tree.h"
#include "Sphere.h"

#include <ctime>
#include <random>
#include <vector>
using std::vector;

//model for drawing: a square from two triangles
int b_count;
Leaf* pLeaf;
vector<Tree*> pTree;


//struct for loading shaders
ShaderProgram shaderProgram;

//window size
int windowWidth = 800;
int windowHeight = 600;

//last mouse coordinates
int mouseX,mouseY;

//camera position
glm::vec3 eye(0,10,20);
//reference point position
glm::vec3 cen(0,0,0);
//up vector direction (head of observer)
glm::vec3 up(0,1,0);

//matrices
glm::mat4x4 modelMatrix;
glm::mat4x4 modelViewMatrix;
glm::mat4x4 projectionMatrix;
glm::mat4x4 modelViewProjectionMatrix;
glm::mat4x4 normalMatrix;

///defines drawing mode
bool useTexture = true;
int leafs = 0;
//texture identificator
GLuint texId[1];

//names of shader files. program will search for them during execution
//don't forget place it near executable 
char VertexShaderName[] = "Vertex.vert";
char FragmentShaderName[] = "Fragment.frag";

////////////////////////////////////////////////////////
///
void initTexture()
{
    //generate as many textures as you need
	glGenTextures(1,&texId[0]);
	
    //enable texturing and zero slot
    glActiveTexture(GL_TEXTURE0);
    //bind texId to 0 unit
	glBindTexture(GL_TEXTURE_2D,texId[0]);

	//don't use alignment
	glPixelStorei(GL_UNPACK_ALIGNMENT,1);
	
	// Set nearest filtering mode for texture minification
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);

	//TODO: load texture from file 
	GLubyte imgData[2*2*3] = {
		//row1: yellow,orange
		255,255,0, 255,128,0,
		//row2: green, dark green
		0,255,0, 0,64,0
	};  

	//set Texture Data
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2,2, 0, GL_RGB, GL_UNSIGNED_BYTE, &imgData[0]);
}

float father_height = 19, father_radius = 1.2;
float branch_height = 13, branch_radius = 0.3;
void make_branches(Tree* father)
{
	int i = 0;
	int pass = 0;
	for (; i < father->branch_count; i++)
	{
		Tree* son = new Tree();
		son->sun_number = father->sun_number + 1;
		bool is_leaf = father->sun_number == 5 || rand() % (16 - 3 * son->sun_number) == 0;
		if (is_leaf)
			leafs++;
		father->sons[i] = son;
		pTree.push_back(son);
		int* son_fi = new int[3];
		for (int j = 0; j < 3; j++)
		{
			int koef = (rand() % 2 == 0) ? -1 : 1;
			son_fi[j] = koef * (10 + rand() % 40);
		}
		unsigned int branches_count = rand() % (13 - son->sun_number);
		while (branches_count < 5 && son->sun_number <= 2)
			branches_count = rand() % 10;
		son->branches = (branches_count > 0) ? new glm::vec3[branches_count] : NULL;
		float height = (father->height == father_height) ? branch_height : father->height / 2;
		float radius = (father->radius == father_radius) ? branch_radius : father->radius / 2;
		if (branches_count <= 2)
		{
			branches_count == 5;
			son->sun_number = 4;
		}
		if (is_leaf)
		{
			son->initLeaf(son_fi, father->branches[i]);
			branches_count = 0;
			son->branch_count = 0;
			son->branches = NULL;
		}
		else
			son->initData(height, radius, father->branches[i], son_fi, branches_count);
		son->initGLBuffers(shaderProgram.programObject,"pos","nor","tex");
		if (branches_count > 0)
			make_branches(son);
		else
			son->sons = NULL;
	}
}

/////////////////////////////////////////////////////////////////////
///is called when program starts
void init()
{
	//enable depth test
	glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);
    glDepthMask(GL_TRUE);
	//initialize shader program
	shaderProgram.init(VertexShaderName,FragmentShaderName);
	//use this shader program
	glUseProgram(shaderProgram.programObject);

	

	srand(time(NULL));
	Tree *father = new Tree();
	pTree.push_back(father);
	int *father_fi = new int[3];
	for (int i = 0; i < 3; i++)
		father_fi[i] = 0;
	unsigned int branch_count = 20;
	father->branches = new glm::vec3[branch_count];
	father->is_main_tree = true;
	father->initData(father_height, father_radius, glm::vec3(0, 0, 0), father_fi, branch_count);
	father->initGLBuffers(shaderProgram.programObject,"pos","nor","tex");
	make_branches(father);


	//initializa texture
	initTexture();
}


/////////////////////////////////////////////////////////////////////
///called when window size is changed
void reshape(int width, int height)
{
  windowWidth = width;
  windowHeight = height;
  //set viewport to match window size
  glViewport(0, 0, width, height);
  
  float fieldOfView = 45.0f;
  float aspectRatio = float(width)/float(height);
  float zNear = 0.1f;
  float zFar = 100.0f;
  //set projection matrix
  projectionMatrix = glm::perspective(fieldOfView,aspectRatio,zNear,zFar);
}

float scale = 0.3f;

glm::mat4x4 viewMatrix;

void compute_sons_modelMatrix(Tree* father)
{
	if (father->sons == NULL)
		return;
	for (int i = 0; i < father->branch_count; i++)
	{
		glm::mat4 modelMatrix(father->modelMatrix);
		
		modelMatrix = glm::translate(modelMatrix, father->sons[i]->point);
		modelMatrix = glm::rotate(modelMatrix, (float)father->sons[i]->fi[0], glm::vec3(0, 0, 1));
		modelMatrix = glm::rotate(modelMatrix, (float)father->sons[i]->fi[1], glm::vec3(0, 1, 0));
		modelMatrix = glm::rotate(modelMatrix, (float)father->sons[i]->fi[2], glm::vec3(1, 0, 0));
		father->sons[i]->modelMatrix = modelMatrix;
		compute_sons_modelMatrix(father->sons[i]);
		father->sons[i]->rotate_leaf();
	}
}

#define RN(a,b) (this->rotate_number >= a && this->rotate_number < b)

void Tree::rotate_leaf()
{
	if (!this->is_leaf)
		return;

	if RN(0, 20)
		this->modelMatrix = glm::rotate(this->modelMatrix, 2.0f, glm::vec3(0, 1, 0));
	if RN(30, 40)
			this->modelMatrix = glm::rotate(this->modelMatrix, 2.0f, glm::vec3(1, 0, 0));
	if RN(60, 70)
			this->modelMatrix = glm::rotate(this->modelMatrix, -2.0f, glm::vec3(0, 1, 1));
	if RN(80, 90)
			this->modelMatrix = glm::rotate(this->modelMatrix, -2.0f, glm::vec3(1, 1, 1));
	this->rotate_number = (this->rotate_number + 1) % 90;
}

void Tree::rotate_tree()
{
	if (!this->is_main_tree)
		return;

	if RN(0,40)
		this->modelMatrix = glm::rotate(this->modelMatrix, 0.4f, glm::vec3(0, 1, 0));
	else
	if RN(80,100)
		this->modelMatrix = glm::rotate(this->modelMatrix, 0.4f, glm::vec3(0, 0, 1));
	else
	if RN(160,200)
		this->modelMatrix = glm::rotate(this->modelMatrix, 0.4f, glm::vec3(1, 0, -1));
	else
	if RN(250,270)
		this->modelMatrix = glm::rotate(this->modelMatrix, 0.4f, glm::vec3(-1, -1, 1));
	else
	if RN(320,340)
		this->modelMatrix = glm::rotate(this->modelMatrix, 0.4f, glm::vec3(-1, 1, 1));
	else
	if RN(400,440)
		this->modelMatrix = glm::rotate(this->modelMatrix, 0.4f, glm::vec3(0, -1, -1));
	this->rotate_number = (this->rotate_number + 1) % 440;
}

#define display_makro glBindTexture(GL_TEXTURE_2D,texId[0]); \
	glUniformMatrix4fv(locMV,1,0,glm::value_ptr(modelViewMatrix)); \
	glUniformMatrix4fv(locV,1,0,glm::value_ptr(viewMatrix)); \
	glUniformMatrix4fv(locN,1,0,glm::value_ptr(normalMatrix)); \
	glUniformMatrix4fv(locP,1,0,glm::value_ptr(modelViewProjectionMatrix)); \
	glUniform1ui(texLoc,0); \
	glUniform1i(locFlag,useTexture);



////////////////////////////////////////////////////////////////////
///actions for single frame

void display()
{
	
  glClearColor(0.0,0,0,0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);

  //Draw triangle with shaders (in screen coordinates)
  //need to set uniform in modelViewMatrix
 
  
  glUseProgram(shaderProgram.programObject);

  //we will need this uniform locations to connect them to our variables
  int locMV = glGetUniformLocation(shaderProgram.programObject,"modelViewMatrix");
  int locN = glGetUniformLocation(shaderProgram.programObject,"normalMatrix");
  int locP = glGetUniformLocation(shaderProgram.programObject,"modelViewProjectionMatrix");
  int locV = glGetUniformLocation(shaderProgram.programObject,"viewMatrix");
  int texLoc = glGetUniformLocation(shaderProgram.programObject,"textureSampler");
  int locFlag = glGetUniformLocation(shaderProgram.programObject,"useTexture");
  //if there is some problem
  if (locMV<0 || locN<0 || locP<0 || locV<0 || texLoc <0 || locFlag<0)
  {
	  //not all uniforms were allocated - show green screen.
	  //check your variables properly. May be there is unused?
	  cout << locMV << locN << locP << locV << texLoc << locFlag << endl;
	  glClearColor(0,1,0,1);
	  glClear(GL_COLOR_BUFFER_BIT);
	  //end frame visualization
	  glutSwapBuffers();
	  return;
  }
  viewMatrix = glm::lookAt(eye,cen,up);
  
  modelMatrix = glm::mat4();
  modelMatrix = glm::scale(modelMatrix, scale * glm::vec3(1, 1, 1));
  modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0f, 0.0f, 0.0f));
  pTree[0]->modelMatrix = modelMatrix;
  pTree[0]->rotate_tree();
  compute_sons_modelMatrix(pTree[0]);
  for (int i = 0; i < pTree.size(); i++)
  {
	modelViewMatrix = viewMatrix * pTree[i]->modelMatrix;
	normalMatrix = glm::inverseTranspose(modelViewMatrix);
	modelViewProjectionMatrix = projectionMatrix * modelViewMatrix;
	display_makro;
	pTree[i]->draw();
  }

  glutSwapBuffers();
  
}

//////////////////////////////////////////////////////////////////////////
///IdleFunction
void update()
{
	//make animation
	glutPostRedisplay();
}


/////////////////////////////////////////////////////////////////////////
///is called when key on keyboard is pressed
///use SPACE to switch mode
///TODO: place camera transitions in this function


void keyboard(unsigned char key, int mx, int my)
{
	float speed = 0.03f;
	glm::vec3 temp_vect(0, 0, 0);
	auto crossVect = glm::cross(eye - cen, up);
	switch (key) {
	case 'e':
		for (int i = 0; i < 3; i++) 
		{
			temp_vect[i] = cen[i] - eye[i];
			eye[i] += temp_vect[i] * speed / 3.0f;
			cen[i] += temp_vect[i] * speed / 3.0f;
		}
	break;
	case 'q':
		for (int i = 0; i < 3; i++) 
		{
			temp_vect[i] = cen[i] - eye[i];
			eye[i] -= temp_vect[i] * speed / 3.0f;
			cen[i] -= temp_vect[i] * speed / 3.0f;
		}
	break;
	case 'd':
		crossVect = glm::cross(eye - cen, up);
		glm::normalize(crossVect);
		eye -= crossVect * speed;
		cen -= crossVect * speed;
		break;
	case 'a':
		crossVect = glm::cross(eye - cen, up);
		glm::normalize(crossVect);
		eye += crossVect * speed;
		cen += crossVect * speed;
	break;
	case 'w':
		eye.y += 3 * speed;
		cen.y += 3 * speed;
	break;
	case 's':
		eye.y -= 3 * speed;
		cen.y -= 3 * speed;
	break;

	default:
	break;
	} 
}

/////////////////////////////////////////////////////////////////////////
///is called when mouse button is pressed
///TODO: place camera rotations in this function
bool push = false;
void mouse(int button, int mode, int posx, int posy)
{
	if (button == GLUT_LEFT_BUTTON)
	{
		if (mode == GLUT_DOWN)
		{
			mouseX = posx;
			mouseY = posy;
			push = true;
		}
		else
		{
			mouseX = posx;
			mouseY = posy;
			push = false;
		}
	}
}

#define M_PI 3.14

void mousemove(int posx, int posy)
{
	int _X = 0, _Y = 0;
	float FX;
	glm::vec3 temp_vect;
	if (push) 
	{
		_X = posx - mouseX;
		_Y = posy - mouseY;
		temp_vect = cen - eye;
		FX = _X * M_PI / 180.0f / 10.0f;
		if (_X != 0) {
			cen.z = (float)(eye.z + sin(FX) * temp_vect.x + cos(FX) * temp_vect.z);
			cen.x = (float)(eye.x + cos(FX) * temp_vect.x - sin(FX) * temp_vect.z);
		}
		if (_Y != 0) 
		{
			cen.y -= _Y / 10.0f;
		}
	}
	mouseX = posx;
	mouseY = posy;
}

////////////////////////////////////////////////////////////////////////
///this function is used in case of InitializationError
void emptydisplay()
{
}



glm::vec3 n, v;

////////////////////////////////////////////////////////////////////////
///entry point
int main (int argc, char* argv[])
{
  glutInit(&argc, argv);
#ifdef __APPLE__
  glutInitDisplayMode( GLUT_3_2_CORE_PROFILE| GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
#else
  glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH );
  glutInitContextVersion (3, 2);  
  glutInitContextProfile(GLUT_CORE_PROFILE);
  glutInitContextFlags (GLUT_FORWARD_COMPATIBLE);
  glewExperimental = GL_TRUE;
#endif

  glutCreateWindow("Test OpenGL application");
  glutDisplayFunc(display);
  glutReshapeFunc(reshape);
  glutReshapeWindow(windowWidth,windowHeight);
  glutIdleFunc(update);
  glutKeyboardFunc(keyboard);
  glutMouseFunc(mouse);
  glutMotionFunc(mousemove);
  


  glewInit();
  const char * slVer = (const char *) glGetString ( GL_SHADING_LANGUAGE_VERSION );
  cout << "GLSL Version: " << slVer << endl;
  
  try
  {
	init();
  }
  catch (const char *str)
  {
	  cout << "Error During Initialiation: " << str << endl;
	  delete pLeaf;
	  glDeleteTextures(1,texId);
	  //start main loop with empty screen
	  glutDisplayFunc(emptydisplay);
	  glutMainLoop();
	  return -1;
  }

  
  try
  {
	glutMainLoop();
  }
  catch (const char *str)
  {
	  cout << "Error During Main Loop: " << str << endl;
  }
  //release memory
  delete pLeaf;

  glDeleteTextures(1,texId);
  return 0;
}
