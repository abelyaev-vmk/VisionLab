#pragma once
#include "Tree.h"

//branch of tree is flat object, symmetric around y axes
//example equation: y=+-sqrt(1 - x*x/100) (also is symmetric around x)
class Leaf : public Tree
{
public:
	Leaf(void);
	virtual ~Leaf(void);
	virtual void initData(float, float, glm::vec3, int*, unsigned int);

private:
	float equation(float x);
};

