#include "Leaf.h"

#ifndef max
#define max(a,b) ((a)>(b))?(a):(b)
#endif

Leaf::Leaf(void)
{
}


Leaf::~Leaf(void)
{
}


float Leaf::equation(float x)
{
	return sqrt(max(0.0f,1.0f - 2*x*x));
}
void Leaf::initData(float, float, glm::vec3, int*, unsigned int)
{
	if (pData)
	{
		delete[] pData;
		delete[] pIndices;
	}

	//example equation: y=+-sqrt(1 - x*x/100) (also is symmetric around x)
	unsigned int nInternalQuaterSteps = 5;
	
	//number of points
	dataCount = 3*(nInternalQuaterSteps*2+1) + 2; 
	//number of triangles
	unsigned int nTriangles = 2*4*nInternalQuaterSteps+4;
	//number of indices
	indicesCount = 3*nTriangles;

	pData = new VertexData [dataCount];
	pIndices = new unsigned int [indicesCount];
	float size = 1.0f;
	//fill in pData array
	//right up
	unsigned int startIndex = 0;
	for (unsigned int i=0; i<nInternalQuaterSteps+1; i++)
	{
		float xPos = (size +i)/(nInternalQuaterSteps+2);
		float yPos = equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(xPos/2, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2((xPos+1)/2, (yPos+1)/2);	
	}
	//right down
	startIndex += nInternalQuaterSteps+1;
	for (unsigned int i=0; i<nInternalQuaterSteps; i++)
	{
		float xPos = (size + nInternalQuaterSteps-i)/(nInternalQuaterSteps+2);
		float yPos = -equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(xPos/2, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2((xPos+1)/2, (yPos+1)/2);		
	}
	startIndex += nInternalQuaterSteps;
	//left up
	for (unsigned int i=0; i<nInternalQuaterSteps+1; i++)
	{
		float xPos = -(size+i)/(nInternalQuaterSteps+2);
		float yPos = equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(xPos/2, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2((xPos+1)/2, (yPos+1)/2);		
	}
	//left down
	startIndex += nInternalQuaterSteps+1;
	for (unsigned int i=0; i<nInternalQuaterSteps; i++)
	{
		float xPos = -(size + nInternalQuaterSteps-i)/(nInternalQuaterSteps+2);
		float yPos = -equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(xPos/2, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2((xPos+1)/2, (yPos+1)/2);		
	}
	startIndex += nInternalQuaterSteps;

	//center up
	for (unsigned int i=0; i<nInternalQuaterSteps+1; i++)
	{
		float xPos = (size+ i)/(nInternalQuaterSteps+2);
		float yPos = equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(0, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2(0.5f,0.5f);		
	}
	//center down
	startIndex += nInternalQuaterSteps+1;
	for (unsigned int i=0; i<nInternalQuaterSteps; i++)
	{
		float xPos = (size + nInternalQuaterSteps-i)/(nInternalQuaterSteps+2);
		float yPos = -equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(0, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2(0.5f,0.5f);		
	}
	startIndex += nInternalQuaterSteps;


	//generate north pole
	pData[startIndex].pos = glm::vec3(0,1,0);
	pData[startIndex].nor = glm::vec3(0,0,-1);
	pData[startIndex].tex = glm::vec2(0.5f, 1.0f);		
	
	//generate south pole
	pData[startIndex+1].pos = glm::vec3(0,0,0);
	pData[startIndex+1].nor = glm::vec3(0,0,-1);
	pData[startIndex+1].tex = glm::vec2(0.5f, 0.0f);		
	
	//fill in pIndices array

	//fill in side triangles (first 6*radialStep*(heightStep-1))
	
	//fill in pData array
	startIndex = 0;
	//center and right
	unsigned int startIndex1 = 0;//right
	unsigned int startIndex2 = 2*(2*nInternalQuaterSteps+1);//center
	for (unsigned int i=0; i<2*nInternalQuaterSteps; i++)
	{ 
		pIndices[startIndex+6*i+0] = startIndex2+i;
		pIndices[startIndex+6*i+1] = startIndex1+i;
		pIndices[startIndex+6*i+2] = startIndex1+i+1;

		pIndices[startIndex+6*i+3] = startIndex2+i;
		pIndices[startIndex+6*i+4] = startIndex1+i+1;
		pIndices[startIndex+6*i+5] = startIndex2+i+1;
	}
	startIndex += 3*4*nInternalQuaterSteps;
	//left and center
	startIndex1 = 2*(2*nInternalQuaterSteps+1);//center
	startIndex2 = 1*(2*nInternalQuaterSteps+1);//left
	for (unsigned int i=0; i<2*nInternalQuaterSteps; i++)
	{ 
		pIndices[startIndex+6*i+0] = startIndex2+i;
		pIndices[startIndex+6*i+1] = startIndex1+i;
		pIndices[startIndex+6*i+2] = startIndex1+i+1;

		pIndices[startIndex+6*i+3] = startIndex2+i;
		pIndices[startIndex+6*i+4] = startIndex1+i+1;
		pIndices[startIndex+6*i+5] = startIndex2+i+1;
	}
	startIndex += 3*4*nInternalQuaterSteps;

	//connect north pole
	unsigned int northPoleIndex = 3*(2*nInternalQuaterSteps+1);
	pIndices[startIndex+0] = 2*nInternalQuaterSteps+1;//left top
	pIndices[startIndex+1] = 2*(2*nInternalQuaterSteps+1);//center top
	pIndices[startIndex+2] = northPoleIndex;

	pIndices[startIndex+3] = 2*(2*nInternalQuaterSteps+1);//center top
	pIndices[startIndex+4] = 0;//right top
	pIndices[startIndex+5] = northPoleIndex;
	startIndex += 3*2;

	//connect south pole
	unsigned int southPoleIndex = 3*(2*nInternalQuaterSteps+1)+1;
	pIndices[startIndex+0] = 2*nInternalQuaterSteps+1+2*nInternalQuaterSteps;//left bottom
	pIndices[startIndex+1] = southPoleIndex;
	pIndices[startIndex+2] = 2*(2*nInternalQuaterSteps+1)+2*nInternalQuaterSteps;//center bottom

	pIndices[startIndex+3] = 2*(2*nInternalQuaterSteps+1)+2*nInternalQuaterSteps;//center bottom
	pIndices[startIndex+4] = southPoleIndex;
	pIndices[startIndex+5] = 2*nInternalQuaterSteps;//right bottom
	startIndex += 3*2;
}
