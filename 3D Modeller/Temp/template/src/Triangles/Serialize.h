#pragma once
#include "glm\glm.hpp"
#include <iostream>
#include <fstream>
#include "Tree.h"
//using namespace std;
using std::ios;
using std::fstream;
using std::ofstream;
class ISerializer
{
public:
	virtual bool InOut(int&) = 0;
	virtual bool InOut(float&) = 0;
	virtual bool InOut(bool&) = 0;
	virtual bool InOut(mat4&) = 0;
};

class BinarySerializerReader: public ISerializer
{
	FILE *file;
	char* path;
public:
	//virtual bool InOut(int&);
	virtual bool InOut(int&);
	virtual bool InOut(float&);
	virtual bool InOut(bool&);
	virtual bool InOut(mat4&);
	BinarySerializerReader(char* s):path(s){}
	bool Open()
	{
		return file = fopen(path, "rb");
	}
	bool Close()
	{
		fclose(file);
		return true;
	}
	bool End()
	{
		return feof(file);
	}
};

class BinarySerializerWriter: public ISerializer
{
	FILE *file;
	char *path;
public:
	virtual bool InOut(int&);
	virtual bool InOut(float&);
	virtual bool InOut(bool&);
	virtual bool InOut(mat4&);
	BinarySerializerWriter(char*s):path(s){}
	bool Open()
	{
		return file = fopen(path, "wb");
	}
	bool Close()
	{
		return fclose(file);
	}
};

class TextSerializerReader: public ISerializer
{
	fstream file;
	char *path;
public:
	virtual bool InOut(int&);
	virtual bool InOut(float&);
	virtual bool InOut(bool&);
	virtual bool InOut(mat4&);
	TextSerializerReader(char* s){path = new char[40]; strcpy(path, s);}
	bool Open()
	{
		file.open(path, ios::in);
		return file.is_open();
	}
	bool Close()
	{
		file.close();
		return true;
	}
	bool End();
};

class TextSerializerWriter: public ISerializer
{
	ofstream file;
	char *path;
public:
	virtual bool InOut(int&);
	virtual bool InOut(float&);
	virtual bool InOut(bool&);
	virtual bool InOut(mat4&);
	TextSerializerWriter(char*s):path(s) {}
	bool Open()
	{
		file.open(path, ios::out);
		return file.is_open();
	}
	bool Close()
	{
		file.close();
		return true;
	}
};

class SettingsFile
{
public:
	Tree* tree;
	bool Serialize(ISerializer&, bool);
};

