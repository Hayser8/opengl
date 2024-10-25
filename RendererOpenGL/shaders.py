
from xml.dom.expatbuilder import FragmentBuilder

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix *viewMatrix * modelMatrix * vec4(position , 1.0); 
    outTexCoords = texCoords;
    outNormals = normals;
}

'''
#la textura solo se usa n el fragment shader
#gl_Position = modelMatrix * vec4(position + normals * sin(time * 3) / 10, 1.0); 

fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
out vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex, outTexCoords);
}
'''

fat_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix *viewMatrix * modelMatrix * vec4(position +normals * sin(time * 3) / 10 , 1.0); 
    outTexCoords = texCoords;
    outNormals = normals;
}

'''

water_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix *viewMatrix * modelMatrix * vec4(position +vec3(0,1,0) *sin(time * position.x *10)  /10 , 1.0); 
    outTexCoords = texCoords;
    outNormals = normals;
}

'''
wave= '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    vec3 modifiedPosition = position;
    modifiedPosition.y += sin(position.x * 5.0 + time * 3.0) * 0.1; // Efecto de onda
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

pulse = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float scale = 1.0 + 0.2 * sin(time * 2.0);
    vec3 modifiedPosition = position * scale;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(modifiedPosition, 1.0);
    outTexCoords = texCoords;
    outNormals = normals;
}
'''

color = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 textureColor = texture(tex, outTexCoords);
    float dynamicColor = abs(sin(time * 2.0)); // Color cambia con el tiempo
    fragColor = vec4(textureColor.rgb * vec3(dynamicColor, 1.0 - dynamicColor, 0.5), textureColor.a);
}
'''

metallic = '''

#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;

uniform sampler2D tex;

out vec4 fragColor;

void main()
{
    vec4 textureColor = texture(tex, outTexCoords);
    vec3 lightDirection = normalize(vec3(0.5, 1.0, 0.3));
    float intensity = max(dot(normalize(outNormals), lightDirection), 0.0);
    vec3 metalColor = mix(textureColor.rgb, vec3(0.8, 0.8, 0.8), 0.5); // Mezcla con tono metálico
    fragColor = vec4(metalColor * intensity, textureColor.a);
}
'''


