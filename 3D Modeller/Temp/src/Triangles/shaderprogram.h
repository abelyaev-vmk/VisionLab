#pragma once
#include "shader.h"

class ShaderProgram
{
	Shader vertex,fragment;
public:
	unsigned int programObject;
	
	ShaderProgram();
	~ShaderProgram();
	void init(const char* vName, const char* fName);
};
