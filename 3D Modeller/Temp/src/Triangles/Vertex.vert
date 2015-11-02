#version 330 core

uniform mat4 modelViewMatrix;
uniform mat4 normalMatrix;
uniform mat4 modelViewProjectionMatrix;
uniform mat4 viewMatrix;
in vec3 pos;
in vec3 nor;
in vec2 tex;
out VertexData
{
	vec3 position;
	vec3 normal;
	vec2 texcoord;
} VertexOut;
out vec3 LightLocationEye;
const vec4 LightLocation = vec4(30, 20, 10, 1.f);

void main()
{
	VertexOut.position = vec3(modelViewMatrix*vec4(pos.xyz,1));
	VertexOut.normal = vec3(normalMatrix*vec4(nor.xyz,1));	
	VertexOut.texcoord = vec2(tex.xy);
	LightLocationEye = vec3(viewMatrix * LightLocation).xyz;	
	gl_Position = modelViewProjectionMatrix*vec4(pos.xyz,1);
}
