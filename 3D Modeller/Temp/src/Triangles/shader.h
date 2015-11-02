#pragma once

class Shader
{
public:
	enum STATUS {SUCCESS, FILE_NOT_FOUND, EMPTY_FILE, READ_ERROR};
	unsigned int shaderObject;
private:
	STATUS iStatus;
	char* strName;
	char* strSource;
	unsigned long iLength;
	unsigned int shaderType;
public:
	Shader();
	~Shader();
	STATUS read(const char *filename,unsigned int type);
	int compile();
	int readAndCompile(const char* filename,unsigned int type);
	void Release();
};

