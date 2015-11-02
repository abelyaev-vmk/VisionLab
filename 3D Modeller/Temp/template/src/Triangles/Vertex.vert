//shader version
#version 330 core

uniform mat4 modelViewMatrix;

//inverse and transpose matrix for normals
uniform mat4 normalMatrix;

//projectionMatrix*modelViewMatrix
uniform mat4 modelViewProjectionMatrix;

uniform mat4 viewMatrix;

//input vertex: position, normal, texture coordinates
in vec3 pos;
in vec3 nor;
in vec2 tex;

//output vertex to fragment shader
out VertexData
{
	vec3 position;
	vec3 normal;
	vec2 texcoord;
} VertexOut;
out vec3 LightLocationEye;

const vec4 LightLocation = vec4(5.f, 10.f, 5.f, 1.f);

void main()
{
	gl_Position = modelViewProjectionMatrix*vec4(pos.xyz,1);

	LightLocationEye = vec3(viewMatrix * LightLocation).xyz;
	VertexOut.position = vec3(modelViewMatrix*vec4(pos.xyz,1));
	VertexOut.normal = vec3(normalMatrix*vec4(nor.xyz,1));	
	VertexOut.texcoord = vec2(tex.xy);
}
