#include "Branch.h"
#ifndef _USE_MATH_DEFINES
#define _USE_MATH_DEFINES
#endif
#include <math.h>

Branch::Branch(void)
{
}


Branch::~Branch(void)
{
}

float get_radius(float radius2, float radius1, int n_step, int step)
{
	return (radius1 - radius2) * step / n_step + radius2;
}

void Branch::initData()
{
	if (pData)
	{
		delete[] pData;
		delete[] pIndices;
	}

	unsigned int radialStep = 10;
	unsigned int heightStep = 10;
	float cylRadius = 1.0f;
	float southRadius = 1.0f;
	float northRadius = 0.3f;

	float B_A = 0.5 * (southRadius - northRadius);
	float normKoef = 1 / sqrt(B_A * B_A + southRadius * southRadius);
	float normX = normKoef * B_A, normY = southRadius * normKoef;

	//number of points
	dataCount = (radialStep+1)*heightStep+2; 
	//number of triangles
	unsigned int nTriangles = 2*radialStep*(heightStep-1)+2*radialStep;
	//number of indices
	indicesCount = 3*nTriangles;

	pData = new VertexData [dataCount];
	pIndices = new unsigned int [indicesCount];
	
	//fill in pData array

	//generate elements on side
	for (unsigned int j=0; j<heightStep; j++)
	{
		float zPos = southRadius*j/(heightStep-1);
		for (unsigned int i=0; i<radialStep+1; i++)
		{
			unsigned int pointId = j*(radialStep+1)+i;

			float fi = 2 * M_PI * i / radialStep; //from 0 to 360 degrees
			//float k = 0.1f * (heightStep - 0.7f * j);
			float xPos = cos(fi); // * k
			float yPos = sin(fi); // * k
			float k = cylRadius - (southRadius - northRadius) * (float(j) / (heightStep - 1));
			pData[pointId].pos = glm::vec3(cylRadius*xPos * k, zPos,cylRadius*yPos * k);
			pData[pointId].nor = glm::vec3(xPos * 0.75f / sqrt(0.56f), float(1 / sqrt(0.56f)), yPos * 0.75f / sqrt(0.56f));
			pData[pointId].tex = glm::vec2((xPos + 1) / 2, (yPos + 1) / 2);		
		}
	}
	//generate north pole
	{
		unsigned int pointId = heightStep*(radialStep+1);
		pData[pointId].pos = glm::vec3(0,southRadius,0);
		pData[pointId].nor = glm::vec3(0,1,0);
		pData[pointId].tex = glm::vec2(0.5f, 0.5f);		
	}
	//generate south pole
	{
		unsigned int pointId = heightStep*(radialStep+1)+1;
		pData[pointId].pos = glm::vec3(0,0,0);
		pData[pointId].nor = glm::vec3(0,-1,0);
		pData[pointId].tex = glm::vec2(0.5f, 0.5f);		
	}
	//fill in pIndices array

	//fill in side triangles (first 6*radialStep*(heightStep-1))
	for (unsigned int j=0; j<heightStep-1; j++)
	{
		for (unsigned int i=0; i<radialStep; i++)
		{
			unsigned int pointId = j*(radialStep+1)+i;
			unsigned int indexId = j*radialStep+i;
			//pData configuration
			//------------------------
			//--.(i,j+1)--.(i+1,j+1)--
			//--.(i,  j)--.(i+1,  j)--
			//------------------------

			//pData indices
			//------------------------
			//--pointId+radialStep+1--pointId+radialStep+2----
			//--pointId---------------pointId+1---------------
			
			//triangle 1			
			//   /|
			//  / |
			// /__|  
			pIndices[6*indexId+0] = pointId;
			pIndices[6*indexId+1] = pointId+1;
			pIndices[6*indexId+2] = pointId+radialStep+2;
			//triangle 2
			// ____
			// |  /
			// | /
			// |/  
			pIndices[6*indexId+3] = pointId;
			pIndices[6*indexId+4] = pointId+radialStep+2;
			pIndices[6*indexId+5] = pointId+radialStep+1;
		}
	}
	//fill in north pole triangles (next 3*radialStep)
	{
		unsigned int startIndex = 6*radialStep*(heightStep-1);
		unsigned int northPoleId = heightStep*(radialStep+1);
		for (unsigned int i=0; i<radialStep; i++)
		{
			//get last row
			unsigned int pointId = (heightStep-1)*(radialStep+1)+i;
			pIndices[startIndex+3*i+0] = pointId;
			pIndices[startIndex+3*i+1] = pointId+1;
			pIndices[startIndex+3*i+2] = northPoleId;
		}
	}
	
	//fill in south pole triangles (last 3*radialStep)
	{
		unsigned int startIndex = 6*radialStep*(heightStep-1)+3*radialStep;	
		unsigned int southPoleId = heightStep*(radialStep+1)+1;

		for (unsigned int i=0; i<radialStep; i++)
		{
			//get first row
			unsigned int pointId = i;
			pIndices[startIndex+3*i+0] = pointId;
			pIndices[startIndex+3*i+1] = southPoleId;
			pIndices[startIndex+3*i+2] = pointId+1;
		}
	}
}
