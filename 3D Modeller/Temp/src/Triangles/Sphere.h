#pragma once
#include "MyObject.h"

//branch of tree is flat object, symmetric around y axes
//example equation: y=+-sqrt(1 - x*x/100) (also is symmetric around x)
class Sphere : public MyObject
{
public:
	Sphere(void);
	virtual ~Sphere(void);
	virtual void initData();
};