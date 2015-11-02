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

//model for drawing: a square from two triangles
Branch* pBranch;
Leaf* pLeaf;
Tree* pTree;


//struct for loading shaders
ShaderProgram shaderProgram;

//window size
int windowWidth = 800;
int windowHeight = 600;

//last mouse coordinates
int mouseX,mouseY;

//camera position
glm::vec3 eye(0,0,10);
//reference point position
glm::vec3 cen(0.0,0,0);
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


	pTree = new Tree();
	pTree->initData();
	pTree->initGLBuffers(shaderProgram.programObject,"pos","nor","tex");


	
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
  int locMV = glGetUniformLocation(shaderProgram.programObject,"modelViewMatrix");
  int locN = glGetUniformLocation(shaderProgram.programObject,"normalMatrix");
  int locP = glGetUniformLocation(shaderProgram.programObject,"modelViewProjectionMatrix");
  int texLoc = glGetUniformLocation(shaderProgram.programObject,"textureSampler");
  int locFlag = glGetUniformLocation(shaderProgram.programObject,"useTexture");
  //if there is some problem
  if (locMV<0 || locN<0 || locP<0 || texLoc <0 || locFlag<0)
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
  
  /*
  ////////////////////////////////////////////
  /////////DRAW BRANCH///////////////////////
  //////////////////////////////////////////

  //modelMatrix is connected with current object
  modelMatrix=glm::mat4();
  
  //3. Translate branch south pole to the point (-0.5, 1.0)
  modelMatrix= glm::translate(modelMatrix,glm::vec3(-0.5f,1.0f,0.0f));

  //2. Rotate cylinder 45 degrees to the left
  modelMatrix = glm::rotate(modelMatrix,45.0f,glm::vec3(0.0f,0.0f,1.0f));
  
  //1. Scale. Make cylinder thinner to look like branch
  modelMatrix = glm::scale(modelMatrix,glm::vec3(0.05f,1.0f,0.05f));
  
  
  //modelViewMatrix consists of viewMatrix and modelMatrix
  modelViewMatrix = viewMatrix*modelMatrix;
  //calculate normal matrix 
  normalMatrix = glm::inverseTranspose(modelViewMatrix);
  //finally calculate modelViewProjectionMatrix
  modelViewProjectionMatrix = projectionMatrix*modelViewMatrix;

  //bind texture
  glBindTexture(GL_TEXTURE_2D,texId[0]);
  
  
  //pass variables to the shaders
  glUniformMatrix4fv(locMV,1,0,glm::value_ptr(modelViewMatrix));
  glUniformMatrix4fv(locN,1,0,glm::value_ptr(normalMatrix));
  glUniformMatrix4fv(locP,1,0,glm::value_ptr(modelViewProjectionMatrix));
  glUniform1ui(texLoc,0);
  glUniform1i(locFlag,useTexture);

  //draw branch
  pBranch->draw();*/


  /////////////////DRAW TREE

  //modelMatrix is connected with current object
  modelMatrix=glm::mat4();
  
  //3. Translate branch south pole to the point (-0.5, 1.0)
  modelMatrix= glm::translate(modelMatrix,glm::vec3(-0.5f,1.0f,0.0f));

  //2. Rotate cylinder 45 degrees to the left
  modelMatrix = glm::rotate(modelMatrix,45.0f,glm::vec3(0.0f,0.0f,1.0f));
  
  //1. Scale. Make cylinder thinner to look like branch
  modelMatrix = glm::scale(modelMatrix,glm::vec3(0.05f,1.0f,0.05f));
  
  
  //modelViewMatrix consists of viewMatrix and modelMatrix
  modelViewMatrix = viewMatrix*modelMatrix;
  //calculate normal matrix 
  normalMatrix = glm::inverseTranspose(modelViewMatrix);
  //finally calculate modelViewProjectionMatrix
  modelViewProjectionMatrix = projectionMatrix*modelViewMatrix;

  //bind texture
  glBindTexture(GL_TEXTURE_2D,texId[0]);
  
  
  //pass variables to the shaders
  glUniformMatrix4fv(locMV,1,0,glm::value_ptr(modelViewMatrix));
  glUniformMatrix4fv(locN,1,0,glm::value_ptr(normalMatrix));
  glUniformMatrix4fv(locP,1,0,glm::value_ptr(modelViewProjectionMatrix));
  glUniform1ui(texLoc,0);
  glUniform1i(locFlag,useTexture);

  //draw branch
  pTree->draw();





  //////////////////////////////////////////
  //////////////DRAW LEAF///////////////////
  //////////////////////////////////////////

  //modelMatrix is connected with current object
  modelMatrix=glm::mat4();
  
  //3. Translate branch south pole to the north pole of branch
  modelMatrix= glm::translate(modelMatrix,glm::vec3(-1.0f/sqrt(2.0f)-0.5f,1.0f/sqrt(2.0f)+1.0f,0.0f));

  //2. Scale. Make leaf smaller
  modelMatrix = glm::scale(modelMatrix,0.3f*glm::vec3(1.0f,1.0f,1.0f));

  //1. Translate branch south pole to (0,0)
  modelMatrix= glm::translate(modelMatrix,glm::vec3(0.0f,0.0f,0.0f));
  
  
  //modelViewMatrix consists of viewMatrix and modelMatrix
  modelViewMatrix = viewMatrix*modelMatrix;
  //calculate normal matrix 
  normalMatrix = glm::inverseTranspose(modelViewMatrix);
  //finally calculate modelViewProjectionMatrix
  modelViewProjectionMatrix = projectionMatrix*modelViewMatrix;
  
  //pass variables to the shaders
  glUniformMatrix4fv(locMV,1,0,glm::value_ptr(modelViewMatrix));
  glUniformMatrix4fv(locN,1,0,glm::value_ptr(normalMatrix));
  glUniformMatrix4fv(locP,1,0,glm::value_ptr(modelViewProjectionMatrix));

  //draw leaf
  pLeaf->draw();


  ////////DRAW SECOND LEAF

  //modelMatrix is connected with current object
  modelMatrix=glm::mat4();
  
  //3. Translate branch south pole to the north pole of branch
  modelMatrix= glm::translate(modelMatrix,glm::vec3(-1/sqrt(4.0f),1,0));

  //2. Scale. Make leaf smaller
  modelMatrix = glm::scale(modelMatrix,0.6f*glm::vec3(1.0f,1.0f,1.0f));

  //1. Translate branch south pole to (0,0)
  modelMatrix= glm::translate(modelMatrix,glm::vec3(0.0f,0.0f,0.0f));
  
  modelMatrix = glm::rotate(modelMatrix, 180.0f, glm::vec3(0.0f, 0.0f, 1.0f));  
  //modelViewMatrix consists of viewMatrix and modelMatrix
  modelViewMatrix = viewMatrix*modelMatrix;
  //calculate normal matrix 
  normalMatrix = glm::inverseTranspose(modelViewMatrix);
  //finally calculate modelViewProjectionMatrix
  modelViewProjectionMatrix = projectionMatrix*modelViewMatrix;
  
  //pass variables to the shaders
  glUniformMatrix4fv(locMV,1,0,glm::value_ptr(modelViewMatrix));
  glUniformMatrix4fv(locN,1,0,glm::value_ptr(normalMatrix));
  glUniformMatrix4fv(locP,1,0,glm::value_ptr(modelViewProjectionMatrix));

  //draw leaf
  pLeaf->draw();
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


/////////////////////////////////////////////////////////////////////////
///is called when key on keyboard is pressed
///use SPACE to switch mode
///TODO: place camera transitions in this function
void keyboard(unsigned char key, int mx, int my)
{
	if (key==' ')
		useTexture = !useTexture;
	else if (key=='w')
		cen[1] += 1;
	else if (key=='s')
		cen[1] -= 1;
	else if (key=='a')
		cen[0] -= 1;
	else if (key=='d')
		cen[0] += 1;
	else if (key=='q')
		eye[2] += 1;
	else if (key=='e')
		eye[2] -= 1;
}

/////////////////////////////////////////////////////////////////////////
///is called when mouse button is pressed
///TODO: place camera rotations in this function
void mouse(int button, int mode,int posx, int posy)
{
	if (button==GLUT_LEFT_BUTTON)
	{
		if (mode == GLUT_DOWN)
		{
			mouseX = posx; mouseY = posy;
		}
		else
		{
			mouseX = -1; mouseY = -1;
		}
	}
	
}

////////////////////////////////////////////////////////////////////////
///this function is used in case of InitializationError
void emptydisplay()
{
}

////////////////////////////////////////////////////////////////////////
///entry point
int n_main (int argc, char* argv[])
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
