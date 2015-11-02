#pragma once
#include "MyObject.h"

//branch of tree is cylinder
class Tree : public MyObject
{
public:
	Tree();
	virtual ~Tree(void);
	//redefinition of 
	virtual void initData(float length, float radius, glm::vec3 point, int* fi, unsigned int branches_count);
	virtual void initLeaf(int* fi, glm::vec3 point);
	glm::vec3* branches;
	glm::vec3 point;
	int* fi;
	int branch_count;
	float height, radius;
	Tree **sons;
	glm::mat4 modelMatrix;
	int* global_angle;
	bool is_leaf, is_main_tree;
	int sun_number;
	void rotate_leaf();
	void rotate_tree();
	int rotate_number;
};

int random(int, int);