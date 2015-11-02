//shader version
#version 150 core

//mode of drawing
//if is true, then use Texture
//otherwise draw gradient
uniform int useTexture;

//texture object
uniform sampler2D textureSampler;

//retrieve this data form vertex shader
in VertexData
{
	vec3 position;
	vec3 normal;
	vec2 texcoord;
} VertexIn;

out vec4 fragColor;

//TODO: you should use VertexIn.normal value to evaluate Phong Lightning for this pixel
// 
		
void main()
{
	if (useTexture>0)
		//take color from texture using texture2D
		fragColor = vec4(texture(textureSampler,VertexIn.texcoord.xy).rgb,length(VertexIn.normal)*length(VertexIn.position));
	else
	{
		//use default color (brown)
		fragColor = vec4(0.5,0.2,0.1,1);
	}
}
