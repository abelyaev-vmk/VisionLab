#include "Tree.h"
#ifndef _USE_MATH_DEFINES
#define _USE_MATH_DEFINES
#endif
#include <math.h>
#include <random>
#include <iostream>
#include <ctime>
using std::cout;
using std::endl;

int random(int start, int end)
{
	//srand(clock());
	int r = rand();
	
	cout << "random: from" << start << " to " << end;
	cout << " returns " << start + r % (end - start) << endl;
	srand(clock());
	cout << rand()  << endl;
	return start + r % (end - start);
}

Tree::Tree(void):is_main_tree(false), sun_number(0), rotate_number(0)
{
}


Tree::~Tree(void)
{
}

typedef unsigned int uint;

inline float get_radius(float radius2, float radius1, int n_step, int step)
{
	return (radius1 - radius2) * step / n_step + radius2;
}

void Tree::initData(float length, float radius, glm::vec3 point, int* fi, uint branches_count)
{
	glm::vec4 BV(0,0,0,0);
	glm::vec3 SV(0,1,1);
	SV = glm::reflect(SV, SV);
	if (pData)
	{
		delete[] pData;
		delete[] pIndices;
	}
	this->fi = new int[3];
	this->global_angle = new int[3];
	//this->branches = new glm::vec3[branch_count];
	for (int i = 0; i < 3; i++)
	{
		this->fi[i] = fi[i];
		this->global_angle[i] = 0;
	}
	this->point = point;
	this->height = length;
	this->radius = radius;
	this->branch_count = branches_count;
	this->sons = new Tree*[this->branch_count];
	this->is_leaf = false;

	uint radialStep = 30, heightStep = 2 * (branches_count + 6);
	float cylHeight = length;
	float southRadius = radius;
	float northRadius = 0.4 * southRadius;
	
	float B_A = 0.5 * (southRadius - northRadius);
	float normKoef = 1 / sqrt(B_A * B_A + cylHeight * cylHeight);
	float normX = normKoef * B_A, normY = cylHeight * normKoef;

	dataCount = (radialStep + 1) * heightStep + 2;
	uint nTriangles = 2 * radialStep * (heightStep - 1) + 2 * radialStep;
	indicesCount = 3 * nTriangles;

	pData = new VertexData[dataCount];
	pIndices = new uint[indicesCount];

	uint pointId;
	//on side
	for (uint j = 0; j < heightStep; j++)
	{
		float zPos = cylHeight * j / (heightStep - 1);
		if (j > 6 && j < heightStep - 6 && j % 2 == 1)
			this->branches[j / 2 - 3] = glm::vec3(0, zPos, 0);
		float radius = get_radius(southRadius, northRadius, heightStep, j);
		for (uint i = 0; i < radialStep + 1; i++)
		{
			pointId = j * (radialStep + 1) + i;
			float fi = 2 * M_PI * i / radialStep;
			float xPos = cos(fi);
			float yPos = sin(fi);
			
			pData[pointId].pos = glm::vec3(radius * xPos, zPos, radius * yPos);
			//pData[pointId].nor = glm::vec3(xPos, 0, yPos);
			pData[pointId].nor = glm::vec3(normX, sqrt(1 - normX * normX), normY);
			pData[pointId].tex = glm::vec2((xPos + 1) / 2, (yPos + 1) / 2);
		}
	}
	//north
	pointId = heightStep * (radialStep + 1);
	pData[pointId].pos = glm::vec3(0, cylHeight, 0);
	pData[pointId].nor = glm::vec3(0, 1, 0);
	pData[pointId].tex = glm::vec2(0.5f, 0.5f);

	//south
	pointId += 1;
	pData[pointId].pos = glm::vec3(0, 0, 0);
	pData[pointId].nor = glm::vec3(0, -1, 0);
	pData[pointId].tex = glm::vec2(0.5f, 0.5f);

	//in side triangles
	uint indexId;

	for (uint j = 0; j < heightStep - 1; j++)
		for (uint i = 0; i < radialStep; i++)
		{
			pointId = j * (radialStep + 1) + i;
			indexId = 6 * (j * radialStep + i);

			pIndices[indexId++] = pointId;
			pIndices[indexId++] = pointId + 1;
			pIndices[indexId++] = pointId + radialStep + 2;

			pIndices[indexId++] = pointId;
			pIndices[indexId++] = pointId + radialStep + 2;
			pIndices[indexId] = pointId + radialStep + 1;
		}

	uint startIndex, index;

	//north triangles
	startIndex = 6 * radialStep * (heightStep - 1);
	uint northPoleId = heightStep * (radialStep + 1);
	for (uint i = 0; i < radialStep; i++)
	{
		pointId = (heightStep - 1) * (radialStep + 1) + i;
		index = startIndex + 3 * i;
		pIndices[index++] = pointId;
		pIndices[index++] = pointId + 1;
		pIndices[index] = northPoleId;
	}

	//south triangles
	startIndex += 3 * radialStep;
	uint southPoleId = heightStep * (radialStep + 1) + 1;
	for (uint i = 0; i < radialStep; i++)
	{
		pointId = i;
		index = startIndex + 3 * i;
		pIndices[index++] = pointId;
		pIndices[index++] = southPoleId;
		pIndices[index] = pointId + 1;
	}
}

#define max(a,b) (a>b)?a:b

float equation(float x)
{
	return sqrt(max(0.0f,1.0f - 2*x*x));
}

void Tree::initLeaf(int* fi, glm::vec3 point)
{
	this->point = point;
	is_leaf = true;
	if (pData)
	{
		delete[] pData;
		delete[] pIndices;
	}
	this->fi = new int[3];
	for (int i = 0; i < 3; i++)
		this->fi[i] = fi[i];

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
	
	//fill in pData array
	//right up
	unsigned int startIndex = 0;
	for (unsigned int i=0; i<nInternalQuaterSteps+1; i++)
	{
		float xPos = (1.0f +i)/(nInternalQuaterSteps+2);
		float yPos = equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(xPos/2, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2((xPos+1)/2, (yPos+1)/2);	
	}
	//right down
	startIndex += nInternalQuaterSteps+1;
	for (unsigned int i=0; i<nInternalQuaterSteps; i++)
	{
		float xPos = (1.0f + nInternalQuaterSteps-i)/(nInternalQuaterSteps+2);
		float yPos = -equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(xPos/2, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2((xPos+1)/2, (yPos+1)/2);		
	}
	startIndex += nInternalQuaterSteps;
	//left up
	for (unsigned int i=0; i<nInternalQuaterSteps+1; i++)
	{
		float xPos = -(1.0f+i)/(nInternalQuaterSteps+2);
		float yPos = equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(xPos/2, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2((xPos+1)/2, (yPos+1)/2);		
	}
	//left down
	startIndex += nInternalQuaterSteps+1;
	for (unsigned int i=0; i<nInternalQuaterSteps; i++)
	{
		float xPos = -(1.0f + nInternalQuaterSteps-i)/(nInternalQuaterSteps+2);
		float yPos = -equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(xPos/2, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2((xPos+1)/2, (yPos+1)/2);		
	}
	startIndex += nInternalQuaterSteps;

	//center up
	for (unsigned int i=0; i<nInternalQuaterSteps+1; i++)
	{
		float xPos = (1.0f + i)/(nInternalQuaterSteps+2);
		float yPos = equation(xPos);
			
		pData[startIndex+i].pos = glm::vec3(0, (yPos+1)/2,0);
		pData[startIndex+i].nor = glm::vec3(0,0,-1);
		pData[startIndex+i].tex = glm::vec2(0.5f,0.5f);		
	}
	//center down
	startIndex += nInternalQuaterSteps+1;
	for (unsigned int i=0; i<nInternalQuaterSteps; i++)
	{
		float xPos = (1.0f + nInternalQuaterSteps-i)/(nInternalQuaterSteps+2);
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