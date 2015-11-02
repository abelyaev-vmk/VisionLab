#pragma once
#include "glm\glm.hpp"
//branch of tree is cylinder
using namespace glm;
class Tree
{
public:
	Tree(): is_leaf(false), angle_x(0), angle_y(0), branches_count(10), height(2), width(0.1f), 
			father(NULL), sons(NULL), modelMatrix(mat4()), scaleMatrix(mat4()) {}
	Tree *father;
	Tree **sons;
	bool is_leaf;
	float angle_x, angle_y;
	int branches_count;
	mat4 modelMatrix;
	mat4 scaleMatrix;
	vec3 point;
	float height, width;
};

