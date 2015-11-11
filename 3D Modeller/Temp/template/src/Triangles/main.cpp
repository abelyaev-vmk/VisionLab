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
#include "Serialize.h"
#include <random>
#include <ctime>
#include <vector>
//model for drawing: a square from two triangles
Branch* pBranch;
Leaf* pLeaf;
using std::vector;
vector<Tree*> pTree;

//struct for loading shaders
ShaderProgram shaderProgram;

//window size
int windowWidth = 800;
int windowHeight = 600;

//last mouse coordinates
int mouseX,mouseY;

//camera position
glm::vec3 eye(0,0,6);
//reference point position
glm::vec3 cen(0.0,2,0);
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

	//create new branch
	pBranch = new Branch();
	//fill in data
	pBranch->initData();

	//initialize opengl buffers and variables inside of object
	pBranch->initGLBuffers(shaderProgram.programObject,"pos","nor","tex");



	
	//create new leaf
	pLeaf = new Leaf();
	//fill in data
	pLeaf->initData();
	//initialize opengl buffers and variables inside of object
	pLeaf->initGLBuffers(shaderProgram.programObject,"pos","nor","tex");



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

////////////////////////////////////////////////////////////////////
///actions for single frame
void display()
{
  glClearColor(0,0,0,0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);

  //Draw triangle with shaders (in screen coordinates)
  //need to set uniform in modelViewMatrix
  
  glUseProgram(shaderProgram.programObject);

  //we will need this uniform locations to connect them to our variables
  int locV = glGetUniformLocation(shaderProgram.programObject, "viewMatrix");
  int locMV = glGetUniformLocation(shaderProgram.programObject,"modelViewMatrix");
  int locN = glGetUniformLocation(shaderProgram.programObject,"normalMatrix");
  int locP = glGetUniformLocation(shaderProgram.programObject,"modelViewProjectionMatrix");
  int texLoc = glGetUniformLocation(shaderProgram.programObject,"textureSampler");
  int locFlag = glGetUniformLocation(shaderProgram.programObject,"useTexture");
  //if there is some problem
  if (locMV<0 || locN<0 || locP<0 || texLoc <0 || locFlag<0 || locV<0)
  {
	  //not all uniforms were allocated - show blue screen.
	  //check your variables properly. May be there is unused?
	  glClearColor(0,0,1,1);
	  glClear(GL_COLOR_BUFFER_BIT);
	  //end frame visualization
	  glutSwapBuffers();
	  return;
  }

  //camera matrix. camera is placed in point "eye" and looks at point "cen".
  glm::mat4x4 viewMatrix = glm::lookAt(eye,cen,up);
  mat4 modelMatrix = mat4();

  for (int i = 0; i < pTree.size(); i++)
  {
	  modelViewMatrix = viewMatrix * pTree[i]->scaleMatrix;
	  normalMatrix = glm::inverseTranspose(modelViewMatrix);
	  modelViewProjectionMatrix = projectionMatrix*modelViewMatrix;
	  glBindTexture(GL_TEXTURE_2D, texId[0]);

	  glUniformMatrix4fv(locV, 1, 0, glm::value_ptr(viewMatrix));
	  glUniformMatrix4fv(locMV, 1, 0, glm::value_ptr(modelViewMatrix));
	  glUniformMatrix4fv(locN, 1, 0, glm::value_ptr(normalMatrix));
	  glUniformMatrix4fv(locP, 1, 0, glm::value_ptr(modelViewProjectionMatrix));
	  glUniform1ui(texLoc, 0);
	  glUniform1i(locFlag, useTexture);
	  
	  if (pTree[i]->is_leaf) 
		  pLeaf->draw();
	  else
		  pBranch->draw();
  }
  

  //end frame visualization
  glutSwapBuffers();
  
}

//////////////////////////////////////////////////////////////////////////
///IdleFunction
void update()
{
	//make animation
	glutPostRedisplay();
}
void makeTree(Tree *tree, int count);

/////////////////////////////////////////////////////////////////////////
///is called when key on keyboard is pressed
///use SPACE to switch mode
///TODO: place camera transitions in this function

char* bin_path = "BinMod.bin";
char *text_path = "TextMod.txt";
BinarySerializerReader BSR(bin_path);
BinarySerializerWriter BSW(bin_path);
TextSerializerReader TSR(text_path);
TextSerializerWriter TSW(text_path);
SettingsFile SF;
bool write = false, read = true;

void keyboard(unsigned char key, int mx, int my)
{
	float speed = 0.03f;
	glm::vec3 temp_vect(0, 0, 0);
	auto crossVect = glm::cross(eye - cen, up);
	Tree *temp;
	int y = 0;
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
	case 'k':
		TSW.Open();
		for (int i = 0; i < pTree.size(); i++)
		{
			SF.tree = pTree[i];
			SF.Serialize(TSW, write);
		}
		TSW.Close();
	break;
	case 'l':
		TSR.Open();
		pTree.clear();
		while (!TSR.End())
		{
			SF.tree = new Tree();
			SF.Serialize(TSR, read);
			pTree.push_back(SF.tree);
		}
		pTree.pop_back();
		TSR.Close();
	break;
	case 'i':
		BSW.Open();
		for (int i = 0; i < pTree.size(); i++)
		{
			SF.tree = pTree[i];
			SF.Serialize(BSW, write);
		}
		BSW.Close();
	break;
	case 'o':
		BSR.Open();
		pTree.clear();
		while (!BSR.End())
		{
			SF.tree = new Tree();
			SF.Serialize(BSR, read);
			pTree.push_back(SF.tree);
		}
		pTree.pop_back();
		BSR.Close();
	break;
	case 'T':
		makeTree(0, 3);
	break;
	case 'N':
		pTree.clear();
		keyboard('T', 0, 0);
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

float get_point(float a, float b, int k, int n)
{
	return ((b - a) * k) / n + a;
}

float get_random_angle(float angle)
{
	int znak = (rand() % 2) ? 1 : -1;
	int r = rand() % 45;
	float answer = (angle + r) * znak;
	return (abs(answer) < 120) ? answer : znak * 60;
}

void makeTree(Tree *tree, int count)
{
	if (count < 0)
		return;
	if (tree == NULL)
	{
		tree = new Tree();
		tree->scaleMatrix = scale(tree->modelMatrix, glm::vec3(tree->width, tree->height, tree->width));
		tree->sons = new Tree*[tree->branches_count];
	}
	else
	{
		tree->modelMatrix = translate(tree->modelMatrix, tree->point);
		tree->modelMatrix = rotate(tree->modelMatrix, tree->angle_x, vec3(1, 0, 0));
		tree->modelMatrix = rotate(tree->modelMatrix, tree->angle_y, vec3(0, 0, 1));
		if (!tree->is_leaf)
			tree->scaleMatrix = scale(tree->modelMatrix, vec3(tree->width, tree->height, tree->width));
		else
			tree->scaleMatrix = scale(tree->modelMatrix, 0.09f * vec3(1, 1, 1));
		if (tree->branches_count > 0) 
			tree->sons = new Tree*[tree->branches_count];
	}

	for (int i = 0; i < tree->branches_count; i++)
	{
		tree->sons[i] = new Tree();
		tree->sons[i]->father = tree;
		tree->sons[i]->point = vec3(0, get_point(tree->height * 0.2, tree->height * 0.93, i + 1, tree->branches_count), 0);
		if (tree->father == NULL)
		{
			tree->sons[i]->height = tree->height * 0.3;
			tree->sons[i]->width = tree->width * 0.3;
		}
		else
		{
			tree->sons[i]->height = tree->height * 0.7;
			tree->sons[i]->width = tree->width * 0.4;
		}

		tree->sons[i]->modelMatrix = tree->modelMatrix;
		tree->sons[i]->angle_x = get_random_angle(tree->angle_x);
		tree->sons[i]->angle_y = get_random_angle(tree->angle_y);
		if (count == 2)
			tree->sons[i]->branches_count = tree->branches_count - 1;
		if (count == 1)
		{
			tree->sons[i]->is_leaf = true;
			tree->sons[i]->branches_count = 0;
		}
		makeTree(tree->sons[i], count - 1);
	}
	pTree.push_back(tree);
}

////////////////////////////////////////////////////////////////////////
///entry point
int main (int argc, char* argv[])
{
	srand(time(NULL));

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
	makeTree(0, 3);
  }
  catch (const char *str)
  {
	  cout << "Error During Initialiation: " << str << endl;
	  delete pBranch;
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
  delete pBranch;
  delete pLeaf;

  glDeleteTextures(1,texId);
  return 0;
}
