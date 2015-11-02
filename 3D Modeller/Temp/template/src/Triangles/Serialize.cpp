#include "Serialize.h"
#include <stdio.h>
using glm::vec3;
using std::fread;
using std::fwrite;
bool BinarySerializerReader::InOut(int& inout)
{
	//file.read((char*)&inout, sizeof inout);
	return true;
}

bool BinarySerializerReader::InOut(float& inout)
{
	fread(&inout, sizeof(float), 1, file);
	return true;
}

bool BinarySerializerReader::InOut(bool &inout)
{
	int t;
	fread(&t, sizeof(int), 1, file);
	inout = t > 0;
	return true;
}

bool BinarySerializerReader::InOut(mat4 &inout)
{
	bool answer = true;
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++)
			answer = answer && InOut(inout[i][j]);
	return answer;
}

bool BinarySerializerWriter::InOut(int& inout)
{
	//file.write((char*)&inout, sizeof inout);
	return true;
}

bool BinarySerializerWriter::InOut(float& inout)
{
	fwrite(&inout, sizeof(float), 1, file);
	return true;
}

bool BinarySerializerWriter::InOut(bool &inout)
{
	int t = (inout) ? 1 : 0;
	fwrite(&t, sizeof(int), 1, file);
	return true;
}

bool BinarySerializerWriter::InOut(mat4 &inout)
{
	bool answer = true;
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++)
			answer = answer && InOut(inout[i][j]);
	return answer;
}

bool TextSerializerReader::InOut(int &inout)
{
	file >> inout;
	return true;
}

bool TextSerializerReader::InOut(float &inout)
{
	file >> inout;
	return true;
}

bool TextSerializerReader::InOut(bool &inout)
{
	int t;
	file >> t;
	inout = t > 0;
	return true;
}

bool TextSerializerReader::InOut(mat4 &inout)
{
	bool answer = true;
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++)
			answer = answer && InOut(inout[i][j]);
	return answer;
}

bool TextSerializerWriter::InOut(int &inout)
{
	file << inout << ' ';
	return true;
}

bool TextSerializerWriter::InOut(float &inout)
{
	file << inout << ' ';
	return true;
}

bool TextSerializerWriter::InOut(bool &inout)
{
	file << (inout) ? 1 : 0 << ' ';
	return true;
}

bool TextSerializerWriter::InOut(mat4 &inout)
{
	bool answer = true;
	for (int i = 0; i < 4; i++)
		for (int j = 0; j < 4; j++)
			answer = answer && InOut(inout[i][j]);
	return answer;
}

bool TextSerializerReader::End()
{
	bool answer;
	answer = file.eof();
	return answer;
}


bool SettingsFile::Serialize(ISerializer &inout, bool)
{
	bool answer = inout.InOut(tree->is_leaf);
	//answer = answer && InOut(tree->angle_x);
	//answer = answer && InOut(tree->angle_y);
	//answer = answer && InOut(tree->branches_count);
	//answer = answer && InOut(tree->height);
	//answer = answer && InOut(tree->width);
	return answer && inout.InOut(tree->scaleMatrix);
}
