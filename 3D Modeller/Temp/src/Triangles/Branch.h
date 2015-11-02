#pragma once
#include "MyObject.h"

//branch of tree is cylinder
class Branch : public MyObject
{
public:
	Branch();
	virtual ~Branch(void);
	//redefinition of 
	virtual void initData(float, float, int);
	glm::vec3 *branches;
	float* fi;
};

