#pragma once
#include "MyObject.h"

//branch of tree is cylinder
class Branch :
	public MyObject
{
public:
	Branch(void);
	virtual ~Branch(void);
	//redefinition of 
	virtual void initData();
};

