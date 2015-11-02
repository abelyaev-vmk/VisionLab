#version 330 core


uniform int useTexture;
uniform sampler2D textureSampler;
in VertexData
{
	vec3 position;
	vec3 normal;
	vec2 texcoord;
} VertexIn;
in vec3 LightLocationEye;
out vec4 fragColor;
const vec4 ka = vec4(0.06,0.06,0.06,1.0);
const vec4 ks = vec4(0.9,0.9,0.9,0.6);
const float ke = 20;	

void main()
{
	vec4 Phong;
	vec3 light = normalize(LightLocationEye - VertexIn.position);
	vec3 normal = normalize(VertexIn.normal);
	vec3 eye = normalize(VertexIn.position);
	float diffuseIntensity = clamp(max(dot(normal, light), 0.0), 0.0, 1.0);
	vec3 reflection = normalize(reflect(light, normal));
	float specularIntensity = pow(clamp(max(dot(reflection, eye), 0.0), 0.0, 1.0), ke);
	if (useTexture>0)
	{
		fragColor = vec4(texture(textureSampler,VertexIn.texcoord.xy).rgb,length(VertexIn.normal)*length(VertexIn.position));
		fragColor = ka + fragColor * diffuseIntensity + ks * specularIntensity;
	}
	else
		fragColor = vec4(0.5,0.2,0.1,1);
}
