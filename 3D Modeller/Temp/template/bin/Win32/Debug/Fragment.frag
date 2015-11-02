//shader version
#version 330 core

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

in vec3 LightLocationEye;

out vec4 fragColor;

const vec4 ka = vec4(0.07,0.07,0.07,1.0);//vec4(0.05, 0.05, 0.05, 1.0);
const vec4 ks = vec4(0.4, 0.4, 0.4, 0.4);//vec4(1.,1.,1.,0.6);//
const float ke = 10;

void main()
{
	vec4 Phong;
	vec3 light = normalize(LightLocationEye - VertexIn.position);
	vec3 normal = normalize(VertexIn.normal);
	vec3 eye = normalize(VertexIn.position);

	float diffuseIntensity = clamp(max(dot(normal, light), 0.0), 0.2, 1.0);
	vec3 reflection = normalize(reflect(light, normal));
	float specularIntensity = pow(clamp(max(dot(reflection, eye), 0.0), 0.2, 1.0), ke);


	if (useTexture>0){
		//take color from texture using texture2D
		fragColor = vec4(texture(textureSampler,VertexIn.texcoord.xy).rgb,length(VertexIn.normal)*length(VertexIn.position));
		Phong = ka + fragColor * diffuseIntensity + ks * specularIntensity;
		fragColor = Phong;
	}
	else
	{
		//use default color (brown)
		fragColor = vec4(0.5,0.2,0.1,1);
		Phong = ka + fragColor * diffuseIntensity + ks * specularIntensity;
		fragColor = Phong;
	}
}
